# Chitter Project

## Introduction

The Chitter Project was a solo project at the end of week 6 of the Makers Academy web development module. The outline of the project was to create a social media type web app like Twitter or Facebook.
Having started the project and getting a lot of the foundations of the backend established by the end of week 6, I was very keen to finish it. This is the first web app project I have done on my own, and so I've had the great opportunity of learning a lot from it. I've also experimented a great deal during this project, particularly with the layouts and styles of everything, to get a web app that looked aesthetically pleasing. I've put a lot of work into the backend of the app, to try and get it to run as smoothly as possible. I've written a comprehensive set of tests too which cover almost all the things a user of the app might do.

## Features

**Top Bar** - This is fixed at the top of the screen of the Homepage, Sign Up page and User page. While unauthenticated and on the homepage or sign up page, this top bar contains the username and password fields with a log in button, as well as a sign up button. While authenticated and on the homepage, this bar contains a 'List by tag' dropdown menu, a 'Change mood' dropdown menu, the user's username, and a view profile and log out button. While authenticated and on the user page, this bar contains a view profile and log out button as well as the user whose profile is being viewed. The top bar always has a home button on the far lefthand side.

**Homepage** - Shows all the peeps posted by all users. Peeps have a 'Like' button (if the user is authenticated) so users can like each others' peeps, a list of tags at the bottom which relate to the topic(s) of the peep, a link with the username to the user who posted the peep, and the time and date of post. For peeps that belong to the logged in user, they also have an 'Amend tags' and 'Delete' button. If the peep includes pictures a button saying 'Peep at the pictures' is included.

**Sign Up Page** - This contains a form with all the information you'd expect on a sign up form. Once the new user completes this form, they will be automatically logged in.

**User Page** - Contains a card with information about the user. If the user is on their own profile page, they can also change their mood (as they also can on the homepage), select their preferred tags, change their password, and delete their profile. (I have put extensive security measures around password changing and profile deleting.) Then below the user info card, are all the peeps the user has posted (these take the same format as on the homepage). Originally I planned to make a separate page for the user's peeps, but in the end I decided to include them in the user's profile.

**Change Password Page** - This is actually a modified webpage from another mini (one day) project I did - Password Checker. I took the html file from that project and integrated it with this project, making all the necessary changes. It does what you'd expect a change password page to do, checking the user's old password and asking for the new password twice. I have done a lot of work on the backend to make sure this part of the site is secure.

**Delete Profile Page** - This was one of the last parts of the app I did. This page includes a number of sections to vary that the user actually wants to delete their profile and check the authenticity of the user. There are also stages to deal with errors. The backend handles which part of the page will be rendered, using extensive security measures to ensure all authenication steps are passed.

## Key Technologies
- Python
- Flask
- PostgreSQL
- Javascript
- AJAX
- Bcrypt
- Redis
- Playwright

## Installation & Setup - In progress (may need changing)

Run the following command to clone the repo:
```bash
git clone https://github.com/shakey0/chitter_project
cd chitter_project
```

Create your virtual environment:
```bash
pipenv install
pipenv shell
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the following commands to create the dev and test databases:
```bash
createdb chitter_project
createdb chitter_project_test
python seed_dev_database.py
```

Create a .env file with the following:
```bash
SECRET_KEY=<YOUR_SECRET_KEY>
REDIS_PASSWORD=<YOUR_REDIS_PASSWORD_IF_YOU_SET_ONE>
```

Run the tests:
```bash
pytest
```

Start the server:
```bash
python app.py
```