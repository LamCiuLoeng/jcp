import cx_Oracle, os, traceback
os.environ["NLS_LANG"] = "american_america.al32utf8"

oracle_config = {"oracle_connection_str":"rpac/rpac@192.168.42.9:1521/oracle"}
def createConnection():
    conn = oracle_config["oracle_connection_str"]
    return cx_Oracle.connect(conn)


def executeSearchSQL(dbconnection, sql, params, all=True, wrap=False):
    cursor = dbconnection.cursor()
    cursor.prepare(sql)
    cursor.execute(None, params)
    if all:
        if wrap:
            return [dtoWrap(cursor, row) for row in cursor.fetchall()]
        else:
            return cursor.fetchall()
    else:
        if wrap:
            return dtoWrap(cursor, cursor.fetchone())
        else:
            return cursor.fetchone()

def searchOracle(sql, params, all=True, wrap=False):
    dbconn = createConnection()
    try:
        return executeSearchSQL(dbconn, sql, params, all, wrap)
    except:
        traceback.print_exc()
        return None
    finally:
        dbconn.close()
