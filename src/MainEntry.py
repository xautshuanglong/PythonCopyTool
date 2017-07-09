'''
Created on 2017年7月9日

@author: JiangShuanglong
'''
from com.shuanglong.utils.LogUtil import LogUtil

print("Hello World!")

LogUtil.instance().debug("test")
LogUtil.instance().info("test")

i = 123
def testFunc():
    LogUtil.instance().debug("ha ha he %d %s", i,"string test")

if __name__ == '__main__':
    LogUtil.instance().debug("hehe")
    testFunc()
    pass