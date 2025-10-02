import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from db import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Use PostgreSQL from environment
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }
    print(f"Using PostgreSQL database")
else:
    # Fallback to SQLite for development
    abs_db_path = os.path.abspath(os.path.join('data', 'hospital.db'))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{abs_db_path}"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    print(f"Using SQLite database: {abs_db_path}")

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()

# Import routes
import routes

# Create admin user after everything is initialized
try:
    with app.app_context():
        routes.create_admin()
except Exception as e:
    print(f"Error creating admin user: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
