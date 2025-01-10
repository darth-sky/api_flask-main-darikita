"""Small apps to demonstrate endpoints with basic feature - CRUD"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from api.books.endpoints import books_endpoints
from api.authors.endpoints import authors_endpoints
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints
from config import Config
from static.static_file_server import static_file_server
from api.donation_project.endpoints import donation_projects_endpoints
from api.blood_donation_project.endpoints import blood_donation_projects_endpoints
from api.volunteer_project.endpoints import volunteer_projects_endpoints

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


jwt.init_app(app)

# register the blueprint
app.register_blueprint(auth_endpoints, url_prefix='/api/v1/auth')
app.register_blueprint(protected_endpoints,
                       url_prefix='/api/v1/protected')
app.register_blueprint(books_endpoints, url_prefix='/api/v1/books')
app.register_blueprint(authors_endpoints, url_prefix='/api/v1/authors')
app.register_blueprint(static_file_server, url_prefix='/static/')
app.register_blueprint(donation_projects_endpoints,
                       url_prefix='/api/v1/donation_projects')
app.register_blueprint(blood_donation_projects_endpoints,
                       url_prefix='/api/v1/blood_donation_projects')
app.register_blueprint(volunteer_projects_endpoints,
                       url_prefix='/api/v1/volunteer_projects')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
