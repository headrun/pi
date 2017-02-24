#!/usr/bin/env python

import sys
import MySQLdb
import optparse
import traceback
import ssh_utils

from table_schemas import TABLES


HOST = '10.28.218.81'
USER = 'veveo'
PASSWORD = 'veveo123'
_setups = {'dev': '10.28.218.81', 'prod': '10.28.218.81'}


def create_new_db(db_name):
    CREATE_NEW_DB_DIR_CMD = "echo 'veveo123' | sudo -S mkdir /data/DATABASES/%s/; echo 'veveo123' | sudo -S chmod 755 /data/DATABASES/%s/;"
    CHANGE_PERMISSIONS_CMD = "echo 'veveo123' | sudo -S chown -R mysql:mysql /data/DATABASES/%s;"
    CREATE_NEW_SYMLINK_CMD = "echo 'veveo123' | sudo -S ln -s /data/DATABASES/%s /var/lib/mysql/%s; echo 'veveo123' | sudo -S chown -R mysql:mysql /var/lib/mysql/%s"

    create_db_cmd = CREATE_NEW_DB_DIR_CMD % (db_name, db_name)
    status = ssh_utils.ssh_cmd(HOST, USER, PASSWORD, create_db_cmd)
    if status != 0: sys.exit(1)

    change_perms_cmd = CHANGE_PERMISSIONS_CMD % (db_name)
    status = ssh_utils.ssh_cmd(HOST, USER, PASSWORD, change_perms_cmd)
    if status != 0: sys.exit(1)

    sym_link_create_cmd = CREATE_NEW_SYMLINK_CMD % (db_name, db_name, db_name)
    status = ssh_utils.ssh_cmd(HOST, USER, PASSWORD, sym_link_create_cmd)
    if status != 0: sys.exit(1)

def change_permissions_to_new_tables(db_name):
    _CHANGE_PERMISSIONS_CMD = "echo 'veveo123' | sudo -S chmod 644 /data/DATABASES/%s/*; " % (db_name)
    _CHANGE_PERMISSIONS_CMD += "echo 'veveo123' | sudo -S chown -R mysql:mysql /data/DATABASES/%s/*;" % (db_name)
    status = ssh_utils.ssh_cmd(HOST, USER, PASSWORD, _CHANGE_PERMISSIONS_CMD)
    if status != 0: sys.exit(1)

def get_cursor(_setup, _ip):
    _host = _ip or _setups[_setup]

    conn = MySQLdb.connect(host=_host, user="veveo", passwd="veveo123")
    cursor = conn.cursor()

    return conn, cursor

def create_tables(db_name, cursor):
    try:
        cursor.execute('USE %s;' % db_name)
        query = "ALTER DATABASE " + db_name + " CHARACTER SET utf8;"
        cursor.execute(query)
        for ttype, table in TABLES.iteritems():
            try:
                cursor.execute(table)
            except:
                print "Table: ", table
                traceback.print_exc()
        print "New Database '%s' Created Successfully." % (db_name)
    except:
        traceback.print_exc()

def main(options):
    db_name = options.db_name.strip()
    _setup  = options.setup.strip()
    _ip     = options.ip.strip()

    if _setup not in ['dev', 'prod']:
        print "Setup Must be in prod/dev"
        sys.exit(1)

    conn, cursor = get_cursor(_setup, _ip)

    if _setup == "prod" and db_name:
        create_new_db(db_name)
    elif _setup == "dev" and db_name:
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s;' % (db_name))
    else:
        print "Please Provide options Properly"
        sys.exit()

    create_tables(db_name, cursor)

    if _setup == "prod" and db_name:
        change_permissions_to_new_tables(db_name)


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-s', '--setup', default='dev', help='Setup - prod / dev' )
    parser.add_option('-i', '--ip', default='', help='Ip Address for Create Database')
    parser.add_option('-d', '--db-name', default='', help='DataBase Name' )

    (options, args) = parser.parse_args()

    main(options)
