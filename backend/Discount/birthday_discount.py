import pymysql
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def birthday_discount():
    print("启动")
    #读取当前日期，如：05-04
    now_date = datetime.datetime.now().strftime('%y-%m-%d')
    print(now_date)

    # 打开数据库连接
    conn = pymysql.connect('localhost', 'root', '123456', 'G3')

    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # SQL 生日折扣更新语句
    sql = "update Member set Discount=0.65 where right(Birthday,5) = '%s'"%(now_date[-5:])
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()
    # 关闭数据库连接
    conn.close()


sched = BlockingScheduler()
sched.add_job(birthday_discount, 'cron', hour=0, minute=1)
sched.start()