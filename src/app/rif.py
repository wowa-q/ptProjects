'''
Created on 29.04.2016

@author: wakl8754
'''
#from abc import ABCMeta, abstractmethod, abstractproperty
from abc import ABC, abstractmethod, abstractproperty

class RIF(ABC):
    '''
    belongs to the observer and must be implemented by each rule
    '''
    __metaclass_ = ABC
    
    #===========================================================================
    # must be implemented methods
    #===========================================================================
    
    @abstractmethod
    def verify(self): pass
     
    #===========================================================================
    # must be implemented properties
    #===========================================================================
    @abstractproperty
    def result(self): pass      # Failed or passed
    
    