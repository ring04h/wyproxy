# encoding: utf-8

from __future__ import absolute_import

from config import mysqldb_conn

import pymysql.cursors
import json
import time
 
def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

class MysqlInterface(object):
    """docstring for MysqlInterface"""
    
    def __init__(self):
        self.connection = self.init()

    @staticmethod
    def init():
        # Connect to the database
        connection = pymysql.connect(
                host = mysqldb_conn.get('host'),
                user = mysqldb_conn.get('user'),
                password = mysqldb_conn.get('password'),
                db = mysqldb_conn.get('db'),
                charset = mysqldb_conn.get('charset'),
                cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insert_result(self, result):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = """INSERT INTO `capture` (
                `content_length`,
                `static_resource`,
                `extension`,
                `url`,
                `status_code`,
                `date_end`,
                `date_start`,
                `port`, 
                `content`, 
                `header`, 
                `host`, 
                `content_type`, 
                `path`, 
                `scheme`, 
                `method`, 
                `request_content`, 
                `request_header`
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            content_length = result.get('content_length'),
            static_resource = result.get('static_resource'),
            extension = result.get('extension'),
            url = result.get('url'),
            status_code = result.get('status_code'),
            date_end = timestamp_datetime(result.get('date_end')),
            date_start = timestamp_datetime(result.get('date_start')),
            port = result.get('port'),

            content = result.get('content'),
            header = json.dumps(result.get('header'))

            host = result.get('host'),
            content_type = result.get('content_type'),
            
            path = result.get('path'),
            scheme = result.get('scheme'),
            method = result.get('method'),

            request_content = result.get('request_content'),
            request_header = json.dumps(result.get('request_header'))

            cursor.execute(sql, (
                content_length,
                static_resource,
                extension,
                url,
                status_code,
                date_end,
                date_start,
                port,
                content,
                header,
                host,
                content_type,
                path,
                scheme,
                method,
                request_content,
                request_header)
            )

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

    def close(self):
        if self.connection:
            return self.connection.close()

    def __del__(self):
        """close mysql database connection"""
        self.close()



