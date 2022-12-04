from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker()

class DB_Constructor():
    def __init__(self, pth):
        self.Base = declarative_base()
        self.Session = sessionmaker()
        # self.Session.close_all()
        # self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        # self.dkb_session = sessionmaker(bind=self.dkb_engine)
        
    