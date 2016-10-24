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
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) < 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) > 4)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekend_filtrado(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet, usuario\n"
        self.query += "WHERE twe_usuario = usu_id\n"
        self.query += "AND NOT usu_filtrado\n"
        self.query += "AND (date_part('dow', DATE(twe_fecha_creacion)) < 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) > 4)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekend_near_POI(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM\n"
        self.query += "(SELECT twe_id, twe_hora_creacion, twe_fecha_creacion, MIN(ST_DISTANCE(twe_geografia, poi_geografia))\n"
        self.query += "FROM tweet, punto_interes\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) < 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) > 4)\n"
        self.query += "GROUP BY twe_id\n"
        self.query += "HAVING MIN(ST_DISTANCE(twe_geografia, poi_geografia)) <= 50) as foo\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekend_near_POI_filtrado(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM\n"
        self.query += "(SELECT twe_id, twe_hora_creacion, twe_fecha_creacion, MIN(ST_DISTANCE(twe_geografia, poi_geografia))\n"
        self.query += "FROM tweet, punto_interes, usuario\n"
        self.query += "WHERE twe_usuario = usu_id\n"
        self.query += "AND NOT usu_filtrado\n"
        self.query += "AND (date_part('dow', DATE(twe_fecha_creacion)) < 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) > 4)\n"
        self.query += "GROUP BY twe_id\n"
        self.query += "HAVING MIN(ST_DISTANCE(twe_geografia, poi_geografia)) <= 50) as foo\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 4)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays_filtrado(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM tweet, usuario\n"
        self.query += "WHERE twe_usuario = usu_id\n"
        self.query += "AND NOT usu_filtrado\n"
        self.query += "AND (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 4)\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays_near_POI(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM\n"
        self.query += "(SELECT twe_id, twe_hora_creacion, twe_fecha_creacion, MIN(ST_DISTANCE(twe_geografia, poi_geografia))\n"
        self.query += "FROM tweet, punto_interes\n"
        self.query += "WHERE (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 4)\n"
        self.query += "GROUP BY twe_id\n"
        self.query += "HAVING MIN(ST_DISTANCE(twe_geografia, poi_geografia)) <= 50) as foo\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()

    def time_distribution_weekdays_near_POI_filtrado(self):
        self.query = "SELECT EXTRACT (HOUR FROM twe_hora_creacion), COUNT(*)\n"
        self.query += "FROM\n"
        self.query += "(SELECT twe_id, twe_hora_creacion, twe_fecha_creacion, MIN(ST_DISTANCE(twe_geografia, poi_geografia))\n"
        self.query += "FROM tweet, punto_interes, usuario\n"
        self.query += "WHERE twe_usuario = usu_id\n"
        self.query += "AND NOT usu_filtrado\n"
        self.query += "AND (date_part('dow', DATE(twe_fecha_creacion)) >= 1\n"
        self.query += "OR date_part('dow', DATE(twe_fecha_creacion)) <= 4)\n"
        self.query += "GROUP BY twe_id\n"
        self.query += "HAVING MIN(ST_DISTANCE(twe_geografia, poi_geografia)) <= 50) as foo\n"
        self.query += "GROUP BY EXTRACT (HOUR FROM twe_hora_creacion)\n"
        self.query += "ORDER BY EXTRACT (HOUR FROM twe_hora_creacion) ASC\n"
        return self.execute_query()



