import pymysql
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def level_discount():
    print("启动") # 转换成记录？
    #读取当前日期，如：05-04
    # 打开数据库连接
    conn = pymysql.connect('localhost', 'root', '123456', 'G3')
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    try:
        # 执行sql语句
        cursor.execute("update Member set Discount=0.95 where Level = 1")
        cursor.execute("update Member set Discount=0.85 where Level = 2")
        cursor.execute("update Member set Discount=0.75 where Level = 3")
        # 提交到数据库执行
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()
    # 关闭数据库连接
    conn.close()

sched = BlockingScheduler()
sched.add_job(level_discount, 'cron', hour=17, minute=5)
sched.start()
