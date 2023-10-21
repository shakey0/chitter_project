1. User requirements

As a Maker
So that I can let people know what I am doing
I want to post a message (peep) to chitter

As a maker
So that I can see what others are saying
I want to see all peeps in reverse chronological order

As a Maker
So that I can better appreciate the context of a peep
I want to see the time at which it was made

As a Maker
So that I can post messages on Chitter as me
I want to sign up for Chitter

As a Maker
So that only I can post messages on Chitter as me
I want to log in to Chitter

As a Maker
So that I can avoid others posting messages on Chitter as me
I want to log out of Chitter


2. Table data and properties

users: name, user_name, password, d_o_b, mood

peeps: content, date&time, likes

tags: name


3. Table connections

Can a user have many peeps? YES
Can a peep have many users? NO
Therefore user_id must be a value of peeps

Can a user like many peeps? YES
Can a peep be liked by many users? YES
Therefore a join table users_peeps is required

Can a user have many tags? YES
Can a tag have many users? YES
Therefore a join table users_tags is required

Can a peep have many tags? YES
Can a tag have many peeps? YES
Therefore a join table peeps_tags is required


4. Write the SQL

Completed in seeds/chitter_data.sql


5. Create the table
psql -h 127.0.0.1 chitter_project < seeds/chitter_data.sql