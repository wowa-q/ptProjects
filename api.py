from abc import ABC, ABCMeta, abstractmethod
from logging import raiseExceptions
from pathlib import Path
import argparse

# user packages:
from dkb.dkb import DKB
import dkb.orm as orm
from dkb.exc import ExcelWriter 

# make use of a command pattern: https://refactoring.guru/design-patterns/command/python/example
class Command(ABC):
    ''' abstract class to alighn different commands '''
    __metaclass__ = ABCMeta

    # to run standard commands
    @abstractmethod
    def execute(self) -> None: pass

class CmdNewMonth(Command): # TODO: Receiver class to be enhanced
    ''' Concrete commands for the Database'''
    def __init__(self, dkb_ld, orm, writer, year, month):
        #self.dkb_ld = dkb_ld
        self.orm = orm
        self.writer = writer
        self.year = year
        self.month = month

    def execute(self) -> None:
        self.orm.get_month(self.year, self.month) # TODO: Receiver class to be enhanced
        self.writer.create_new_sheet(self.month, after='title')
        # self.writer.useDataToImport # TODO: Receiver class to be enhanced

class CmdUpdateDbTable(Command):    # TODO: Receiver class to be enhanced
    ''' Concrete commands for the Database'''
    def __init__(self, dkb_ld, orm, writer):
        self.dkb_ld = dkb_ld
        self.orm = orm
        self.writer = writer

    def execute(self) -> None:
        pass

class CmdImportNewCsv(Command): # TODO: Receiver class to be enhanced
    def __init__(self, dkb_ld, orm, csv_file):
        self.dkb_ld = dkb_ld
        self.orm = orm
        self.csv_file = csv_file
    
    def execute(self) -> None:
        df = self.dkb_ld.get_dkb_df(self.csv_file)
        self.orm.import_dkb_df(df)

class CmdCreateNewDB(Command):  # ready to test
    ''' Command class to create new DB '''
    def __init__(self, dkb_ld, orm, csv_file):
        self.dkb_ld = dkb_ld
        self.o = orm
        self.csv_file = csv_file

    def execute(self) -> None:         
        csv_df = self.dkb_ld.get_dkb_df_from_folder(self.csv_file)        
        # self.o.createClassTable()
        # self.o.createDkbMetaTable()
        # self.o.createCathTable()
        self.o.create_class_table()
        self.o.create_dkb_meta_table()
        self.o.create_cath_table()
        # self.o.createTables() # not needed anymore
        self.o.import_dkb_df(csv_df)
        # self.o.addClassColumn()
        # self.o.addCathColumn()
        # self.o.updateEngine()
        self.o.add_class_column()
        self.o.add_cath_column()
        self.o.update_engine()

class CmdCheckFileSystem(Command):
    def __init__(self, receiver=None):
        self.receiver = receiver

    def execute(self) -> None:
        if self.receiver is None:
            print('Nothing to be done here')
        elif isinstance(self.receiver, Path):
            if self.receiver.exists() == True:
                raise ValueError('The file exists allready')

class Invoker(object):
    ''' The Invoker is associated with one or several commands. It sends a request
    to the command. '''
    _on_start = None
    _main_command = None
    _on_finish = None

    """
    Initialize commands.
    """
    def set_on_start(self, command: Command):
        self._on_start = command

    def set_main_command(self, command: Command):
        self._main_command = command

    def set_on_finish(self, command: Command):
        self._on_finish = command
    
    # busyness methods
    def run_commands(self) -> None:
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        print("Invoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")
        if isinstance(self._main_command, Command):
            self._main_command.execute()

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()