from flask import request, jsonify
from database import get_db
from . import vehicles_bp

@vehicles_bp.route('/vehicles', methods=['GET', 'POST'])
def api_vehicles():
    """Get all vehicles or create new vehicle"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO vehicles (registration_no, type, capacity, mileage) VALUES (?,?,?,?)',
                (data['registration_no'], data['type'], data['capacity'], data.get('mileage', 0))
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Vehicle added"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    vehicles = db.execute('SELECT * FROM vehicles').fetchall()
    db.close()
    return jsonify([dict(v) for v in vehicles])

@vehicles_bp.route('/vehicles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def vehicle_detail(id):
    """Get, update, or delete specific vehicle"""
    db = get_db()
    
    if request.method == 'GET':
        vehicle = db.execute('SELECT * FROM vehicles WHERE id = ?', (id,)).fetchone()
        db.close()
        if vehicle:
            return jsonify(dict(vehicle))
        return jsonify({"error": "Vehicle not found"}), 404
    
    elif request.method == 'PUT':
        data = request.json
        db.execute(
            'UPDATE vehicles SET type=?, capacity=?, mileage=? WHERE id=?',
            (data.get('type'), data.get('capacity'), data.get('mileage'), id)
        )
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Vehicle updated"})
    
    elif request.method == 'DELETE':
        db.execute('DELETE FROM vehicles WHERE id = ?', (id,))
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Vehicle deleted"}), 200