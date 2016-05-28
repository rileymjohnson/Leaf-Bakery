import MySQLdb as mdb
def getRows(): #add to the stats tables
    con = mdb.connect('localhost', 'restuser', 'restuser1', 'rest')
    query = "select * from appetizersnum"
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
    return rows

print getRows()