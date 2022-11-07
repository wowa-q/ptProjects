
import logging
import datetime
from operator import or_
import sqlite3 as sql
from unicodedata import name
from requests import Session
from sqlalchemy import create_engine, not_, text, Table, Column, Integer, String, MetaData, select, ForeignKey
from sqlalchemy.sql import select, or_, and_, not_
from sqlalchemy.orm import sessionmaker


DEBUGLEVEL = 1
INFO = True

class EngineMaker(object):
    def __init__(self, pth, db_name, db_type):
        self.__path = pth
        self.__name = db_name
        self.__type = db_type   
    
    def createEngine(self):
        engine = None
        if self.__type == "sqlite3":
            db_pth = str(self.__path) + "/" + self.__name + '.db'
            # respect this: https://docs.sqlalchemy.org/en/14/core/pooling.html#pool-disconnects
            engine = create_engine("sqlite:///"+db_pth, pool_pre_ping=True, echo=INFO)
            logging.debug(f'Engine for DB created at:  {db_pth}')
            if DEBUGLEVEL > 0: print(f"# createEngine: db-Name: {db_pth}")
        return engine

    def getMetaData(self):
        metadata = MetaData()
        return metadata

class DB_Handler(object):
    
    # initiaization
    def __init__(self, pth, db_name, db_type):
        self.__path = pth
        self.__name = db_name
        self.__type = db_type 
        self.tableName = {}

    # Engine Maker:
        self.maker = EngineMaker(pth, db_name, db_type)
        self.engine = self.maker.createEngine()
        self.metadata = self.maker.getMetaData()
    # config
        self.tableName['dkb'] = 'DKBTable'
        self.tableName['class'] = 'Class'
        self.tableName['cath'] = 'Cath'
        self.tableName['meta'] = 'Meta-Table'
    
    # ------------------------------------------------------------------------------
    # user inner functions        
    def importDKBDF(self, df):
        '''
        imports pandas DF into SQL table 'dkb'
        '''
        if df is None:
            print('# importDKBDF: No data Frame received #')
        self.tableName['dkb'] = 'DKBTable'
        if DEBUGLEVEL > 1: print(f"# importDKBDF: db-Table-Name: {self.tableName['dkb']}")
        try:
            
            self.meta = self.maker.getMetaData()
            df.to_sql(  self.tableName['dkb'],          # table name
                        con=self.engine,                # connection
                        if_exists='append',             # what to do if table already exists ('fail', 'replace, 'append' are the options)
                        index=False,                    # use csv column as index
                        chunksize=100,                  # how many rows to be copied at once
                        # dtype={
                        #     "date":Date
                        # }
                    )
        except:
            print('ORM: CSV import to DB failed')
            return False
        
        return True

    def createDkbMetaTable(self):
        self.meta_table = Table(self.tableName['meta'], self.metadata, 
            Column('start-date', String, nullable=False),
            Column('end-date', String, nullable=False),
            Column('konto', String, nullable=False),
            # ForeignKey('users.id')
            extend_existing=True,
        )

    def createClassTable(self):
        self.tableName['class'] = 'ClassTable'
        self.class_table = Table(self.tableName['class'], self.metadata, 
            Column('INOUT', String, nullable=False),
            Column('class', String, nullable=False),
            Column('fix', String, nullable=False),
            Column('konto', String, nullable=False),
            # Column('last_updated', DateTime, onupdate=datetime.datetime.now)
            extend_existing=True,
        )
        self.class_table.create(self.engine)
    
    def createCathTable(self):
        self.tableName['cath'] = 'CathTable'
        self.cath_table = Table(self.tableName['cath'], self.metadata, 
            Column('type', String, nullable=False),
            Column('cycle', Integer, nullable=False),
            extend_existing=True,
        )
        self.cath_table.create(self.engine)
    
    def createTables(self):
        self.metadata.create_all(self.engine)
    
    def updateEngine(self):
        # to be used, if any changes were by done on the DB outside of this handler
        self.engine = self.maker.createEngine()     # create new engine to reload
        self.meta = self.maker.getMetaData()

    def _check_column_exists(self, column):
        dkb_table = Table(self.tableName['dkb'], self.meta, autoload=True, autoload_with=self.engine)
        if column in dkb_table.columns: return True

    def addClassColumn(self):        
        column = 'Class'
        if self._check_column_exists(column): return
        tableName = self.tableName['dkb']
        foreignTable = self.tableName['class']
        create_new_column = f"""ALTER TABLE {tableName} 
                                    ADD COLUMN {column} FOREIGN_KEY {foreignTable} id;"""
        with self.engine.connect() as conn:
            conn.execute(text(create_new_column))
            
    def addCathColumn(self):
            column = 'Cath'
            if self._check_column_exists(column): return
            tableName = self.tableName['dkb']
            
            foreignTable = self.tableName['cath']
            create_new_column = f"""ALTER TABLE {tableName} 
                                        ADD COLUMN {column} FOREIGN_KEY {foreignTable} id;"""
            with self.engine.connect() as conn:
                conn.execute(text(create_new_column))

    def addCathColumnPure(self):
        db_pure_handler=DB_Pure_SqlLiteHandler(self.__path, self.__name)
        db_pure_handler.addColumn(  tableName=self.tableName['dkb'], 
                                    foreignTable=self.tableName['cath'], 
                                    column='Cath')
    
    def addClassColumnPure(self):
        db_pure_handler=DB_Pure_SqlLiteHandler(self.__path, self.__name)
        db_pure_handler.addColumn(  tableName=self.tableName['dkb'], 
                                    foreignTable=self.tableName['class'], 
                                    column='Class')

    # ------------------------------------------------------------------------------
    # busyness functions 
    def addNewClass(self, class_data):
        self.engine = self._createEngine()
        if len(class_data) != 4:
            if DEBUGLEVEL > 1: print(f"Number of values not equal to number of columns")
            return False
        ins = self.class_table.insert().values(class_data)
        self.engine.execute(ins)
    
    def addNewCath(self, cath_data):
        if len(cath_data) != 2:
            if DEBUGLEVEL > 1: print(f"Number of values not equal to number of columns")
            return False
        ins = self.cath_table.insert().values(cath_data)
        self.engine.execute(ins)
    
    # ------------------------------------------------------------------------------
    # untested functions 
    def getMonth(self, year, month):
        if 'Jan' in month:
            if DEBUGLEVEL > 0: print(f'Getting {month} from DB')
            month = '01'

        # get table from the data base: https://docs.sqlalchemy.org/en/13/core/reflection.html?highlight=table+reflection#overriding-reflected-columns
        dkb_table = Table(self.tableName['dkb'], self.meta, autoload=True, autoload_with=self.engine)
        
        selection = select([(dkb_table.c.date + ", " + \
                            dkb_table.c.text + ", " +   \
                            dkb_table.c.verwendung + ", " + \
                            dkb_table.c.value)]).where(
                                dkb_table.c.date.like(f'{year}-{month}-%')
                                # dkb_table.c.booking-date.like(f'{year}-{month}-%')
                            )
        with self.engine.connect() as conn:  
            selected_data=conn.execute(selection).fetchall()
        return selected_data

    def getClass(self):
        dkb_table = self.metadata(self.tableName['dkb'])
        stm = select([dkb_table.c.Class])
        classes = self.engine.execute(stm).fetchall()
        
        s = select([self.class_table])
        classes = self.engine.execute(s)
        return classes
    
