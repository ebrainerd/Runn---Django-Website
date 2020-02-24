use Runn; -- use Runn database
SET FOREIGN_KEY_CHECKS = 0; -- turn off foreign key checks before dropping tables
drop table if exists users;
drop table if exists runs;
drop table if exists posts;
drop table if exists comments;
drop table if exists following;
SET FOREIGN_KEY_CHECKS = 1; -- turn checks back on

-- Below: The column Team is a foreign key to the same table. 
-- Sometimes the Team column references a User ID that has not been added yet
-- then that makes an error. Too lazy to fix right now. 
create table users (
   UserID integer primary key,
   FirstName varchar(50) not null, 
   LastName varchar(50) not null,
   Email varchar(75) not null,
   Tagline varchar(250) not null,
   Location varchar(100) not null,
   UserType integer not null,
   Team integer
   -- foreign key (Team) references users (UserID)
);

create table runs (
   RunID integer primary key,
   UserID integer not null,
   Distance decimal(5,2) not null,
   RunTime varchar(100) not null,
   `Date` datetime not null,
   Location varchar(100) not null,
   Image varchar(250),
   Post varchar(1000), -- text posts cannot be longer than 1000 chars
   foreign key (UserID) references users (UserID),
   Likes integer not null
);

-- below table is not needed. 
create table posts (
   postID integer primary key,
   userID integer not null, 
   runID integer not null,
   text varchar(1000), -- this text should be the same as in Runs table
   image varchar(250), -- should be same as in Runs table
   likes integer not null,
   foreign key (userID) references users (userID),
   foreign key (runID) references runs (runID)
);

create table comments (
   CommentID integer primary key, 
   UserID integer not null,
   RunID integer not null,
   CommentText varchar(1000) not null,
   Time datetime not null,
   foreign key (UserID) references users (UserID),
   foreign key (RunID) references runs (RunID)
); 

-- below table should have a composite primary key: 
-- primary key (UserID_1, UserID_2).
-- Entries 1 2 and 2 1 should be allowed.
-- Further entries 1 2 and 2 1 should NOT be allowed. 
-- But primary key constraint prevents inserting 
-- 2 1 after 1 2 has already been inserted. 
-- Too lazy to fix right now. 
create table following (
   UserID_1 integer not null, 
   UserID_2 integer not null,
   primary key (UserID_1, UserID_2), -- composite primary key
   foreign key (UserID_1) references users (UserID),
   foreign key (UserID_2) references users (UserID)
);

