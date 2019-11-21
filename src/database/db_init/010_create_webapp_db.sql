DROP DATABASE IF EXISTS webapp_db;
CREATE DATABASE webapp_db;
USE webapp_db;

DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS videos;

CREATE TABLE accounts (
	userID	INTEGER PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(248) NOT NULL UNIQUE,
	pass_hash VARCHAR(248) NOT NULL,
	TotalVideoCount INTEGER NOT NULL DEFAULT 0,
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE videos (
	vidID	INTEGER PRIMARY KEY AUTO_INCREMENT,
	userID	INTEGER NOT NULL,
	videoTitle	VARCHAR(248),
	fileName    VARCHAR(248) NOT NULL UNIQUE,
	videoURL	VARCHAR(248),  # NOT NULL UNIQUE,
	upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT videos_uploader_fk FOREIGN KEY (userID)
		REFERENCES accounts(userID)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);


GRANT ALL PRIVILEGES ON webapp_db.* TO 'root'@'0.0.0.0'
	IDENTIFIED BY 'toor';
FLUSH PRIVILEGES;

