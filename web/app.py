# encoding: utf-8

import sys
sys.path.append("..")

# from gevent import monkey
# monkey.patch_all()

from flask import Flask, request, Response, jsonify, render_template, g, redirect
from database import MYSQL
from pymysql import escape_string
from config import mysqldb_conn, show_cnt

app = Flask(__name__)

def connect_db():
    # msyql dababase connection info
    dbconn = MYSQL(
            dbhost = mysqldb_conn.get('host'), 
            dbuser = mysqldb_conn.get('user'),
            dbpwd = mysqldb_conn.get('password'),
            dbname = mysqldb_conn.get('db'),
            dbcharset = mysqldb_conn.get('charset'))
    return dbconn

@app.route("/", methods=['POST', 'GET'])
def index():
    dbconn = connect_db()

    sql = 'select count(*) as cnt from capture'
    table_size = int(dbconn.query(sql, fetchone=True).get('cnt'))
    max_page = table_size / show_cnt + 1

    page = request.args.get('p', 1, type=int)
    page = page if page > 0 else 1
    limits = '{},{}'.format((page-1)*show_cnt, show_cnt)
    order = 'id desc'
    records = dbconn.fetch_rows(
                        table='capture',
                        order=order,
                        limit=limits)
    return render_template(
                    'index.html', 
                    records=records, 
                    page=page,
                    max_page=max_page)

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/r", methods=['GET'])
def show_record():
    rid = request.args.get('id', 0, type=int)
    if not rid:
        return redirect('/')
    dbconn = connect_db()
    cond = {'id':rid}
    record = dbconn.fetch_rows(table='capture',condition=cond, fetchone=True)
    if record:
        return render_template('record.html', record=record)
    else:
        return redirect('/')

@app.route('/del', methods=['GET'])
def delete_record():
    rid = request.args.get('id', 0, type=int)
    referer = request.headers.get('Referer')
    if not rid:
        return redirect('/')
    dbconn = connect_db()
    cond = {'id':rid}
    dbconn.delete(table='capture',condition=cond)
    return redirect(referer) if referer else redirect('/')

@app.route('/q')
def add_numbers():
    search = request.args.get('s')
    if not search or ':' not in search or "'" in search:
        return redirect('/')
    page = request.args.get('p', 1, type=int)
    page = page if page > 0 else 1

    limits = '{},{}'.format((page-1)*show_cnt, show_cnt)
    order = 'id desc'

    search_str = search.split(' ')
    params = {}
    for param in search_str:
        name, value = param.split(':')
        if name not in ['host', 'port', 'status_code','method', 'type', 'content_type', 'scheme', 'extension']:
            return redirect('/')
        params[name] = value
    
    condition = comma = ''
    glue = ' AND '
    for key, value in params.iteritems():
        if ',' in value and key in ['port','status_code','method','type']:
            values = [escape_string(x) for x in value.split(',')]
            condition +=  "{}`{}` in ('{}')".format(comma, key, "', '".join(values))
        elif key in ['host']:
            condition +=  "{}`{}` like '%{}'".format(comma, key, escape_string(value))
        else:
            condition +=  "{}`{}` = '{}'".format(comma, key, escape_string(value))
        comma = glue

    dbconn = connect_db()
    count_sql = 'select count(*) as cnt from capture where {}'.format(condition)
    record_size = int(dbconn.query(count_sql, fetchone=True).get('cnt'))
    
    max_page = record_size/show_cnt + 1
    
    records = dbconn.fetch_rows(
                table='capture',
                condition=condition,
                order=order,
                limit=limits)

    return render_template(
                    'index.html', 
                    records=records, 
                    page=page,
                    search=search,
                    max_page=max_page)

@app.route('/proxy.pac')
def show_proxy_pac():
    ipaddr = '127.0.0.1'
    port = 8080
    pac_syntac = '''
function FindProxyForURL(url, host)
{
    if (isInNet(host, "192.168.199.0", "255.255.255.0"))
        return "DIRECT";

    return "SOCKS %s:%s";
}
    ''' % (ipaddr, port)

    return pac_syntac

@app.errorhandler(404)
def not_found(error):
    return redirect('/')

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

@app.template_filter('json_dumps')
def json_dumps(dict):
    import json
    return json.loads(dict)

@app.template_filter('to_unicode')
def to_unicode(content):
    from requests.packages import chardet
    encode_name = chardet.detect(content).get('encoding')
    return unicode(content, encode_name) if encode_name else ''

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=False,
        threaded=True)
