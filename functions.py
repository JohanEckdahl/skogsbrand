import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
class Database():
    
    def __init__(self, db_name): self.connection = self.connect(db_name)
    
    def read(self, sql): pass
    
    def connect(self,db_name): pass
    
    def insert(self, table_name, dataframe): print("yaa, inserted, get some!")
        
    def disconnect(self): pass
        
    def __del__(self): self.disconnect()
        

class SQLiteDB(Database):
    
    def connect(self,db_name): return sqlite3.connect(db_name)
    
    def read(self, sql): return pd.read_sql_query(sql, self.connection,
                                                  index_col="id")
    
    def insert(self, table_name, dataframe):
        dataframe.to_sql(table_name, self.connection,
                         if_exists="append", index = False)
        
    def disconnect(self): self.connection.close()

def df_to_file(df, name): pass


import math

class Haversine:
    '''
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet
    
    '''
    def __init__(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280               # output distance in feet

def plot(df,lines):
    x = df["CenterY"]/10000
    y = df["CenterX"]/10000
    s = df["GISHektar"]*2
    s = 2
    print("Total fires: {}".format(len(df.index)))
    #display(df.head())
    plt.figure(figsize=(9,9))
    plt.scatter(x,y,s, color = 'orange', linewidths = 2)
    plt.hlines(lines,30,90, color = 'green')
    plt.axis('equal')
    plt.show()
    
def show_image(area): display(Image(filename='images/area_{}.png'.format(area)))
    
def write(df):
    og = pd.read_csv("./data/df.csv", index_col=0)
    og.update(df)
    og.to_csv("./data/df.csv")
    
def read(): return pd.read_csv("./data/df.csv", index_col = 'OBJECTID')


def sites_per_zone(df, lines):
    count = []
    for zone in range(5):
        zone += 1
        df2 = df
        df2 = df2[df2.quality >= 2]
        df2 = df2[df2.CenterX < lines[-1+zone]*10000]
        df2 = df2[df2.CenterX > lines[0+zone]*10000]
        count.append(len(df2.index))
    names = ['1','2','3','4','5']
    plt.figure(figsize = (4,4))
    plt.grid(1, axis = 'x')
    plt.barh(names[::-1], count[::-1], )
    

def hectare_per_zone(df):
    df = df[df.quality >= 2]
    df = df.sort_values("CenterX", axis =0)
    df.plot.barh(x='CenterX', y='GISHektar', xlim = (0,150))


def calculate_walk(name):
    db = SQLiteDB(name)
    df = db.read("SELECT * FROM fires_site")
    df2 = db.read("SELECT * FROM fires_parking")
    db.disconnect
    df = df.merge(df2, left_on='parking_id', right_on='id')
    display(df)
    list=[]
    i = 0
    for index, row in df.iterrows():
        a = Haversine([row['longitude_y'], row['latitude_y']],[row['longitude_x'], row['latitude_x']]).km*1000
        a=int(a)
        list.append(a)
        #if a < 500:
            #print(index, int(a), i)
            #i += 1
    df['Walk'] = list
    return(df)

