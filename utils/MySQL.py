# -*- coding:utf-8 -*-
"""
    @Time  : 2021/11/10  13:55
    @Author: Feng Lepeng
    @File  : MySQL.py
    @Desc  :
"""
import pymysql
from utils.logging import logger
from utils.op_ini import OPConfig


class MySQLLocal(object):

    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )

    def select(self, sql, sql_parameter=None):
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql, sql_parameter)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            logger.exception(e)
            return []

        finally:
            if cursor is not None:
                cursor.close()

    def exec_sql(self, sql, data=None):
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            logger.exception(e)
            if self.conn is not None:
                self.conn.rollback()
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def update(self, sql, data=None):
        return self.exec_sql(sql, data)

    def insert(self, sql, data=None):
        return self.exec_sql(sql, data)

    def delete(self, sql, data=None):
        return self.exec_sql(sql, data)

    def truncate_table(self, sql=None, data=None):
        return self.exec_sql(sql, data)

    def insert_many_items(self, sql=None, data=None):
        cursor = None

        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            logger.exception(e)
            if self.conn is not None:
                self.conn.rollback()
        finally:
            if cursor is not None:
                cursor.close()

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.exception("close db error")


if __name__ == '__main__':
    opc = OPConfig()
    user = opc.get_config("MySQL", "user")
    port = opc.get_config("MySQL", "port")
    host = opc.get_config("MySQL", "host")
    passwd = opc.get_config("MySQL", "passwd")
    db = opc.get_config("MySQL", "db")
    mysql = MySQLLocal(host, port, user, passwd, db)
