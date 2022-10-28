from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path

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
    def __init__(self, dkb_ld, orm, writer, month):
        self.dkb_ld = dkb_ld
        self.orm = orm
        self.writer = writer
        self.month = month

    def execute(self) -> None:
        self.orm.getMonth(self.month)
        self.writer.createSheet(self.month, after='title')
        self.writer.useDataToImport # TODO: Receiver class to be enhanced

class CmdUpdateDbTable(Command):    # TODO: Receiver class to be enhanced
    ''' Concrete commands for the Database'''
    def __init__(self, dkb_ld, orm, writer):
        self.dkb_ld = dkb_ld
        self.orm = orm
        self.writer = writer

    def execute(self) -> None:
        pass

class CmdImportNewCsv(Command): # TODO: Receiver class to be enhanced
    def __init__(self, dkb_ld, orm):
        self.dkb_ld = dkb_ld
        self.orm = orm
    
    def execute(self) -> None:
        self.dkb_ld.parseDkbData()

class CmdCreateNewDB(Command):  # ready to test
    ''' Command class to create new DB '''
    def __init__(self, dkb_ld, orm):
        self.dkb_ld = dkb_ld
        self.o = orm

    def execute(self) -> None:         
        csv_df = self.dkb_ld.parseDkbData()        
        self.o.createClassTable()
        self.o.createDkbMetaTable()
        self.o.createCathTable()
        self.o.createTables()
        self.o.importDKBDF(csv_df)
        self.o.addClassColumn()
        self.o.addCathColumn()

class CmdCheckFileSystem(Command):
    def _init(self, receiver=None):
        self.receiver = receiver

    def execute(self) -> None:
        if self.receiver is None:
            print('Nothing to be done here')

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

if __name__ == "__main__":
    """
    The client code can parameterize an invoker with any commands.
    """
    # Create Receiver objects    
    pth = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    db_file = Path('D:/005-pj/ptpj/dkb/ptProjects/test/fixtures')
    xls_file=r"d:\005-pj\ptPj\dkb\ptProjects\test\fixtures\haushalt.xlsm"
    db_name = 'new_db'
    dkb_ld = DKB(pth)    
    orm = orm.DB_Handler(db_file, db_name, 'sqlite3')   
    writer = ExcelWriter(xls_file)

    # Parametrize the Invoker and execute the command
    invoker = Invoker()
    invoker.set_on_start(CmdCheckFileSystem(None))
    invoker.set_main_command(CmdCreateNewDB(dkb_ld, orm))
    invoker.run_commands()
    