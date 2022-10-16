
import logging
import datetime
import sqlite3 as sql
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select


DEBUGLEVEL = 1
INFO = True


class DB_Handler(object):
    
    # initiaization
    def __init__(self, pth, db_name, db_type):
        self.__path = pth
        self.__name = db_name
        self.__type = db_type   
    # Alchemy    
        self.engine = self._createEngine()
        self.metadata = MetaData()
        self.tableName = {}
    # sql
        pth = str(self.__path / self.__name) + '.db'
        self.__conn = sql.connect(pth)
        self.__curs = self.__conn.cursor()
    
    # ------------------------------------------------------------------------------
    # helper functions
    def _createEngine(self):
        engine = None
        if self.__type == "sqlite3":
            db_pth = str(self.__path) + "/" + self.__name + '.db'
            # respect this: https://docs.sqlalchemy.org/en/14/core/pooling.html#pool-disconnects
            engine = create_engine("sqlite:///"+db_pth, pool_pre_ping=True, echo=INFO)
            logging.debug(f'Engine for DB created at:  {db_pth}')
            if DEBUGLEVEL > 0: print(f"# createEngine: db-Name: {db_pth}")
        return engine
    
    def _checkColumnExists(self, table, column):
        try:
            selCol = f"""SELECT {column} FROM {table};"""
            self.__curs.execute(selCol)
            if INFO: print (f'** Column {column} EXISTS')
            return True
        except:
            if INFO: print (f'** Column {column} is not there')
            return False
    
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
        self.tableName['meta'] = 'Meta-Table'
        self.meta_table = Table(self.tableName['meta'], self.metadata, 
            Column('start-date', String, nullable=False),
            Column('end-date', String, nullable=False),
            Column('konto', String, nullable=False),
            # ForeignKey('users.id')
        )

    def createClassTable(self):
        self.tableName['class'] = 'ClassTable'
        self.class_table = Table(self.tableName['class'], self.metadata, 
            Column('INOUT', String, nullable=False),
            Column('class', String, nullable=False),
            Column('fix', String, nullable=False),
            Column('konto', String, nullable=False),
            # Column('last_updated', DateTime, onupdate=datetime.datetime.now)
        )
    
    def createCathTable(self):
        self.tableName['cath'] = 'CathTable'
        self.cath_table = Table(self.tableName['cath'], self.metadata, 
            Column('type', String, nullable=False),
            Column('cycle', Integer, nullable=False),
        )
    
    def createTables(self):
        self.metadata.create_all(self.engine)
    
    def addClassColumn(self):
        '''
        Adds a column to the table
        '''        
        column = 'Class'
        if self._checkColumnExists(self.tableName['dkb'], column):
            return True
        create_new_column = f"""ALTER TABLE {self.tableName['dkb']} 
                                ADD COLUMN {column} FOREIGN_KEY {self.tableName['class']} id;"""
        try:
            self.__curs = self.__conn.cursor()
            self.__curs.execute(create_new_column)
            return True
        except ValueError as e:
            if DEBUGLEVEL: print('DB could not be created')
            ValueError(e)
            return False

    def addCathColumn(self):
        '''
        Adds a column to the table
        '''
        column = 'Cath'  
        if self._checkColumnExists(self.tableName['dkb'], column):
            return True    
        create_cath_column = f"""ALTER TABLE {self.tableName['dkb']} 
                                ADD COLUMN {column} FOREIGN_KEY {self.tableName['cath']} id;"""
        try:
            self.__curs = self.__conn.cursor()
            self.__curs.execute(create_cath_column)
            return True
        except ValueError as e:
            if DEBUGLEVEL: print('DB could not be created')
            ValueError(e)
            return False

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
    def getClass(self):
        s = select([self.class_table])
        classes = self.engine.execute(s)
        return classes
    
    
            

    