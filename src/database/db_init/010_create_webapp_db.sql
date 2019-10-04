DROP DATABASE IF EXISTS webapp_db;
CREATE DATABASE webapp_db;
USE webapp_db;

CREATE TABLE accounts (
	uid		INTEGER PRIMARY KEY,
	username	TINYTEXT NOT NULL UNIQUE,
	password	CHAR(128)
);

CREATE TABLE videos (
	id		INTEGER PRIMARY KEY,
	uploader	INTEGER NOT NULL,
	display_name	TINYTEXT,
	video_file	TEXT NOT NULL UNIQUE,
	CONSTRAINT videos_uploader_fk FOREIGN KEY (uploader)
		REFERENCES accounts(uid)
);

