import os
from flask import Flask, request, redirect, render_template
from lib.database_connection import get_flask_database_connection


app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
