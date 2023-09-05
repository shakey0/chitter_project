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
  password text,
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

INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES ('Jody', 'jodesnode', 'Pass123!', '1993/08/06', 'calm');
INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES ('Sam', 'sammy1890', 'Word234*', '1999/02/27', 'excited');
INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES ('Johnson', 'son_of_john', 'Never00!', '1995/10/19', 'angry');
INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES ('Alice', 'mousey_14', 'Chitchat981!', '1982/05/31', 'content');
INSERT INTO users (name, user_name, password, d_o_b, current_mood) VALUES ('Rose', 'rosy_red', 'gatheR&45', '1993/05/15', 'calm');

INSERT INTO peeps (content, time, likes, user_id) VALUES ('I went to Summerfield park today.', '2022-08-10 19:10:25', 4, 1);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('This ice cream is amazing!', '2022-08-10 19:25:06', 7, 2);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('It''s a brilliant day for the beach.', '2022-08-10 20:46:40', 2, 3);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Who wants to go for food tonight?', '2022-08-11 15:22:33', 5, 2);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Photos from my holiday in spain.', '2022-08-23 10:02:03', 10, 1);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Delicious 4 cheese pizza I made!', '2022-08-31 18:52:58', 24, 4);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('A brilliant book about magic.', '2022-08-31 19:30:29', 8, 2);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Italy is a brilliant place to visit!', '2022-09-27 23:49:14', 4, 5);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('A perfect day for a picnic.', '2022-09-28 14:15:24', 0, 3);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Merry Christmas everyone!', '2022-12-25 07:00:01', 12, 3);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Happy New Year from South Korea!', '2023-01-01 00:04:56', 130, 1);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Party at mine tonight!', '2023-01-15 16:35:50', 3, 5);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('My fantastic lego house!', '2023-02-10 19:45:00', 1602, 2);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('A picture I painted in Turkey.', '2023-05-30 11:02:59', 45330, 4);
INSERT INTO peeps (content, time, likes, user_id) VALUES ('Kayaking at the lake.', '2023-05-30 17:59:04', 56, 4);

INSERT INTO tags (name) VALUES ('#DaysOut');
INSERT INTO tags (name) VALUES ('#Food');
INSERT INTO tags (name) VALUES ('#Travel');
INSERT INTO tags (name) VALUES ('#Hobbies');
INSERT INTO tags (name) VALUES ('#Festivals');
INSERT INTO tags (name) VALUES ('#Music');
INSERT INTO tags (name) VALUES ('#Art');
INSERT INTO tags (name) VALUES ('#Nature');
INSERT INTO tags (name) VALUES ('#Social');
INSERT INTO tags (name) VALUES ('#Work');
INSERT INTO tags (name) VALUES ('#Creative');
INSERT INTO tags (name) VALUES ('#Books');

INSERT INTO users_peeps (user_id, peep_id) VALUES (1, 3);
INSERT INTO users_peeps (user_id, peep_id) VALUES (1, 7);
INSERT INTO users_peeps (user_id, peep_id) VALUES (1, 12);
INSERT INTO users_peeps (user_id, peep_id) VALUES (1, 14);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 3);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 4);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 8);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 10);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 11);
INSERT INTO users_peeps (user_id, peep_id) VALUES (2, 15);
INSERT INTO users_peeps (user_id, peep_id) VALUES (3, 1);
INSERT INTO users_peeps (user_id, peep_id) VALUES (3, 2);
INSERT INTO users_peeps (user_id, peep_id) VALUES (3, 7);
INSERT INTO users_peeps (user_id, peep_id) VALUES (3, 8);
INSERT INTO users_peeps (user_id, peep_id) VALUES (3, 14);
INSERT INTO users_peeps (user_id, peep_id) VALUES (4, 1);
INSERT INTO users_peeps (user_id, peep_id) VALUES (4, 4);
INSERT INTO users_peeps (user_id, peep_id) VALUES (4, 5);
INSERT INTO users_peeps (user_id, peep_id) VALUES (4, 6);
INSERT INTO users_peeps (user_id, peep_id) VALUES (4, 8);
INSERT INTO users_peeps (user_id, peep_id) VALUES (5, 10);
INSERT INTO users_peeps (user_id, peep_id) VALUES (5, 11);
INSERT INTO users_peeps (user_id, peep_id) VALUES (5, 13);
INSERT INTO users_peeps (user_id, peep_id) VALUES (5, 14);
INSERT INTO users_peeps (user_id, peep_id) VALUES (5, 15);

INSERT INTO users_tags (user_id, tag_id) VALUES (1, 1);
INSERT INTO users_tags (user_id, tag_id) VALUES (1, 3);
INSERT INTO users_tags (user_id, tag_id) VALUES (1, 5);
INSERT INTO users_tags (user_id, tag_id) VALUES (2, 2);
INSERT INTO users_tags (user_id, tag_id) VALUES (2, 4);
INSERT INTO users_tags (user_id, tag_id) VALUES (3, 1);
INSERT INTO users_tags (user_id, tag_id) VALUES (3, 2);
INSERT INTO users_tags (user_id, tag_id) VALUES (3, 5);
INSERT INTO users_tags (user_id, tag_id) VALUES (4, 1);
INSERT INTO users_tags (user_id, tag_id) VALUES (4, 3);
INSERT INTO users_tags (user_id, tag_id) VALUES (4, 4);
INSERT INTO users_tags (user_id, tag_id) VALUES (5, 5);

INSERT INTO peeps_tags (peep_id, tag_id) VALUES (1, 1);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (1, 8);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (2, 2);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (3, 1);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (4, 2);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (4, 9);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (5, 3);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (5, 8);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (6, 2);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (6, 4);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (6, 7);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (7, 4);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (7, 12);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (8, 3);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (9, 1);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (9, 2);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (9, 8);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (10, 3);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (11, 3);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (11, 5);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (12, 6);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (12, 9);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (13, 4);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (13, 11);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (14, 3);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (14, 4);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (14, 7);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (14, 8);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (14, 11);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (15, 1);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (15, 4);
INSERT INTO peeps_tags (peep_id, tag_id) VALUES (15, 8);

INSERT INTO peeps_images (file_name, peep_id) VALUES ('Megeve_SimonGarnier_150119_004.jpg', 14)