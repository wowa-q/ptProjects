from abc import ABC, ABCMeta, abstractmethod
import hashlib
import zipfile 
import shutil
import os
from dkb.cfg import ResponseCode as RC
from dkb.cfg import Project as pj



# make use of a command pattern: https://refactoring.guru/design-patterns/command/python/example
class Command(ABC):
    ''' abstract class to alighn different commands '''
    __metaclass__ = ABCMeta

    # to run standard commands
    @abstractmethod
    def execute(self) -> None: pass
# ----------------------------------------------------------------
# ------------------- DB interaction -----------------------------
# ----------------------------------------------------------------
class CmdCreateNewDB(Command):  # ready to test
    ''' Command class to create new DB '''
    def __init__(self, db_handler, db_file):
        self.db_handler = db_handler
        self.db_file = db_file

    def execute(self) -> None:
        ''' creates new db with empty tables '''
        self.db_handler.create_db(self.db_file)
        self.db_handler.close()

class CmdImportNewCsv(Command):
    def __init__(self, db_handler, dkb_ld, csv_file):
        self.dkb_ld = dkb_ld
        self.db_handler = db_handler
        self.csv_file = csv_file

    def set_new_csv(self, csv_file):
        self.csv_file = csv_file
               
    def execute(self) -> None:
        print(' # start execution *CmdImportNewCsv* # ')
        csv_meta = {}
        print(f'CmdImportNewCsv: {self.csv_file}')
        
        with open(self.csv_file, 'rb') as file:
            # calculate first the checksum of the given csv file
            checksum =  hashlib.md5(file.read()).hexdigest().upper()

        # search the checksum in the meta table
        (rc, lresults) = self.db_handler.find_checksum(checksum)
        # check the response code
        if rc == RC.META_TABLE_NOK:
            return RC.NOK
        elif rc == RC.META_TABLE_OK:
            if len(lresults) > 0:
                # an entry was found in the meta table -> csv is already imported
                print('CmdImportNewCsv: CSV already imported')
                print(lresults)
                return RC.NONE
            else: 
                # no entry was found -> import can be continued
                # 1. get data for meta entry
                with open(self.csv_file, 'r') as file:
                    for row in file:
                        print(row.split(';'))
                        # Konto is in the first row
                        csv_meta['konto'] = row.split(';')[1]
                        break
                csv_meta['name'] = self.csv_file
                csv_meta['checksum'] = checksum                
                
                # 2. import csv data
                (rc, csv_ln) = self.dkb_ld.get_lines_as_list_of_dicts(self.csv_file)
                self.db_handler.import_dkb_csv(csv_ln, csv_meta)
                # 3. create meta entry
                self.db_handler.create_csv_meta(csv_meta)
                return RC.OK

class CmdArchiveCsv(Command):
    def __init__(self, csv_file, zip_file):
        self.csv_file = csv_file
        # self.base_dir = base_dir
        self.zip_file = zip_file


    def execute(self) -> None:
        
        with zipfile.ZipFile(self.zip_file, 'w', compression=zipfile.ZIP_DEFLATED) as newzip:
            newzip.write(self.csv_file)
        self.csv_file.unlink()
        # if not self.zip_file.exists():
        #     # create new zip file
        #     zip_file = ZipFile(self.zip_file, 'w')
        #     zip_file.write(self.csv_file)
        #     zip_file.close()

        #     # create first the new zip file
        #     _, csv_archive = os.path.split(self.zip_file)
        #     src, _ = os.path.split(self.csv_file)
        #     base_name = csv_archive.strip('.zip')
        #     shutil.make_archive(base_name, 'zip', base_dir=src)
        # else:
        #     with ZipFile(self.zip_file, 'w') as newzip:
        #         newzip.write(self.csv_file)

        # put new csv file into zip_file
        
        # try:
        #     if self.csv_file.exists():
                
        #         base_dir, _ = os.path.split(self.csv_file)
        #         base_dir = pj.PROJEC_DIRECTORY_PATH
        #         shutil.make_archive('csv_archive', 'zip', base_dir=base_dir)
        #         # self.csv_file.unlink()
        #         return RC.OK
        #     else:
        #         return RC.NONE
        # except FileNotFoundError:
        #     return RC.NOK
# ----------------------------------------------------------------
# ------------------ User interactions ---------------------------
# ----------------------------------------------------------------
class CmdNewMonth(Command): # TODO: Receiver class to be enhanced
    ''' Concrete commands for the Database'''
    def __init__(self, db_handler, writer, year, month):
        self.db_handler = db_handler
        self.writer = writer
        self.year = year
        self.month = month

    def execute(self) -> None:
        print('# CmdNewMonth #')
        (rc, data) = self.db_handler.get_month(self.year, self.month) # TODO: Receiver class to be enhanced
        if rc == RC.OK:
            sheet = self.writer.create_new_sheet(self.month, after='title')
            self.writer.write_month(sheet, data)
        self.db_handler.close()

# ----------------------------------------------------------------
# ------------------ Invoker implementation ----------------------
# ----------------------------------------------------------------
class Invoker(object):
    ''' The Invoker is associated with one or several commands. It sends a request
    to the command. '''
    def __init__(self) -> None:    
        self._on_start = None
        self._main_command = None
        self._on_finish = None

    """
    Initialize commands.
    """
    def set_on_start(self, command: Command):
        self._on_start = command

    def set_main_command(self, command: Command):
        self._main_command = command

    def set_on_finish(self, command: Command):
        self._on_finish = command
    
    def run_commands(self) -> None:
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        if isinstance(self._on_start, Command):
            self._on_start.execute()
        
        if isinstance(self._main_command, Command):
            self._main_command.execute()
        
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()        