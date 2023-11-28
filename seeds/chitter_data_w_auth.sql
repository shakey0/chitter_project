DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS peeps CASCADE;
DROP SEQUENCE IF EXISTS peeps_id_seq;
DROP TABLE IF EXISTS tags CASCADE;
DROP SEQUENCE IF EXISTS tags_id_seq;
DROP TABLE IF EXISTS users_peeps;
DROP SEQUENCE IF EXISTS users_peeps_id_seq;
DROP TABLE IF EXISTS users_tags;
DROP SEQUENCE IF EXISTS users_tags_id_seq;
DROP TABLE IF EXISTS peeps_tags;
DROP SEQUENCE IF EXISTS peeps_tags_id_seq;
DROP TABLE IF EXISTS peeps_images;
DROP SEQUENCE IF EXISTS peeps_images_id_seq;


CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name text,
  user_name text,
  password bytea,
  d_o_b date,
  current_mood text
);

CREATE TABLE peeps (
  id SERIAL PRIMARY KEY,
  content text,
  time timestamp,
  likes int,
  user_id INT REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name text
);

CREATE TABLE users_peeps (
  user_id int,
  peep_id int,
  constraint fk_user foreign key(user_id) references users(id) on delete cascade,
  constraint fk_peep foreign key(peep_id) references peeps(id) on delete cascade,
  PRIMARY KEY (user_id, peep_id)
);

CREATE TABLE users_tags (
  user_id int,
  tag_id int,
  constraint fk_user foreign key(user_id) references users(id) on delete cascade,
  constraint fk_tag foreign key(tag_id) references tags(id) on delete cascade,
  PRIMARY KEY (user_id, tag_id)
);

CREATE TABLE peeps_tags (
  peep_id int,
  tag_id int,
  constraint fk_peep foreign key(peep_id) references peeps(id) on delete cascade,
  constraint fk_tag foreign key(tag_id) references tags(id) on delete cascade,
  PRIMARY KEY (peep_id, tag_id)
);

CREATE TABLE peeps_images (
  id SERIAL PRIMARY KEY,
  file_name text,
  peep_id INT REFERENCES peeps(id) ON DELETE CASCADE
);


GRANT USAGE ON SEQUENCE users_id_seq TO chitter_docker;
GRANT USAGE ON SEQUENCE peeps_id_seq TO chitter_docker;
GRANT USAGE ON SEQUENCE tags_id_seq TO chitter_docker;
GRANT USAGE ON SEQUENCE peeps_images_id_seq TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON peeps TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON tags TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON users_peeps TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON users_tags TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON peeps_tags TO chitter_docker;
GRANT SELECT, INSERT, UPDATE, DELETE ON peeps_images TO chitter_docker;
GRANT REFERENCES ON users TO chitter_docker;
GRANT REFERENCES ON peeps TO chitter_docker;
GRANT REFERENCES ON tags TO chitter_docker;
GRANT TRIGGER ON users TO chitter_docker;
GRANT TRIGGER ON peeps TO chitter_docker;
GRANT TRIGGER ON tags TO chitter_docker;
GRANT CONNECT ON DATABASE chitter_project TO chitter_docker;
GRANT TEMP ON DATABASE chitter_project TO chitter_docker;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO chitter_docker;
GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA public TO chitter_docker;