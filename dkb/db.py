'''
Created on 22.06.2021

@author: wakl8754
'''

from ast import Str
from cmath import e
import logging
from pathlib import Path
import sqlite3 as sql # con = sqlite3.connect('example.db')
from sqlite3 import Error


DEBUG = True
INFO = False

logging.basicConfig(level=logging.INFO, format='(%asctime%)s:%(message)s)', filename='builder.log' )

class DB(object):
    __path = None   # file path of DB
    __name = None   # DB name
    __type = None   # DB type
    __conn = None   # connection to DB
    __curs = None   # cursor in DB
    __ram = False   # option parameter to create DB in RAM only
    __tab = None    # current table name

    # initiaization
    def __init__(self, pth, db_name, db_type):
        self.setPath(pth)
        self.setDbName(db_name)
        self.setDbType(db_type)

# organization
#------------------------------------------------------------------------------ 
    def setPath(self, sPath) -> None:
        self.__path = sPath    
    def setDbName(self, nm) -> None:
        self.__name = nm      
    def setDbType(self, tp) -> None:
        ''' 'sqlite3' is supported '''
        self.__type = tp    # e.g.'sqlite3'  
    def setTableName(self, nm) -> None:
        self.__tab = nm
    def getTableName(self) -> Str:
        return self.__tab
    def getDbPath(self) -> Path:
        return self.__path + self.__name + '.db'
    def setOptions(self, opt) -> None:
        '''
        opt = {'ram':True/False}
        '''
        if 'ram' in opt:
            self.__ram = opt['ram']
        else:
            if INFO: print('DB store options not provided')
            logging.debug('DB.setOptions: DB store options not provided')
    
    def _createConnection(self):
        ''' creates DB connection '''
        if self.__type == 'sqlite3':
            pth = str(self.__path / self.__name) + '.db'
        else:
            print('DB type not supported')
            return None

        try:
            if self.__ram:
                self.__conn = sql.connect(":memory:")
                logging.debug('DB in RAM was created')
            else:
                self.__conn = sql.connect(pth)
                logging.debug(f'Connected to DB:  {pth}')
            self.__curs = self.__conn.cursor()
            return True
        except Error as e:
            if DEBUG: print('DB could not be created')
            print(e)
            return False
    
    def createNewTable(self, name):
        create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
        self.__curs.execute(create_table_sql)

    def createTable(self, name):
        self._createConnection()
        sql =  f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id integer PRIMARY KEY,
                    standard_type text,
                    class text,
                    direction text
                );"""
        self.__curs.execute(sql)

    def createDKBTable(self, name):
        self._createConnection()
        sql =  f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    date
                    booking-date
                    booking-text text,
                    debitor text,
                    verwendung text,
                    konto text,
                    blz text,
                    value integer,
                    debitor-id integer,
                    Mandat-reference text,
                    Customer-reference text
                );"""
        self.__curs.execute(sql)
# busyness
#------------------------------------------------------------------------------ 
    def importNewData(self, df):
        '''
        https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        @data in DataFrame
        '''
        
        if self.__tab is not None:
            try:
                df.to_sql(self.__tab,           # table name
                            self.__conn,        # connection
                            if_exists='append', # what to do if table already exists ('fail', 'replace, 'append' are the options)
                            index=False,        # use csv column as index
                            chunksize=100)      # how many rows to be copied at once
                return True
            except:
                print('CSV import to DB failed')
                return False
        else:
            if DEBUG: print('# DB.impotrNewData # No table selected to write')
            return False   
    
# finalization
#------------------------------------------------------------------------------ 
    def close(self): 
        self.__conn.close()

    def save(self): 
        self.__conn.commit()
        logging.debug('Changes committed to DB')
        

class SQLDB(object):
    '''
    Class to create and handle sqlite 3 DB
    https://www.sqlitetutorial.net/
    '''
    
    def __init__(self, db_file):
        ''' db_file is a string path (type Path)'''
        if True:
            self._create(db_file)
        else:
            pass

    def _create(self, db_file) -> None: 
        try:
            self.__con = sql.connect(db_file)   # create connection to db, means creates new db
        except Error as e:
            print(e)
        finally:
            if self.__con:
                self.__con.close

