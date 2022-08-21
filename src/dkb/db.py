'''
Created on 22.06.2021

@author: wakl8754
'''

import logging
import sqlite3  # con = sqlite3.connect('example.db')


logging.basicConfig(level=logging.INFO, format='(%asctime%)s:%(message)s)', filename='builder.log' )

class DB(object):
    __path = None   # file path of DB
    __name = None   # DB name
    __conn = None   # connection to DB
    __curs = None   # cursor in DB
    __ram = False   # option parameter to create DB in RAM only
    __tab = None    # current table name

# organization
#------------------------------------------------------------------------------ 
    def setPath(self, sPath):
        self.__path = sPath    
    def setDbName(self, nm):
        self.__name = nm        
    def setTableName(self, nm):
        self.__tab = nm
    def getTableName(self):
        return self.__tab
    def getDbPath(self):
        return self.__path + self.__name + '.db'
    def setOptions(self, opt):
        '''
        opt = {'ram':True/False}
        '''
        if 'ram' in opt:
            self.__ram = opt['ram']
        else:
            print('DB store options not provided')
            logging.debug('DB store options not provided')
    
    def create(self):
        ''' creates DB connection '''
        try:
            if self.__ram:
                self.__conn = sqlite3.connect(":memory:")
                logging.debug('DB in RAM was created')
            else:
                pth = self.__path + self.__name + '.db'
                self.__conn = sqlite3.connect(pth)
                logging.debug(f'Connected to DB:  {pth}')
            self.__curs = self.__conn.cursor()
            return True
        except:
            print('DB could not be created')
            return False

# busyness
#------------------------------------------------------------------------------ 
    def importNewData(self, data):
        '''
        https://www.fullstackpython.com/blog/export-pandas-dataframes-sqlite-sqlalchemy.html
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        @data in DataFrame
        '''
        
        if self.__tab is not None:
            try:
                data.to_sql(self.__tab,         # table name
                            self.__conn,        # connection
                            if_exists='append', # what to do if table already exists ('fail', 'replace, 'append' are the options)
                            index=False,        # use csv column as index
                            chunksize=100)      # how many rows to be copied at once
                return True
            except:
                print('CSV import to DB failed')
                return False
        else:
            print('No table selected to write')
            return False   
    
# finalization
#------------------------------------------------------------------------------ 
    def close(self): 
        self.__conn.close()

    def save(self): 
        self.__conn.commit()
        logging.debug('Changes committed to DB')
        
