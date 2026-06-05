from flask import request, jsonify
from database import get_db
from . import drivers_bp

@drivers_bp.route('/drivers', methods=['GET', 'POST'])
def api_drivers():
    """Get all drivers or create new driver"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO drivers (name, license_no, license_expiry) VALUES (?,?,?)',
                (data['name'], data['license_no'], data.get('license_expiry', ''))
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Driver added"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    drivers = db.execute('SELECT * FROM drivers').fetchall()
    db.close()
    return jsonify([dict(d) for d in drivers])

@drivers_bp.route('/drivers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def driver_detail(id):
    """Get, update, or delete specific driver"""
    db = get_db()
    
    if request.method == 'GET':
        driver = db.execute('SELECT * FROM drivers WHERE id = ?', (id,)).fetchone()
        db.close()
        if driver:
            return jsonify(dict(driver))
        return jsonify({"error": "Driver not found"}), 404
    
    elif request.method == 'PUT':
        data = request.json
        db.execute(
            'UPDATE drivers SET name=?, license_no=?, license_expiry=? WHERE id=?',
            (data.get('name'), data.get('license_no'), data.get('license_expiry'), id)
        )
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Driver updated"})
    
    elif request.method == 'DELETE':
        db.execute('DELETE FROM drivers WHERE id = ?', (id,))
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Driver deleted"}), 200