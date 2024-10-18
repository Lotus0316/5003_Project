BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Class" (
	"cid"	VARCHAR(16),
	"semester"	VARCHAR(16) NOT NULL,
	"cname"	VARCHAR(64) NOT NULL,
	"room"	VARCHAR(64) NOT NULL,
	"ctime"	VARCHAR(64) NOT NULL,
	"info"	TEXT,
	PRIMARY KEY("cid")
);
CREATE TABLE IF NOT EXISTS "Student" (
	"sid"	INTEGER,
	"name"	VARCHAR(64) NOT NULL,
	"cur_major"	VARCHAR(64) NOT NULL,
	"email"	VARCHAR(64),
	"info"	TEXT,
	PRIMARY KEY("sid")
);
CREATE TABLE IF NOT EXISTS "Student_Class" (
	"sid"	INTEGER,
	"cid"	VARCHAR(16),
	PRIMARY KEY("sid","cid"),
	FOREIGN KEY("sid") REFERENCES "Student"("sid")
	FOREIGN KEY("cid") REFERENCES "Class"("cid")
);
CREATE TABLE IF NOT EXISTS "Team" (
	"tid"	INTEGER,
	"tname"	VARCHAR(64),
	"leader_id"	INTEGER NOT NULL,
	"cid"	INTEGER NOT NULL,
	"is_recruiting"	INTEGER NOT NULL,
	"info"	TEXT,
	PRIMARY KEY("tid" AUTOINCREMENT),
	FOREIGN KEY("leader_id") REFERENCES "Student"("sid")
);
CREATE TABLE IF NOT EXISTS "Team_Member" (
	"tid"	INTEGER,
	"cid"	INTEGER,
	"sid"	INTEGER,
	PRIMARY KEY("tid","cid","sid"),
	FOREIGN KEY("cid") REFERENCES "Class"("cid"),
	FOREIGN KEY("sid") REFERENCES "Student"("sid"),
	FOREIGN KEY("tid") REFERENCES "Team"("tid")
);
CREATE TABLE IF NOT EXISTS "Team_Request" (
	"sid"	INTEGER,
	"cid"	VARCHAR(16),
	"info"	TEXT,
	PRIMARY KEY("sid","cid"),
	FOREIGN KEY("cid") REFERENCES "Class"("cid"),
	FOREIGN KEY("sid") REFERENCES "Student"("sid")
);
COMMIT;
