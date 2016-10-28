import psycopg2

class Queries:

    def __init__(self):
        self.conn = ""

        self.query = ""

    def connect(self):
        self.conn = psycopg2.connect("dbname=postgis_22_sample user=postgres password=postgres")
        print("Connected to database")

    def disconnect(self):
        self.conn.close()
        print("Disconnected from database")

    def execute_query(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(self.query)
        result = cur.fetchall()
        cur.close()
        self.disconnect()
        return result

    def select_pois(self):
        self.query = "SELECT * FROM punto_interes"
        return self.execute_query()

    def tweet_intensity(self):
        self.query = "SELECT numTweets, count(*)\n"
        self.query += "FROM\n"
        self.query += "(SELECT COUNT(*) as numTweets\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY twe_usuario\n"
        self.query += "ORDER BY count(*)) as q\n"
        self.query += "GROUP BY numTweets\n"
        return self.execute_query()

    def users_by_month(self):
        self.query = "SELECT date_part('month', DATE(twe_fecha_creacion)), COUNT(DISTINCT twe_usuario)\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY date_part('month', DATE(twe_fecha_creacion))\n"
        self.query += "ORDER BY date_part('month', DATE(twe_fecha_creacion)) ASC\n"
        return self.execute_query()

    def tweets_by_month(self):
        self.query = "SELECT date_part('month', DATE(twe_fecha_creacion)), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY date_part('month', DATE(twe_fecha_creacion))\n"
        self.query += "ORDER BY date_part('month', DATE(twe_fecha_creacion)) ASC\n"
        return self.execute_query()

    def time_intervals(self):
        self.query = "SELECT dif, COUNT(*)\n"
        self.query += "FROM (SELECT twe_usuario, COUNT(*),MAX(twe_fecha_creacion)-MIN(twe_fecha_creacion) AS dif\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY twe_usuario\n"
        self.query += "HAVING COUNT(*) >=3 ) AS foo\n"
        self.query += "GROUP BY dif\n"
        self.query += "ORDER BY dif\n"
        return self.execute_query()

    def distance_between_tweets_and_pois(self):
        self.query = "SELECT twe_id, MIN(ST_DISTANCE(twe_geografia, poi_geografia))\n"
        self.query += "FROM tweet, punto_interes\n"
        self.query += "GROUP BY twe_id\n"
        #self.query += "LIMIT 200"
        return self.execute_query()

    def time_distribution_weekend(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) = 0\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) = 6)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekend_near_POI(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) = 0\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion))= 6)\n"
        self.query += "AND twe_min_distancia <= 50\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 5)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays_near_POI(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 5)\n"
        self.query += "AND twe_min_distancia <= 50\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def avg_stddev_distance_to_POI(self):
        self.query = "SELECT twe_usuario, AVG(twe_min_distancia), STDDEV(twe_min_distancia)\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY twe_usuario\n"
        self.query += "HAVING COUNT(*) >= 5\n"
        self.query += "ORDER BY STDDEV(twe_min_distancia) ASC\n"
        return self.execute_query()

    """
    def avg_distance_and_interval(self):
        self.query = "SELECT usu_fecha_max - usu_fecha_min, usu_avg_distancia\n"
        self.query += "FROM usuario\n"
        self.query += "WHERE usu_id IN (SELECT twe_usuario FROM tweet GROUP BY twe_usuario HAVING COUNT(*) >= 5)\n"
        return self.execute_query()
    """

    def avg_distance_and_interval(self):
        self.query = "SELECT AVG(twe_min_distancia), MAX(twe_fecha_creacion)-MIN(twe_fecha_creacion)\n"
        self.query += "FROM tweet\n"
        self.query += "GROUP BY twe_usuario HAVING COUNT(*) >= 5\n"
        return self.execute_query()

    def time_gap_between_consecutive_tweets(self):
        self.query = "SELECT t1.twe_id, MIN(DATE_PART('day', t2.twe_fecha_creacion::timestamp - t1.twe_fecha_creacion::timestamp)*24 + EXTRACT (HOUR FROM t2.twe_hora_creacion) - EXTRACT (HOUR FROM t1.twe_hora_creacion))\n"
        self.query += "FROM tweet t1, tweet t2\n"
        self.query += "WHERE t1.twe_usuario = t2.twe_usuario\n"
        self.query += "AND ((t2.twe_fecha_creacion = t1.twe_fecha_creacion AND t2.twe_hora_creacion > t1.twe_hora_creacion)\n"
        self.query += "OR t2.twe_fecha_creacion > t1.twe_fecha_creacion)\n"
        self.query += "GROUP BY t1.twe_id\n"
        self.query += "ORDER BY t1.twe_id\n"
        return self.execute_query()




