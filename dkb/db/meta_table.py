from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, DateTime
from datetime import datetime
from dkb.db.constructor import Base
from dkb.cfg import ResponseCode as RC

class CSV_Meta(Base):
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

class CSV_Table_Handler(object):
    
    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine

    def add(self, ln_dict):        
        date = None
        # konto = str(ln_dict['name']).strip(".csv")[-10:]
        konto = ln_dict['konto']
        name = str(ln_dict['name']) #[-14:]
        checksum = ln_dict['checksum']
        date = ln_dict.get('date')
        new = CSV_Meta(name, date, konto, checksum)
        self.session.add(new)
        self.session.commit()
        return RC.META_TABLE_OK

    def find_checksum(self, checksum):
        print(f"searching checksum: {checksum}")
        try:
            results = self.session.query(CSV_Meta.name,
                                        CSV_Meta.id,
                                        CSV_Meta.date,
                                        CSV_Meta.konto,
                                        CSV_Meta.checksum                                        
                                        ).filter(CSV_Meta.checksum == checksum)
            lres = []
            for result in results:
                print(result)
                lres.append(result)
            return (RC.META_TABLE_OK, lres)
        except:
            return (RC.META_TABLE_NOK, [])