#!/usr/bin/env python
# coding: utf-8
import pymysql
import gevent
import time


class MyPyMysql:
    def __init__(self, host, port, username, password, db, charset='utf8'):
        self.host = host  # mysql主机地址
        self.port = port  # mysql端口
        self.username = username  # mysql远程连接用户名
        self.password = password  # mysql远程连接密码
        self.db = db  # mysql使用的数据库名
        self.charset = charset  # mysql使用的字符编码,默认为utf8
        self.pymysql_connect()  # __init__初始化之后，执行的函数

    def pymysql_connect(self):
        # pymysql连接mysql数据库
        # 需要的参数host,port,user,password,db,charset
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset
                                    )

        # 连接mysql后执行的函数
        # max_line:定义每次最大插入行数(max_line=N,即一次插入N行),max_num:插入总数
        self.run('emp_test1',1000,200001)
        # self.run('emp_test2',1000,3001)
        # self.run('emp_test3',1000,5001)
        self.conn.close()  # 关闭pymysql连接

    def run(self, table_name,max_line,max_num):
        self.create_table(table_name)
        self.asynchronous(table_name,max_line,max_num)

    def insert_data(self, nmin, nmax, table_name):
        # 创建游标
        self.cur = self.conn.cursor()

        # 定义sql语句,插入数据id,name,gender,email
        sql = "insert into " + table_name + "(name,gender,email,x1,x2,x3,x4,x5,x6,x7) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # 定义总插入行数为一个空列表
        data_list = []
        for i in range(nmin, nmax):
            # 添加所有任务到总的任务列表
            result = (
            'zhangsan' + str(i), 1, 'zhangsan' + str(i) + '@qq.com', str(i), str(i), str(i), str(i), str(i), str(i),
            str(i))
            data_list.append(result)

        # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
        # print(sql)
        # print(data_list)
        content = self.cur.executemany(sql, data_list)
        if content:
            print('成功插入第{}条数据'.format(nmax - 1))

        # 提交数据,必须提交，不然数据不会保存
        self.conn.commit()

    def asynchronous(self, table_name, max_line,max_num):

        # g_l 任务列表
        # 定义了异步的函数: 这里用到了一个gevent.spawn方法
        # max_line = 1000  # 定义每次最大插入行数(max_line=N,即一次插入N行)
        # g_l = [gevent.spawn(self.run, i, i+max_line) for i in range(1, 3000001, max_line)]
        g_l = [gevent.spawn(self.insert_data, i, i + max_line, table_name) for i in range(1, max_num, max_line)]

        # gevent.joinall 等待所以操作都执行完毕
        gevent.joinall(g_l)
        self.cur.close()  # 关闭游标
        # self.conn.close()  # 关闭pymysql连接

    def create_table(self, table_name):

        # 创建游标
        self.cur = self.conn.cursor()
        # 创建游标
        # cursor = db.cursor()
        # 如果存在表，则删除
        self.cur.execute("DROP TABLE IF EXISTS `" + table_name + "`")

        # 创建student表
        sql = "CREATE TABLE `" + table_name + "` (`name` VARCHAR (64) DEFAULT NULL,`gender` TINYINT (8) DEFAULT NULL,`email` VARCHAR (128) DEFAULT NULL,`x1` VARCHAR (64) DEFAULT NULL,`x2` VARCHAR (64) DEFAULT NULL,`x3` VARCHAR (64) DEFAULT NULL,`x4` VARCHAR (64) DEFAULT NULL,`x5` VARCHAR (64) DEFAULT NULL,`x6` VARCHAR (64) DEFAULT NULL,`x7` VARCHAR (64) DEFAULT NULL)"

        try:
            # 执行SQL语句
            self.cur.execute(sql)
            print("创建表成功")
        except Exception as e:
            print("创建表失败：case%s" % e)
        finally:
            # 关闭游标连接
            self.cur.close()
            # self.conn.close()  # 关闭pymysql连接


if __name__ == '__main__':
    start_time = time.time()  # 计算程序开始时间
    # st = MyPyMysql('172.16.10.65', 3306, 'drpeco', 'DT@Stack#123', 'test')  # 实例化类，传入必要参数
    st = MyPyMysql('172.16.8.193', 3306, 'root', '123456', 'api_test')  # 实例化类，传入必要参数
    print('程序耗时{:.2f}'.format(time.time() - start_time))  # 计算程序总耗时