class DB_Pure_SqlLiteHandler(object):
    def __init__(self, pth, db_name):
        self.__path = pth
        self.__name = db_name
    # sql 
        pth = str(self.__path / self.__name) + '.db'
        self.__conn = sql.connect(pth)
        self.__curs = self.__conn.cursor()  
    

    def addColumn(self, tableName = '', foreignTable='', column='unnamed'):
        '''
        Adds a column to the table
        '''        
        # if self._checkColumnExists(self.tableName['dkb'], column):
        #     return True
        if tableName == '': return False
        if foreignTable != '':
            create_new_column = f"""ALTER TABLE {tableName} 
                                    ADD COLUMN {column} FOREIGN_KEY {foreignTable} id;"""
        try:
            self.__curs = self.__conn.cursor()
            self.__curs.execute(create_new_column)
            return True
        except ValueError as e:
            if DEBUGLEVEL: print('DB could not be created')
            ValueError(e)
            return False
        
    def _checkColumnExists(self, table, column):
        try:
            selCol = f"""SELECT {column} FROM {table};"""
            self.__curs.execute(selCol)
            if INFO: print (f'** Column {column} EXISTS')
            return True
        except:
            if INFO: print (f'** Column {column} is not there')
            return False

    def getMonth(self, tableName, month): # not tested
        if 'Jan' in month:
            if DEBUGLEVEL > 0: print(f'Getting {month} from DB')
            request = f"""SELECT verwendung FROM {tableName} WHERE date:2015-01 """
            
            with self.engine.connect() as conn:
                result = conn.execute(text(request))
                for date in result:
                    if '' in date.date:
                        print('Januar')
                        
# class DB_Queries(object):
#     def __init__(self, engine):
#         self.engine = engine          
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()

#     def getMonth(self, year, month, tableName):
#         dkb_table = Table(tableName, self.meta, autoload=True, autoload_with=self.engine)


#     def queryDate(self):
#         dkb_query = self.session.query(DKB_Table)
#         instance = dkb_query.first()
#         dkb_query.filter(DKB_Table.name == '2022-01')
