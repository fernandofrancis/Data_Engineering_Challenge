#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 16:31:16 2022

@author: Francis
"""

import os
from flask import Flask,  request, redirect, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine,text

###

UPLOAD_FOLDER = '/home/mtuser/Documentos/josity'

######

def create_engeni():
    engine = create_engine("postgresql://postgres:Empresa1@localhost:5432/jobsity")
    
    return engine
    
def get_uuid(engine):
    stmt= text("SELECT uuid_generate_v4()")
    result=engine.execute(stmt).fetchall()[0][0]
    
    return result

def queue_file(engine,file_name,uuid,file_name_proc):
    stmt= text("INSERT INTO queue_table(id_uuid,file_name,file_name_proc) VALUES(:id_uuid,:file_name,:file_name_proc)")
    engine.execute(stmt,{"id_uuid":uuid,"file_name":file_name,"file_name_proc":file_name_proc})
    
    return None

def insert_info_file(engine,file_name,uuid,status):
    stmt= text("INSERT INTO CSV_FILES(id_uuid,file_name,status,datetime) VALUES(:id_uuid,:file_name,:status,now())")
    engine.execute(stmt,{"id_uuid":uuid,"file_name":file_name,"status":status})
    
    return None
    
#%%
ALLOWED_EXTENSIONS = {'csv'}
conn=create_engeni()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#%%


    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=[ 'POST'])
def upload_file():
    if request.method == 'POST':       
        file = request.files['file']       
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uuid=get_uuid(conn)
            filename_new=filename+"-"+str(uuid)+'.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))
            queue_file(conn,filename,uuid,filename_new)
            insert_info_file(conn,filename,uuid,"queued")
            return jsonify(job=uuid,
                           filename=file.filename,
                           status="queued")

@app.route('/weekly/region/<string:region>', methods=['GET'])
def get_weekly_region(region):
    stmt= text('''select json_agg(json) from (SELECT sum(qty) as qty,to_char(date_trunc('week',datetime) :: DATE, 'yyyy-mm-dd') AS weekly,region                            
                       FROM trips
                       where region=:region
                       GROUP BY region,weekly) json;''')
    result=conn.execute(stmt,{"region":region}).all()[0][0]
    return jsonify(result)

@app.route('/weekly/bbox/<string:bbox>', methods=['GET'])
def get_weekly_bbx(bbox):
    min_long,min_lat,max_long,max_lat=map(float,bbox.split(','))
    stmt= text('''select json_agg(json) from (SELECT sum(qty) as QTD,to_char(date_trunc('week',datetime) :: DATE, 'yyyy-mm-dd') AS weekly,region                            
                       FROM trips where 
                       ST_Intersects(trips.geometry,ST_MakeEnvelope(:min_long,:min_lat,:max_long,:max_lat,4326))
                       GROUP BY region,weekly) json;''')
    result=conn.execute(stmt,{"min_long":min_long,"min_lat":min_lat,"max_long":max_long,"max_lat":max_lat}).all()[0][0]
    return jsonify(result)

@app.route("/jobs/", defaults={ 'job': 'all' })
@app.route('/jobs/<string:job>',methods=['GET'])    
def get_jobs(job):
    if job!='all':
        add_sql='where id_uuid=:job) json;'
    else:
        add_sql=') json;'    
    stmt= text('''select json_agg(json) from (SELECT id_uuid,file_name,to_char(datetime :: DATE, 'yyyy-mm-dd') AS date,status                            
                       FROM CSV_FILES '''+add_sql)
    result=conn.execute(stmt,{"job":job}).all()[0][0]
    return jsonify(result)
#%%    

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)




