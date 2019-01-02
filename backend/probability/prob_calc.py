import sqlite3

DB_FILENAME = 'available_log.db'

"""this function returns list of probabilitis for finding parking places according to the 
inserted time
the probabilities are according to the following order: ['mosachim', 'shapira', 'north', 'jerusalem']"""

def calculat_probs(user_time, delta=10/60):
    delta = (10/60)
    with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            stmt = """  SELECT AVG(found)
                        FROM log_tbl 
                        WHERE (? - ? < time) AND (time < ? + ?)
                        GROUP BY area_id
                        """
            cur.execute(stmt, (user_time,delta,user_time,delta))
            res = [p[0] for p in cur.fetchall()]
            cur.close()
    return res