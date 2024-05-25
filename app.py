import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Import the SECRET_KEY from the config file
from config import SECRET_KEY
# Set up logging, with the log file located at /tmp/error.log and the log level set to DEBUG
logging.basicConfig(filename='/tmp/error.log', level=logging.DEBUG)

# Create a Flask application instance
app = Flask(__name__)
# Set the secret key for the Flask app, typically used to keep client sessions secure
app.config['SECRET_KEY'] = SECRET_KEY

# Configure CORS for all routes to allow access from all origins
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/app/send_command": {"origins": "http://localhost:8080"}})

# Configure the SQLAlchemy database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ll123456%23@localhost/Inventory_Sys'
# Disable SQLAlchemy track modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the User model for database operations
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Define the login route, only accepting POST requests
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Query the user
    user = User.query.filter_by(email=email).first()

    # Validate password (currently comparing plain text passwords directly)
    if user and user.password == password:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Email or password is incorrect"})

# Define the register route, only accepting POST requests
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match."})

    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters long."})

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return jsonify({"success": False, "message": "Email is already registered."})

    # Create a new user and insert it into the database
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "Registration successful."})

# Define the send command route, only accepting POST requests
@app.route('/send_command', methods=['POST'])
def send_command():
    # Ensure that the request contains JSON data, otherwise return a 400 error
    if not request.is_json:
        return jsonify({"success": False, "message": "Missing JSON in request"}), 400
    # Parse the `command` field from the JSON data
    data = request.get_json()
    command = data.get('command')
    print(f"Received command: {command}")  # Print to the server console

    # Response
    return jsonify({"success": True, "message": "Command received"})

@app.route('/')
def index():
    app.logger.debug('This is a debug message')
    return 'Hello, World!'

# Define a 500 error handler, log the error, and return a 500 error response
@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return "500 error", 500

# Uncomment to run the app on all interfaces, on port 8080
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
