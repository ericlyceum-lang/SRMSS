import sqlite3
from flask import request, jsonify
from database import get_db
from . import users_bp

@users_bp.route('/users', methods=['GET', 'POST'])
def api_users():
    """Get all users or create new user"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO users (username, password, role) VALUES (?,?,?)',
                (data['username'], data['password'], data['role'])
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "User created"}), 201
        except sqlite3.IntegrityError:
            db.close()
            return jsonify({"success": False, "message": "Username already exists"}), 400
    
    users = db.execute('SELECT id, username, role FROM users').fetchall()
    db.close()
    return jsonify([dict(u) for u in users])

@users_bp.route('/users/<int:id>', methods=['PUT', 'DELETE'])
def update_user(id):
    """Update or delete user"""
    db = get_db()
    
    if request.method == 'PUT':
        data = request.json
        db.execute(
            'UPDATE users SET role = ? WHERE id = ?',
            (data.get('role'), id)
        )
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "User role updated"})
    
    elif request.method == 'DELETE':
        db.execute('DELETE FROM users WHERE id = ?', (id,))
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "User deleted"}), 200