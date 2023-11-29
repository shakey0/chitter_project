# Chitter Project

https://chitter-by-shakey0.onrender.com/

## Introduction

Welcome to the Chitter Project! Conceived during week 6 of the Makers Academy web development module, Chitter is a solo undertaking aimed at emulating the features and functionalities of popular social media platforms like Twitter and Facebook. This project represents my maiden voyage into independent web app development, serving as both a challenging task and a profound learning experience. Throughout its development, I've focused extensively on the app's aesthetics, backend functionality, and efficient database interactions. To enhance performance, I tackled the N+1 problem, optimizing queries to ensure smooth, responsive user experiences. In addition to ensuring smooth operations, I've emphasized the importance of comprehensive testing, ensuring that the app is well-prepared for various user interactions and robust under different loads.

## Features

### Main Features

**Nav Bar** - Universally accessible from the Homepage, Sign Up page, and User page. It adapts its content based on the user's authentication status, presenting options ranging from login fields to profile management tools.

**Homepage** - Displays posts ("peeps") from all users, with features such as 'Like' buttons, tags, user links, and post timestamps. Users have added controls over their own posts, like editing tags or deleting the peep.

**Sign Up Page** - A straightforward registration page that automatically logs in users upon successful sign-up.

**User Page** - A user-centric dashboard displaying personal details and their peeps. It doubles as a personal management hub, offering options to update mood, manage tags, change passwords, and even delete profiles.

**Change Password Page** - A secure section, repurposed from my "Password Checker" project, which ensures safe password changes by verifying the old password and confirming the new one.

**Delete Profile Page** -  A meticulously designed interface that requires multiple layers of user verification before allowing profile deletion, bolstered by backend security checks to maintain data integrity and user safety.

### Highlighted Features

