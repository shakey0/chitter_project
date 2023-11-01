# Chitter Project

## Introduction

Welcome to the Chitter Project! Conceived during week 6 of the Makers Academy web development module, Chitter is a solo undertaking aimed at emulating the features and functionalities of popular social media platforms like Twitter and Facebook. This project represents my maiden voyage into independent web app development, serving as both a challenging task and a profound learning experience. Throughout its development, I've focused extensively on the app's aesthetics and backend functionality. In addition to ensuring smooth operations, I've emphasized the importance of comprehensive testing, ensuring that the app is well-prepared for various user interactions.

## Features

**Nav Bar** - Universally accessible from the Homepage, Sign Up page, and User page. It adapts its content based on the user's authentication status, presenting options ranging from login fields to profile management tools.

**Homepage** - Displays posts ("peeps") from all users, with features such as 'Like' buttons, tags, user links, and post timestamps. Users have added controls over their own posts, like editing tags or deleting the peep.

**Sign Up Page** - A straightforward registration page that automatically logs in users upon successful sign-up.

**User Page** - A user-centric dashboard displaying personal details and their peeps. It doubles as a personal management hub, offering options to update mood, manage tags, change passwords, and even delete profiles.

**Change Password Page** - A secure section, repurposed from my "Password Checker" project, which ensures safe password changes by verifying the old password and confirming the new one.

**Delete Profile Page** -  A meticulously designed interface that requires multiple layers of user verification before allowing profile deletion, bolstered by backend security checks to maintain data integrity and user safety.

## Key Technologies

- **Backend:** Python, Flask, PostgreSQL
- **Frontend:** Javascript, AJAX
- **Security:** Bcrypt, Redis
- **Testing:** Playwright

## Database Tables

**Main Tables** - The id in each of these tables is the primary key.

- **users** (id, name, user_name, password, d_o_b, current_mood)
- one-to-many with peeps through user_id, many-to-many with peeps through users_peeps, many-to-many with tags through users_tags
- **peeps** (id, content, time, likes, user_id [FK - users.id]) - FK connects peep to user
- one-to-many with peeps_images through peep_id, many-to-many with tags through peeps_tags
- **peeps_images** (id, file_name, peep_id [FK - peeps.id]) - FK connects image to peep
- **tags** (id, name)
- many-to-many with users through users_tags, many-to-many with peeps through peeps_tags

**Join Tables** - The values here all reference the main tables.

- **users_peeps** (user_id, peep_id) - To keep track of which users likes which peeps
- **users_tags** (user_id, tag_id) - To keep track of which users prefers which tags
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

Test/Initial User Accounts (Username - Password):
- jodesnode - Pass123!
- sammy1890 - Word234*
- son_of_john - Never00!
- mousey_14 - Chitchat981!
- rosy_red - gatheR&45

## Future Enhancements

This is a list of things I would add to the project if I had more time:
- Like button on image pop up box
- Amend pictures button for the user's own peeps
- Edit peep button, so the user can edit the text in their peeps. The original text as well as the edited text would be saved.
- **Introducing Chitter Spaces**, where a user can create a space and invite other users to that space. Users part of the space can then see peeps from other users that are part of that space. Users can change spaces using a dropdown menu on the nav bar that lists all the spaces they are part of. Spaces will only be visible by invite.