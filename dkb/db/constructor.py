''' The module is required to be imported to have 
a use of the same Base instance '''
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker()

# pylint: disable=too-few-public-methods
class DbConstructor():
    ''' class to provide instances of Base and Session'''
    def __init__(self):
        # pylint: disable=invalid-name
        self.Base = declarative_base()
        self.Session = sessionmaker()
        # self.Session.close_all()
        # self.dkb_engine = create_engine('sqlite:///' + str(pth), echo=True)
        # self.dkb_session = sessionmaker(bind=self.dkb_engine)
        
    