- Checks if a post ("peep") contains any bad words before adding it to the database.
    - [See here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/peep_repository.py#L88-L97)
    - If any bad words are found, an error message will be returned to the user. Of course the words 'daily mail' are included here.
- Has a complex part of the 'get' query in the PeepRepository class '[see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/peep_repository.py#L28-L38)' to check if a user likes a peep or not, which displays either the 'Like' OR 'Liked' button on the page.
    - See handling in [index.html](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/templates/index.html#L150-L160).
- Has a method '[check_valid_d_o_b](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/user_repository.py#L95-L110)' to check the dates the user entered exist. For example, if the user tries to enter 31 April, an error will be thrown, and the same if the user tries to enter 29 February 2001, since February only had 28 days in that year.
- If a peep or user is deleted, all images associated with the peep or user's peeps will be removed.
    - [See in the delete method in PeepRepository](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/peep_repository.py#L160-L163)
    - [See in the delete method in UserRepository](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/user_repository.py#L213-L226)
- Uses Flask to send different parts of a html template to the frontend.
    - (Best example in [delete_user.html](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/templates/delete_user.html#L11-L107))

### Security Features (Redis)

- Has a sophisticated '[delete user route](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/user_routes.py#L151-L255)' that generates a random secret token, caches it in Redis for 10 minutes ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/user_routes.py#L165-L168)) and sends it to the frontend which sends it back to the backend ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/templates/delete_user.html#L55-L57)) to check authenticity. Finally all 4 of these secret tokens are sent to the user repository class delete method ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/repositories/user_repository.py#L206-L211)) and checked against the values cached in Redis.
- Uses Redis to cache failed attempts at logging in as a specific user ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/auth.py#L18-L20)). If the wrong password is entered 5 times for the same user, login for this user will be prevented for 2 minutes.
    - See the [timeout function](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/constants.py#L10-L22) in constants.py . This function is also called by the [/change_password](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/user_routes.py#L118-L121) route and (at stages 2, 3 and 4 of) the [/delete_user](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/user_routes.py#L206-L208) route.
- Uses Redis to cache how many peeps a user has posted in the last 24 hours ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/peep_routes.py#L59-L62)), limiting each user to 5 peeps within a 24 hour window.
- Has a sophisticated check to ensure images cannot be larger than 2 MB and the total images per peep cannot be larger than 5 MB ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/peep_routes.py#L26-L40)). Also limits users to only 2 peeps with images within a 24 hour window ([see here](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/routes/peep_routes.py#L51-L54)).

## Deployment & CI/CD Pipeline Process

1. Used Docker to containerise the app and Redis on my local machine.
    - [See Dockerfile](https://github.com/shakey0/chitter_project/blob/main/Dockerfile)
2. Connected it to the PostgreSQL database on my local machine by creating a new Postgres user named 'chitter_docker' and giving this user full permissions for the chitter_project database.
    - [See in database_connection.py](https://github.com/shakey0/chitter_project/blob/main/ChitterApp/lib/database_connection.py#L27-L29)
    - [See in chitter_data_w_auth.sql](https://github.com/shakey0/chitter_project/blob/main/seeds/chitter_data_w_auth.sql#L70-L90)
3. Attached a Docker Volume to get the uploaded images to persist.
4. Configured the database_connection.py file to connect to the database instance on ElephantSQL by adding the URL in an environment variable named 'DATABASE_URL'.
5. Created a script - seed_prod_database.py (gitignored) - to seed the database instance on ElephantSQL.
6. Created a script - deploy.yml - to build and test the app in GitHub Actions.
7. Created a new web service in Render with an attached persistence disk for the uploaded images.
8. Configured GitHub to give Render the necessary permissions on this repository, so each time a new push is made to the main branch, and the tests pass, the latest version of the app will be deployed to Render.

## Key Technologies

- **Backend:** Python, Flask, PostgreSQL
- **Frontend:** JavaScript, AJAX, CSS, HTML
- **Security:** Bcrypt, Redis
- **Testing:** Pytest, Playwright
- **Deployment:** Docker, ElephantSQL, GitHub Actions, Render

## Database Tables

**Main Tables** - The id in each of these tables is the primary key.

- **users** (id, name, user_name, password, d_o_b, current_mood) - <em>one-to-many with peeps through user_id, many-to-many with peeps through users_peeps, many-to-many with tags through users_tags</em>
- **peeps** (id, content, time, likes, user_id [FK - users.id]) - FK connects peep to user - <em>many-to-many with users through users_peeps, one-to-many with peeps_images through peep_id, many-to-many with tags through peeps_tags</em>
- **peeps_images** (id, file_name, peep_id [FK - peeps.id]) - FK connects image to peep
- **tags** (id, name) - <em>many-to-many with users through users_tags, many-to-many with peeps through peeps_tags</em>

**Join Tables** - The values here all reference the main tables.

- **users_peeps** (user_id, peep_id) - To keep track of which users like which peeps
- **users_tags** (user_id, tag_id) - To keep track of which users prefer which tags
- **peeps_tags** (peep_id, tag_id) - To keep track of which peeps have which tags

## Installation & Setup

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
(If you haven't, install and setup PostgreSQL on your machine.)
```bash
createdb chitter_project
createdb chitter_project_test
python seed_dev_database.py
```

Create a .env file with the following:
(If you haven't, install and setup Redis on your machine.)
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

Test/Initial User Accounts (Username - Password):
- jodesnode - Pass123!
- sammy1890 - Word234*
- son_of_john - Never00!
- mousey_14 - Chitchat981!
- rosy_red - gatheR&45

## Future Enhancements

This is a list of things I would add to the project if I had more time:
- Modify the get_all method in the PeepRepository class to only get about 20-30 peeps at a time for display on the webpage. The will improve scalability.
    - If a user scrolls down more peeps will be loaded.
- 'Like button' on image pop up box
- 'Amend pictures button' for the user's own peeps
- 'Edit peep button' so the user can edit the text in their peeps. The original text as well as the edited text would be saved.
- Add administrator users who can delete abusive peeps and ban unruly users.
- ***Introducing Chitter Spaces***, where a user can create a space and invite other users to that space. Users part of the space can then see peeps from other users that are part of that space. Users can change spaces using a dropdown menu on the nav bar that lists all the spaces they are part of. Spaces will only be visible by invite.