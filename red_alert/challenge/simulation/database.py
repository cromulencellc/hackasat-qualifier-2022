from numpy import insert
import psycopg2


class SimDatabase:
    def __init__( self , ip, port , user , pw , db ):
        self.connection = psycopg2.connect(database=db, \
                                      user = user, \
                                      password = pw, \
                                      host =ip, 
                                      port = port)
        self.cursor = self.connection.cursor()
        self.count = 0 
        self.laser_count = 0 
        self.detector_count = 0
    def create_laser( self ):
        db_name = "LASERS"

        #self.cursor.execute("""DROP TABLE {}""".format( db_name))
        #self.connection.commit()
        create_query = """CREATE TABLE {} \
                            (COUNT INT PRIMARY KEY NOT NULL,\
                            TIME TIMESTAMP NOT NULL, \
                            CYCLE REAL NOT NULL, \
                            STATE REAL NOT NULL
                            )""".format( db_name )
        self.cursor.execute( create_query )
        self.connection.commit()
    def create_detector( self ):
        db_name = "DETECTOR"

        create_query = """CREATE TABLE {} \
                            (COUNT INT PRIMARY KEY NOT NULL,\
                            TIME TIMESTAMP NOT NULL, \
                            RANGE REAL NOT NULL,\
                            CYCLE REAL NOT NULL, \
                            STATE REAL NOT NULL
                            )""".format( db_name )
        self.cursor.execute( create_query )
        self.connection.commit()
    def post_detector( self, sats , current_time ):
        for name, sat in sats.items():
            nearest = sat.get_range()
            count = self.laser_count
            detector = sat.get_detector()
            state = 1 if detector[0] else 0
            cycle = detector[1]
            time_db = current_time.strftime("%Y-%m-%d %H:%M:%S+00")
            insert_query = """INSERT INTO DETECTOR (COUNT,TIME,RANGE,CYCLE,STATE) \
                              VALUES ({},'{}',{},{},{})""".format(  count , time_db,  nearest , cycle ,state  )
            self.cursor.execute( insert_query )
            self.connection.commit( )
            self.detector_count +=1
    def post_laser( self , sats , current_time  ):
        for name, sat in sats.items():
            nearest = sat.get_range()
            count = self.laser_count
            lasers = sat.get_laser()
            state = 1 if lasers[0] else 0
            cycle = lasers[1]
            time_db = current_time.strftime("%Y-%m-%d %H:%M:%S+00")
            insert_query = """INSERT INTO LASERS (COUNT,TIME,CYCLE,STATE) \
                              VALUES ({},'{}',{},{})""".format(  count , time_db,   cycle ,state  )

            self.cursor.execute( insert_query )
            self.connection.commit( )

            self.laser_count +=1
    def create_sat( self ,sats ):
        for name,sat in sats.items():
            db_name = "CDH"

            
            create_query = """CREATE TABLE {} \
                           (COUNT INT PRIMARY KEY NOT NULL,\
                            TIME TIMESTAMP NOT NULL, \
                            TEMP REAL NOT NULL, \
                            BATTERY REAL NOT NULL
                            )""".format( db_name )
            self.cursor.execute( create_query )
            self.connection.commit( )
    def post_sats( self , sats , current_time):
        for name,sat in sats.items():
            db_name = "CDH"
            
            temp = sat.get_temperature()
            battery = sat.get_battery()

            self.count = self.count+1
            count = self.count
            time_db = current_time.strftime("%Y-%m-%d %H:%M:%S+00")

            insert_query = """INSERT INTO {} (COUNT,TIME,TEMP,BATTERY) \
                              VALUES ({},'{}',{},{})""".format( db_name, count , time_db, temp , battery )
            self.cursor.execute( insert_query )
            self.connection.commit( )
    def post_flag( self , flag ):
        create_query = """CREATE TABLE FLAG \
                           (COUNT INT PRIMARY KEY NOT NULL,\
                            FLAG VARCHAR(200) NOT NULL)"""
        self.cursor.execute( create_query )
        self.connection.commit( )
        insert_query = """INSERT INTO FLAG (COUNT , FLAG ) VALUES ({}, '{}')""".format(1 , flag )
        self.cursor.execute( insert_query )
        self.connection.commit( )