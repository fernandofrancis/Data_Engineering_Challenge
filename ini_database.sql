## Create the database and extention
CREATE DATABASE jobsity;
###conect to jobsity database 
CREATE EXTENSION postgis;


CREATE TABLE  IF NOT EXISTS  trips (
    id integer PRIMARY KEY,
    region character varying(50),
    origin_coord geography(Point,4326),
    destination_coord geography(Point,4326),
    datetime timestamp without time zone,
    geometry geometry(LineString,4326),
    geometry_wkb bytea,
    qty integer
);

CREATE INDEX IF NOT EXISTS trip_geometry_idx
  ON trips USING GIST (geometry);

CREATE INDEX IF NOT EXISTS trip_region_idx
  ON trips  (region);

CREATE TABLE IF NOT EXISTS datasource (
    id integer,
    datasource character varying(50),
	FOREIGN KEY (id) REFERENCES trips(id)
);

CREATE INDEX IF NOT EXISTS datasource_id_idx
  ON datasource  (id);
  
CREATE TABLE csv_files (
    id_uuid uuid PRIMARY KEY,
    file_name text,
    datetime timestamp without time zone,
    status character varying(30) DEFAULT 'Queued'::character varying,
    datetime_proc timestamp without time zone
);

CREATE INDEX IF NOT EXISTS csv_files_uuid_idx
  ON csv_files  (id_uuid);

CREATE TABLE queue_table (
    id integer NOT NULL,
    queue_time timestamp DEFAULT now(),
    id_uuid uuid,
    file_name text,
    file_name_proc text
);

CREATE INDEX IF NOT EXISTS queue_table_id_idx
  ON queue_table  (id);



