#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 18:54:59 2022

@author: mtuser
"""
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
from shapely import wkt
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import time


UPLOAD_FOLDER = '/home/mtuser/Documentos/josity/'


def get_sequence_id(engine,sequence):
    stmt= text("SELECT NEXTVAL(:seq)")
    result=engine.execute(stmt,{"seq":sequence}).fetchall()[0][0]
    
    return result

def create_engeni():
    engine = create_engine("postgresql://postgres:Empresa1@localhost:5432/jobsity")
    
    return engine

def insert_postgis(table,gpd_fram,engine):
    gpd_fram.to_postgis(table, engine,if_exists='append')  
    
#%%     
def gpd_csv_preparation(file):    
    
    ## Load csv as gpd
    
    data = gpd.read_file(file)
    data.set_crs(epsg=4326, inplace=True)
    ### Convert datetime cuting minutes and seconds
    
    data['datetime']= pd.to_datetime(data['datetime'])
    data['datetime']= pd.to_datetime(data['datetime'].dt.strftime('%m/%d/%Y %H'))
    
    ### load the points 
    
    data['origin_coord']=gpd.GeoSeries.from_wkt(data['origin_coord'])
    data['destination_coord']=gpd.GeoSeries.from_wkt(data['destination_coord'])
    
    ### Reduce the coord precision to 4 decimals 
    data['origin_coord'] = data.apply(lambda row: wkt.dumps(row['origin_coord'], rounding_precision=4), axis=1)
    data['destination_coord'] = data.apply(lambda row: wkt.dumps(row['destination_coord'], rounding_precision=4), axis=1)
    
    data['origin_coord']=gpd.GeoSeries.from_wkt(data['origin_coord'])
    data['destination_coord']=gpd.GeoSeries.from_wkt(data['destination_coord'])
    
    ### Create LineString using  origin_coord and destination_coord points
    
    data['geometry'] = data.apply(lambda row: LineString([row['origin_coord'], row['destination_coord']]), axis=1)
    
    
    ### create column geometry_wkb with the hex from geometry to use when aggregate
    
    data['geometry_wkb'] = gpd.GeoSeries.to_wkb(data['geometry'],hex=True)
    
    ### create column datasource_2 with a list of datasources with  similar trips
    
    data2=data.groupby(['geometry_wkb','datetime'])['datasource'].apply(list).reset_index(name = 'datasource_2')
    
    ### join the dataframes, remove the duplicated rows and switch to the new datasource column
    
    data=data.merge(data2, on =['geometry_wkb','datetime'])
    data.drop(columns=['datasource'])
    data = data.drop_duplicates(subset='geometry_wkb', keep="first")
    data=data.drop(columns=['datasource'])
    data=data.rename(columns={'datasource_2': 'datasource'})
    
    ### Add trip's quantity column 
    
    data['qty']=data['datasource'].str.len()
    
    return data

def insert_data(data):
    data['id']=data.apply(lambda row: get_sequence_id(conn,'trips_id_seq'), axis=1)    
    #  create datasource dataframe with ID and datasource , insert into datasource table 
    data_datasource=data[['id','datasource']]
    data_datasource_expand = data_datasource.assign(name=data.datasource.str.split(",")).explode('datasource')
    data_datasource_expand=data_datasource_expand.drop(columns=['name'])    
    
    #Insert geopandas into postgis
    data=data.drop(columns=['datasource'])
    insert_postgis("trips",data,conn)
    #insert 
    data_datasource_expand.to_sql('datasource',conn,if_exists='append',index=False)
    
    return True

def get_queue(session):
    session.begin()    
    stmt= text('''DELETE FROM queue_table USING (
                SELECT * FROM queue_table LIMIT 1 FOR UPDATE SKIP LOCKED
                ) q
                WHERE q.id = queue_table.id RETURNING q.id,q.file_name_proc,q.id_uuid;''')
    result=session.execute(stmt).all()
    
    return result

def update_file_status(id_uuid,status):
    stmt= text('''update csv_files set status=:status,datetime_proc=now() 
                                               where id_uuid=:id_uuid;''')
    conn.execute(stmt,{"status":status,"id_uuid":id_uuid})
    
    return None
    

def main_program():
    while True:    
        queue=get_queue(session)
        if queue:   
            for row in queue:
                #print(row[0])
                update_file_status(row[2],'Running')
                data=gpd_csv_preparation(UPLOAD_FOLDER+row[1])
                insert_data(data)
                update_file_status(row[2],'Processed')
            session.commit()            
        else:        
            print("No file")
            session.commit()
        #queue[1].commit()        
        time.sleep(5) 
    return None
#%%
conn=create_engeni()
Session = sessionmaker(bind=conn)
session=Session()
#%%

if __name__ == "__main__":
    main_program()
    

