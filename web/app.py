# encoding: utf-8

import sys
sys.path.append("..")

from flask import Flask, request, Response, jsonify, render_template, g, redirect
from database import MYSQL
from config import mysqldb_conn

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
    show_cnt = 10

    sql = 'select count(*) as cnt from capture'
    table_size = int(dbconn.query(sql, fetchone=True).get('cnt'))
    max_page = table_size / show_cnt + 1

    page = request.args.get('page', 1, type=int)
    page = page if page >= 0 else 1
    limits = '{},{}'.format(show_cnt * page - show_cnt, show_cnt)
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

@app.route('/n')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

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
    return unicode(content, encode_name)

# return type of arg


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True)
