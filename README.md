# Description

This challenge will evaluate your proficiency in Data Engineering, and your knowledge in
Software development as well.


# Assignment

Your task is to build an automatic process to ingest data on an on-demand basis. 
The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

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

# Solution

Data Base: Postgresql SQL database with PostGis extensions. 

Ingestion routine: **app.py** - rest api to upload the file to the server and put the file in the process queue. Request reports and process status. 

Process routine: **data_proc.py** - responsible to get the files from the queue, process and insert into postgres. 


## Steps
> $ git@github.com:fernandofrancis/Data_Engineering_Challenge.git
- Install PostgreSQL 12 + PostGIS on Ubuntu 20.4 (https://joets.medium.com/install-postgresql-12-postgis-on-ubuntu-20-4-in-5-mins-1b8948545185)

- Create database using ini_database.sql

- Change the UPLOAD_FOLDER and create_engine variables in both programs (app.py,data_proc.py) to reflect your environment:


    UPLOAD_FOLDER = '/home/mtuser/Documentos/josity' - Location where the files will be uploaded.    
    post_usu='postgres'     - Postegres user
    post_pass='PASSWD'      - Password
    post_ip='localhost'     - Postegres IP server
    post_port='5432'        - Postegres Port
    post_db='jobsity'       - Postegres database with postgis extention and ini_database.sql objects.

- run both programs: 

      python3 app.py
      python3 data_proc.py
- Check the file **request_examples.py** to see how to upload files, get reports and status information.


# Test using Docker Container

- Install the docker
- Load the docker image **app-challange.tar.gz** located in this repository.
	 > sudo docker load < app-challange.tar.gz
 - Create a docker volume with name  trips_csv
	  > sudo docker volume create  trips_csv
 - Change the **docker.env** file to reflect your target database. Do not change the CSV_PATH param.
 - Run the image 
	  > sudo docker run  -v trips_csv:/csv --env-file docker.env -p 5001:5000 -d app-challange
 - Run again now with de data_proc.py command
	  > sudo docker run -v trips_csv:/csv --env-file docker.env -d app-challange python3 data_proc.py 
 - The rest api is ready on port 5001. 
	 - Request  using bounding box exemple:
	  > import requests
	  > url = 'http://localhost:5001/'
      > url_region = 'http://127.0.0.1:5001/weekly/bbox/6.185303,43.436966,10.085449,45.836454'
	  > r = requests.get(url_region)
	  > print(r.json())

