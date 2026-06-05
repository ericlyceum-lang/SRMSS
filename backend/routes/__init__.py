from flask import Blueprint

# Create blueprints for each module
auth_bp = Blueprint('auth', __name__, url_prefix='/api')
users_bp = Blueprint('users', __name__, url_prefix='/api')
vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/api')
drivers_bp = Blueprint('drivers', __name__, url_prefix='/api')
routes_bp = Blueprint('routes', __name__, url_prefix='/api')
schedules_bp = Blueprint('schedules', __name__, url_prefix='/api')
operations_bp = Blueprint('operations', __name__, url_prefix='/api')
fuel_bp = Blueprint('fuel', __name__, url_prefix='/api')
maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/api')
reports_bp = Blueprint('reports', __name__, url_prefix='/api')

# Import routes
from . import auth, users, vehicles, drivers, routes, schedules, operations, fuel, maintenance, reports

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(operations_bp)
    app.register_blueprint(fuel_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(reports_bp)