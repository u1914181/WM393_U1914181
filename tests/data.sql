-- User is the first table in schema.sql. For each user, their username, password and role (job)
-- is stored in this table and is then retried by the Python code.
INSERT INTO user (username, password, role)
VALUES
-- The values that are inserted are of the same type as the original sql database i.e. the usernames are strings,
-- the passwords are hashed and encoded and the roles are Tutors or Students.
  ('TestUsername', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'Tutor'),
  ('TestUsername2', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'Tutor');

-- Post is the second table in schema.sql. This table stores information regarding what has been uploaded
-- to the resource board. The lecturer specifies the title, writes some information about the resource
-- (body), the author ID is automatically saved to the database as is the date and time it was created. body2
-- is the name of the uploaded file. The module and topic are also selected by the lecturer using a dropdown menu.
INSERT INTO post (title, body, author_id, created, body2, module, topic)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00', 'Testfile.txt', 'WM393', 'Assessments');