-- Drop the tables if they already exist when the database is initialised.
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comments;

-- Creates the table called user that will store all user details following registration by the admin.
CREATE TABLE user (
  -- The user ID is AUTOINCREMENTED meaning the user ID's are automatically numbered in sequence.
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  -- TEXT UNIQUE means the username cannot be the same as any others.
  username TEXT UNIQUE NOT NULL,
  -- TEXT NOT NULL means the field must be filled.
  password TEXT NOT NULL,
  role TEXT NOT NULL
);
-- The post table holds all of the information about the uploaded resource.
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  -- Current timestamp records the current time to add this to the details about the resource upload.
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  body2 TEXT NOT NULL,
  module,
  topic,
  -- The foreign key author_id relates to the primary key id from the user table.
  -- These 2 tables can be joined using this key relationship.
  FOREIGN KEY (author_id) REFERENCES user (id)
);

-- The comments table holds all of the data when the student adds a comment and a tutor replies to a comment.
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  module,
  priority,
  reply,
  -- The foreign key author_id relates to the primary key id from the user table.
  -- These 2 tables can be joined using this key relationship.
  FOREIGN KEY (author_id) REFERENCES user (id)
);