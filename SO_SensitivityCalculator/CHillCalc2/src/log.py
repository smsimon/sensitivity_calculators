#python Version 2.7.2

class Log:
    def __init__(self, logFile, verbose=1):
        self.__logFile = logFile
        self.__f = open(self.__logFile, 'w')
        if verbose > 2: self.__verbose = 2
        if verbose < 0: self.__verbose = 0
        else:           self.__verbose = verbose
    
    def log(self, msg, importance=None):
        if not importance: importance = self.__verbose
        self.__f.write(msg+'\n')
        if importance <= self.__verbose: print msg
    
        
        
