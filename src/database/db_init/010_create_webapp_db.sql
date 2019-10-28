DROP DATABASE IF EXISTS webapp_db;
CREATE DATABASE webapp_db;
USE webapp_db;

CREATE TABLE accounts (
	uid		INTEGER PRIMARY KEY AUTO_INCREMENT,
	username	TINYTEXT NOT NULL UNIQUE,
	password	CHAR(128) NOT NULL,
	password_salt	CHAR(8) NOT NULL
);

CREATE TABLE videos (
	id		INTEGER PRIMARY KEY AUTO_INCREMENT,
	uploader	INTEGER NOT NULL,
	display_name	TINYTEXT,
	video_file	TEXT NOT NULL UNIQUE,
	upload_date DATE,
	CONSTRAINT videos_uploader_fk FOREIGN KEY (uploader)
		REFERENCES accounts(uid)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

GRANT ALL PRIVILEGES ON webapp_db.* TO 'sanders'@'%'
	IDENTIFIED BY 'One day, Ihaq will rise again!';
FLUSH PRIVILEGES;

