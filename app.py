import os
from ChitterApp.routes.home_route import home_route
from ChitterApp.routes.auth import auth
from ChitterApp.routes.user_routes import user_routes
from ChitterApp.routes.peep_routes import peep_routes
from flask import Flask
from ChitterApp.lib.database_connection import get_flask_database_connection
from flask_login import LoginManager
from ChitterApp.lib.repositories.user_repository import UserRepository
from ChitterApp.constants import UPLOAD_FOLDER


app = Flask(__name__, 
            template_folder='ChitterApp/templates', 
            static_folder='ChitterApp/static')
app.secret_key = 'your_secret_key_here'
app.jinja_env.autoescape = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    return repo.find_by_id(user_id)


app.register_blueprint(home_route, url_prefix='/')

app.register_blueprint(auth, url_prefix='/')

app.register_blueprint(user_routes, url_prefix='/')

app.register_blueprint(peep_routes, url_prefix='/')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
