import logging
import logging.config
import inspect
import ConfigParser
import sys
import time

logFile = "logging.conf"
try:
    logging.config.fileConfig("logging.conf")
except:
    pass


simpleLogConfigCache = {}#Used to init a logger if there is no logger setting in the config file

logSys = logging

def openLogConfig(fileName):
    config = ConfigParser.RawConfigParser()
    try:
      config.read(fileName)
    except:
      pass
    return config


def loadLogConofig(fileName):
    global simpleLogConfigCache
    try:
      config = openLogConfig(fileName)
      loggerNames = getLoggerNames(config)
      for i in loggerNames:
          simpleLogConfigCache[i] = True
    except:
      pass
        
def getLoggerNames(config):
    try:
      keys = config.get('loggers', 'keys')
      loggerNames = keys.split(',')
      return loggerNames
    except:
      pass
      
def updateLogConfig(fileName, loggerName):
    config = openLogConfig(fileName)
    try:
		config.set('loggers', 'keys', config.get('loggers', 'keys')+','+loggerName)
		#print 'new logger names:',config.get('loggers', 'keys')
		config.add_section('logger_'+loggerName)
		config.set('logger_'+loggerName, 'handlers', 'consoleHandler')
		config.set('logger_'+loggerName, 'propagate', '0')
		config.set('logger_'+loggerName, 'level', 'ERROR')
		config.set('logger_'+loggerName, 'qualname', loggerName)
		configfile = open(fileName, 'wb')
		config.write(configfile)
    except:
		configfile = open(fileName, 'wb')
		try:
			config.add_section('loggers')
		except:
			pass
		config.set('loggers', 'keys', '')
		config.write(configfile)
      
loadLogConofig(logFile)

def printLog(*args):
    logStr = ''
    for i in args:
        logStr += str(i)
    logger.debug(logStr)


def pL(*args):
    logStr = ''
    for i in args[1:]:
        logStr += str(i)
    args[0].debug(logStr)


def smL(*args):
    logStr = ''
    for i in args[1:]:
        logStr += str(i)
    smartProxyLogger.error(logStr)

def whosdaddy():
    #print inspect.stack()
    return inspect.stack()[2][3]
def getFileLocation():
    #print inspect.stack()
    return str(inspect.stack()[2][1]) + ',' + str(inspect.stack()[2][2])
def changeEncoding(s):
    if type(s) == unicode:
        return s.encode('gbk', 'replace')
    if type(s) == str:
        return s.decode('gbk', 'replace').encode('gbk', 'replace')
    try:
        str(s)
    except:
        print type(s)
    return str(s)

class customLogSys:
    simpleLogConfigCache = {}
    handlerAdded = []
    def __init__(self):
        pass
    def getLogger(self, funcName):
        realLogger = logging.getLogger(funcName)
        if not (funcName in self.handlerAdded):
            self.handlerAdded.append(funcName)
            ch = logging.StreamHandler(sys.stderr)
            #create formatter
            #formatter = logging.Formatter("%(asctime)-15s %(message)s")
            formatter = logging.Formatter("%(message)s")
            #add formatter to ch and fh
            ch.setFormatter(formatter)
            #add ch to logger
            realLogger.addHandler(ch)
            realLogger.propagate = False
    
            if not self.simpleLogConfigCache.has_key(funcName):
                #The logger name does not exist in the config file
                ch.setLevel(logging.DEBUG)
                self.simpleLogConfigCache[funcName] = True
                updateLogConfig(logFile, funcName)
        return realLogger

def info(*args):
    logStr = ''
    for i in args:
        logStr += changeEncoding(i)+" "
    print logStr,
    
def ninfo(*args):
    pass
    
def cl(*args):
    p = whosdaddy()
    #print 'dady is',p
    realLogger = customLogSys().getLogger(p)
    '''
    realLogger = logging.getLogger(p)
    ch = logging.StreamHandler(sys.stderr)
    #create formatter
    formatter = logging.Formatter("%(asctime)-15s %(message)s")
    #add formatter to ch and fh
    ch.setFormatter(formatter)
    #add ch to logger
    realLogger.addHandler(ch)
    realLogger.propagate = False

    #print realLogger.findCaller()
    global simpleLogConfigCache
    #print >>sys.stderr, "in cl"
    if not simpleLogConfigCache.has_key(p):
        #The logger name does not exist in the config file
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.DEBUG)
        simpleLogConfigCache[p] = True
        updateLogConfig(logFile, p)
    '''
    #logStr = '------------------------\n'+str(time.time())+', '+p+', '+getFileLocation()+':\n'
    logStr = '------------------------\n'+p+', '+getFileLocation()+':\n'
    for i in args:
        logStr += changeEncoding(i)+" "
    #print 'calling debug'
    #logStr += '\n------------------------'
    #logStr += '\n'
    realLogger.error(logStr)
    #realLogger.removeHandler(ch)#Must remove the handler otherwise, the output will be produced multiple times
    
def ncl(*args):
    p = whosdaddy()
    #print 'dady is',p
    realLogger = customLogSys().getLogger(p)
    '''
    realLogger = logging.getLogger(p)
    #create formatter
    formatter = logging.Formatter("%(message)s")
    #add formatter to ch and fh
    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(formatter)
    #add ch to logger
    realLogger.addHandler(ch)
    realLogger.propagate = False

    #print realLogger.findCaller()
    global simpleLogConfigCache
    if not simpleLogConfigCache.has_key(p):
        #The logger name does not exist in the config file
        ch.setLevel(logging.DEBUG)
        simpleLogConfigCache[p] = True
        updateLogConfig(logFile, p)
    
    '''
    logStr = p+': '
    for i in args:
        try:
          logStr += str(i)+" "
        except:
          pass
    #print 'calling debug'
    realLogger.debug(logStr+str(realLogger.findCaller()))
    #realLogger.removeHandler(ch)#Must remove the handler otherwise, the output will be produced multiple times
    
def testFunc():
    cl('hello world')
    ncl('hello world')

    
class testClass:
    def testFunc(self):
        cl('hello test class')
'''
Use case:
1. add a log simply:
cl('a','b','c')
2. remove a log simply.
ncl('a','b','c')
Requirement:
1. log system shall has a config file.
2. log system shall output the function name of the log.
3. log system shall output log when requested.
4. log system shall support turn off single log in every log output.
5. log system shall output logs when it is not turned off
6. log system shall support to record the turn off operation for a log command.
'''
if __name__ == "__main__":
    #print loadLogConofig("logging.conf")
    testFunc()
    t = testClass()
    t.testFunc()
    
