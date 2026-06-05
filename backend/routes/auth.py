from flask import request, jsonify
from database import get_db
from . import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username=? AND password=?', 
        (username, password)
    ).fetchone()
    db.close()
    
    if user:
        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
        })
    
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@auth_bp.route('/stats')
def stats():
    """Get dashboard statistics"""
    db = get_db()
    
    stats_data = {
        "vehicles": db.execute('SELECT COUNT(*) FROM vehicles').fetchone()[0],
        "drivers": db.execute('SELECT COUNT(*) FROM drivers').fetchone()[0],
        "trips": db.execute("SELECT COUNT(*) FROM schedules").fetchone()[0],
        "pending_fuel": db.execute("SELECT COUNT(*) FROM fuel_logs WHERE status='Pending'").fetchone()[0],
        "active_today": db.execute("SELECT COUNT(*) FROM schedules WHERE date(departure_time) = date('now')").fetchone()[0]
    }
    
    db.close()
    return jsonify(stats_data)