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


2. Pages/Routes

@app.route("/")
# display the homepage with all peeps in reverse chronological order
# include a topbar menu with login(username&password)/signup OR logout, view_profile options IF logged in
# include an option to change current mood IF logged in - dropdown menu
# include an add peep box above the list of peeps IF the user is logged in
# for each peep that belongs to the user, include a delete button
# for each peep that belongs to the user, include an ammend tags button
# include a search_peep_by_tag in the top menu
# make the usernames for peeps clickable and send to a page to view the user's details

@app.route("/signup")
# fields - name, username, d_o_b, password, confirm_password (mood already set to content)
# choose favourite_tags

@app.route("/user/<id>")
# display the user's name, username, age&d_o_b, current mood, favourite_tags
# IF the username matches the logged in user INCLUDE BELOW:
# include an option to change password
# show all tags and allow selection and deselection
# include an option to review peeps and delete them

@app.route("/user-peeps/<id>)
# show all peeps the user has posted
# have a delete button next to them all
