/* Debug code*/
/*
  select * from user;
  select * from active_user;
  insert into active_users(email,token) values('jt@live.com','123456');
*/
/*DROP TABLE IF EXISTS active_users;*/
/*DROP TABLE IF EXISTS user_messages;*/
/*DROP TABLE IF EXISTS user;*/

/*
CREATE TABLE IF NOT EXISTS user (
     email TEXT PRIMARY KEY,
     password TEXT,
     firtname TEXT,
     familyname TEXT,
     gender TEXT,
     city TEXT,
     country TEXT
   ) ;
*/

/*CREATE TABLE IF NOT EXISTS active_users (
    email TEXT PRIMARY KEY,
    token TEXT,
    FOREIGN KEY(email) REFERENCES user(email)
) ;*/

/*
CREATE TABLE IF NOT EXISTS user_messages (
    reciever TEXT,
    message TEXT,
    sender TEXT,
    FOREIGN KEY (reciever) REFERENCES user(email)
);*/
