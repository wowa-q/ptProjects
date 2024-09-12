'''
Interface to db table CsvMeta
'''
# standard library
from datetime import datetime
# 3rd party
from sqlalchemy import Column, String, Integer, DateTime
#from sqlalchemy import ForeignKey, CHAR

# user packages
from dkb.db.constructor import Base
from dkb.cfg import ResponseCode as RC

# pylint: disable=too-few-public-methods
class CsvMeta(Base):
    ''' class to build a table in the data base '''
    __tablename__ = "csv-meta"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    date = Column("date", DateTime(), default = datetime.utcnow)
    konto = Column("konto", String)
    checksum = Column("checksum", String, unique=True)

    def __init__(self, name, date, konto, checksum) -> None:
        self.date = date
        self.name = name
        self.konto = konto
        self.checksum = checksum

    def __repr__(self) -> str:
        return f"CSV: {self.name}"

# pylint: disable=too-few-public-methods
class CsvMetaTableHandler():
    ''' class providing methods to work with the table from data base '''
    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine

    def add(self, ln_dict):
        ''' method to add new entry in the table '''   
        date = None
        # konto = str(ln_dict['name']).strip(".csv")[-10:]
        konto = ln_dict['konto']
        name = str(ln_dict['name']) #[-14:]
        checksum = ln_dict['checksum']
        date = ln_dict.get('date')
        new = CsvMeta(name, date, konto, checksum)
        self.session.add(new)
        self.session.commit()
        return RC.META_TABLE_OK

    def find_checksum(self, checksum):
        ''' searching checksum in the table '''
        print(f"searching checksum: {checksum}")
        try:
            results = self.session.query(CsvMeta.name,
                                        CsvMeta.id,
                                        CsvMeta.date,
                                        CsvMeta.konto,
                                        CsvMeta.checksum                                        
                                        ).filter(CsvMeta.checksum == checksum)
            lres = []
            for result in results:
                print(result)
                lres.append(result)
            return (RC.META_TABLE_OK, lres)
        except:
            return (RC.META_TABLE_NOK, [])