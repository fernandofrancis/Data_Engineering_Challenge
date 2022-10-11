# Description
This challenge will evaluate your proficiency in Data Engineering, and your knowledge in
Software development as well.

## Assignment
Your task is to build an automatic process to ingest data on an on-demand basis. 
The data
represents trips taken by different vehicles, and include a city, a point of origin and a destination.

This CSV file gives you a small sample of the data your solution will have to handle. 
We would like to have some visual reports of this data, but in order to do that, we need the following
features.

We do not need a graphical interface. Your application should preferably be a REST API, or a
console application.

## Mandatory Features
There must be an automated process to ingest and store the data.  

Trips with similar origin, destination, and time of day should be grouped together. 

Develop a way to obtain the weekly average number of trips for an area, defined by a
bounding box (given by coordinates) or by a region. 

Develop a way to inform the user about the status of the data ingestion without using a
polling solution. 

The solution should be scalable to 100 million entries. It is encouraged to simplify the
data by a data model. Please add proof that the solution is scalable. 

Use a SQL database. 

## Solution
Data Base: Postgresql SQL database with PostGis extensions. 

Ingestion routine: app.py - rest api to upload the file to the server and put the file in the process queue. Request reports and process status. 

Process routine: data_proc.py - responsible to get the files from the queue, process and insert into postgres. 

## Steps
- Install PostgreSQL 12 + PostGIS on Ubuntu 20.4 (https://joets.medium.com/install-postgresql-12-postgis-on-ubuntu-20-4-in-5-mins-1b8948545185)

- Create database using ini_database.sql

- Change the UPLOAD_FOLDER and create_engine variables in both programs (app.py,data_proc.py) to reflect your environment.

- runn both programs: 

      python3 app.py
      python3 data_proc.py

- Check the file request_examples.py to see how upload files, get reports and status information.
