from email.errors import NonPrintableDefect
import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey


DEBUGLEVEL = 1
INFO = False


class DB_Handler(object):
    
    # initiaization
    def __init__(self, pth, db_name, db_type):
        self.__path = pth
        self.__name = db_name
        self.__type = db_type       
        self.engine = self._createEngine()
        self.tableName = {}
    # organization
    #------------------------------------------------------------------------------ 
    def _createEngine(self):
        engine = None
        if self.__type == "sqlite3":
            db_pth = str(self.__path) + "/" + self.__name + '.db'
            engine = create_engine("sqlite:///"+db_pth, echo=INFO)
            logging.debug(f'Engine for DB created at:  {db_pth}')
            if DEBUGLEVEL > 0: print(f"# createEngine: db-Name: {db_pth}")
        return engine

    def createDkbMetaTable(self):
        self.tableName['meta'] = 'Meta-Table'
        metadata = MetaData()
        dkb_table = Table(self.tableName['meta'], metadata, 
            Column('start-date', String, nullable=False),
            Column('end-date', String, nullable=False),
            Column('konto', String, nullable=False),
            # ForeignKey('users.id')
        )
    
    def importDKBDF(self, df):
        if df is None:
            print('# importDKBDF: No data Frame received #')
        self.tableName['dkb'] = 'DKB-Table'
        if DEBUGLEVEL > 1: print(f"# importDKBDF: db-Table-Name: {self.tableName['dkb']}")
        try:
            df.to_sql(  self.tableName['dkb'],          # table name
                        con=self.engine,                # connection
                        if_exists='append',             # what to do if table already exists ('fail', 'replace, 'append' are the options)
                        index=False,                    # use csv column as index
                        chunksize=100)                  # how many rows to be copied at once
        except:
            print('ORM: CSV import to DB failed')
            return False
        return True