'''
Created on 2017年7月9日

@author: JiangShuanglong
'''
# encoding:utf-8
import os
import threading
import logging.config

LogDict = {
    'version':1,
    'loggers':{
        'root':{
            'level':'DEBUG',
            'handlers':['streamHandler','fileHandler','rotateHandler']
        },
        'stream':{
            'level':'DEBUG',
            'handlers':['streamHandler']
        },
        'tempFile':{
            'level':'DEBUG',
            'handlers':['fileHandler']
        },
        'rotateFile':{
            'level':'INFO',
            'handlers':['rotateHandler']
        }
    },
    'handlers':{
        'streamHandler':{
            'class':'logging.StreamHandler',
            'level':'DEBUG',
            'formatter':'streamFmt',
            'stream':'ext://sys.stdout'
        },
        'fileHandler':{
            'class':'logging.FileHandler',
            'level':'DEBUG',
            'formatter':'streamFmt',
            'filename':'./logs/tempFile.log',
            'mode':'w'
        },
        'rotateHandler':{
            'class':'logging.handlers.RotatingFileHandler',
            'level':'INFO',
            'formatter':'rotateFmt',
            'filename':'./logs/rotateFile.log',
            'mode':'a',
            'maxBytes':10485760,
            'backupCount':5
        }
    },
    'formatters':{
        'streamFmt':{
            'format':'%(asctime)s.%(msecs)d [%(levelname)-5s] %(message)s (%(filename)s:%(lineno)d %(module)s.%(funcName)s tid=%(thread)d)',
            'datefmt':'%H:%M:%S'
        },
        'rotateFmt':{
            'format':'%(asctime)s [%(levelname)-5s] %(module)s- %(message)s'
        }
    }
}

class LogUtil(object):
    '日志工具类'
    
    _instance = None
    _log = None
    _lock = threading.Lock()
    
    def __init__(self):
        print("disable the __init__ method")
        
    def __del__(self):
        pass
    
    @staticmethod
    def __checkLogsDir():
        logsDir = os.path.abspath(".")+"\\logs"
        if not os.path.exists(logsDir):
            os.mkdir(logsDir)
            
    @staticmethod
    def __logUtilInit():
        LogUtil.__checkLogsDir()
        logging.config.dictConfig(LogDict)
        LogUtil._log = logging.getLogger("root")

    @staticmethod
    def instance():
        if not LogUtil._instance:
            LogUtil._lock.acquire()
            if not LogUtil._instance:
                LogUtil._instance = object.__new__(LogUtil)
                object.__init__(LogUtil._instance)
                LogUtil.__logUtilInit()
            LogUtil._lock.release()
        return LogUtil._instance
    
    def __log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        sinfo = None
        try:
            fn, lno, func, sinfo = LogUtil._log.findCaller(stack_info)
        except ValueError: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        record = LogUtil._log.makeRecord(LogUtil._log.name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        LogUtil._log.handle(record)
        
    def debug(self,msg, *args, **keywords):
        if msg and LogUtil._log:
            self.__log(logging.DEBUG, msg, args, keywords)

    def info(self,msg=None):
        if msg:
            LogUtil._log.info(msg)
    
    def warn(self,msg=None):
        if msg:
            LogUtil._log.warn(msg)
    
    def error(self,msg=None):
        if msg:
            LogUtil._log.error(msg)

    def shutdown(self):
        logging.shutdown()