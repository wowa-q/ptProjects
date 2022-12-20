''' global configuration of the App '''
import pathlib
import os 
from enum import Enum



class Project(Enum):
    '''
    https://docs.python.org/3/library/enum.html
    Project.WORKING_DIRECTORY_PATH
    file_path = Project.PROJEC_DIRECTORY_PATH / 'datei.txt'
    with file_path.open('a') as file:
        file.write('bla bla')
    '''
    # calculates the path of parent directory for this file
    # resolve is good pattern to remove signs from the path like "..."
    PROJEC_DIRECTORY_PATH = pathlib.Path(__file__).parent.resolve()
    # calculates the current working directory - where was the programm executed
    WORKING_DIRECTORY_PATH = os.getcwd()
    # headers to map
    CSV_HEADER = [
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
    # CSV Line number with the header
    CSV_HEADER_LINE = 6
    
    # def __str__(self):
    #     return f'{self.name} \n project directory: {self.PROJEC_DIRECTORY_PATH} \n \
    #             current working directory: {self.WORKING_DIRECTORY_PATH}'

class ResponseCode(Enum):
    ''' setting global return codes '''
    # Generic Response codes
    OK = 1
    NOK = 0
    NONE = 2   # if no operation to be done, but no error
    # Meta Table response codes
    META_TABLE_OK = 1
    META_TABLE_NOK = 0
    # DKB Table response codes
    DKB_TABLE_OK = 1
    DKB_TABLE_NOK = 0
    # Class Table response codes
    CLASSES_TABLE_OK = 1
    CLASSES_TABLE_NOK = 0
    # Category Table response codes
    CAT_TABLE_OK = 1
    CAT_TABLE_NOK = 0



if __name__ == '__main__':
    print(Project.PROJEC_DIRECTORY_PATH.value)
    print(Project.WORKING_DIRECTORY_PATH.value)
