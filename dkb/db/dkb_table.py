from sqlalchemy import ForeignKey, Column, String, Integer, Float

from dkb.db.constructor import Base
from dkb.cfg import ResponseCode as RC

class DKB_Table(Base):
    __tablename__ = "dkb-table"
    # Columns erstellen
    __header = [
                'date',
                'booking-date',
                'text',
                'debitor',
                'verwendung',
                'konto',
                'blz',
                'value',
                'debitor-id',
                'Mandats reference',
                'Customer reference']
    id              = Column("id", Integer, primary_key=True)
    date            = Column("date", String)
    booking_date    = Column("booking-date", String)
    text            = Column("text", String)
    debitor         = Column("debitor", String)
    verwendung      = Column("verwendung", String)
    konto           = Column("konto", String)
    blz             = Column("blz", String)
    value           = Column("value", Float)
    debitor_id      = Column("debitor-id", String)
    mandats_ref     = Column("Mandats reference", String)
    customer_ref    = Column("Customer reference", String)
    checksum        = Column("checksum", String, unique=True)
    classes         = Column("classes", String, ForeignKey("classes.id"))
    category        = Column("category", String, ForeignKey("category.id"))

    # def __init__(self, name, date, konto, checksum) -> None:
    #     self.name = name
    #     self.date = date
    #     self.konto = konto
    #     self.checksum = checksum

    def __repr__(self) -> str:
        return f"{self.id} - {self.date} - {self.konto} - {self.value} - {self.checksum}"

class DKB_Table_Handler(object):

    def __init__(self, sessionmaker, engine) -> None:
        self.session = sessionmaker()
        self.engine = engine
# ----------------------------------------------------------------
# ------------------ Update Table data -------------------------------
# ----------------------------------------------------------------    
    def add(self, ln_as_dict):
        (rc, lresults) = self._find_checksum(ln_as_dict["checksum"])
        if rc == RC.DKB_TABLE_NOK:
            # reading DKB table not possible
            return RC.DKB_TABLE_NOK
        elif rc == RC.DKB_TABLE_OK:
            if len(lresults) > 0:
                # an entry was found in the meta table -> line was already imported
                print('DKB-Table-Handler: Transaction already imported')
                print(lresults)
            else: 
                new_dkb_line = DKB_Table(
                    date            = ln_as_dict['date'],            
                    booking_date    = ln_as_dict["booking-date"],
                    text            = ln_as_dict["text"],
                    debitor         = ln_as_dict["debitor"],
                    verwendung      = ln_as_dict["verwendung"],
                    konto           = ln_as_dict["konto"],
                    blz             = ln_as_dict["blz"],
                    value           = ln_as_dict["value"],                    
                    debitor_id      = ln_as_dict["debitor-id"],
                    checksum        = ln_as_dict["checksum"],
                    mandats_ref     = ln_as_dict["mandats_ref"],
                    customer_ref    = ln_as_dict["customer_ref"],
                )
                print(ln_as_dict["verwendung"], ln_as_dict["value"])
                self.session.add(new_dkb_line)
                self.session.commit()
                return RC.DKB_TABLE_OK    

    def import_pure_csv(self, csv_lines_as_dict, csv_meta):      
        # TODO update Meta table currently done by user  
        for ln_as_dict in csv_lines_as_dict:
            self.add(ln_as_dict)        

    def _find_checksum(self, checksum):
        try:
            results = self.session.query(DKB_Table).filter(DKB_Table.checksum == checksum)
            lres = []
            for result in results:
                print(result)
                lres.append(result)
            return (RC.DKB_TABLE_OK, lres)
        except:
            return (RC.DKB_TABLE_NOK, [])

# ----------------------------------------------------------------
# ------------------ Retrieve Table data -------------------------
# ----------------------------------------------------------------
    def get_month(self, year, month):
        '''
        year: 2016
        month: 01 January
        '''
        try:            
            results = self.session.query(DKB_Table.checksum,
                                        DKB_Table.date, 
                                        DKB_Table.debitor, 
                                        DKB_Table.text, 
                                        DKB_Table.verwendung, 
                                        DKB_Table.value,
                                        DKB_Table.classes,
                                        DKB_Table.category
                                        ).filter(DKB_Table.date.like(f'%{month}.{year}%')).all()
            header = ('checksum', 
                    'Datum', 
                    'Debitor', 
                    'Buchungstext', 
                    'Verwendung',
                    'Betrag',
                    'Klasse',
                    'Typ'
                    )
            lres = []
            for result in results:                
                lres.append(result)
                print(lres)
            print (f'# get_month: {RC.DKB_TABLE_OK}')
            return (RC.DKB_TABLE_OK, lres, header)
        except:
            print (f'# get_month: {RC.DKB_TABLE_NOK}')
            return (RC.DKB_TABLE_NOK, [])
    
    def get_class(self, dkb_class):
        result = self.session.query(DKB_Table).filter(DKB_Table.classes == dkb_class).all() 
        return result