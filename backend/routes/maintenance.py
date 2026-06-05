from flask import request, jsonify
from database import get_db
from . import maintenance_bp

@maintenance_bp.route('/maintenance', methods=['GET', 'POST'])
def api_maintenance():
    """Get all maintenance logs or create new entry"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO maintenance_logs (vehicle_id, type, description, cost) VALUES (?,?,?,?)',
                (data['vehicle_id'], data['type'], data['description'], data['cost'])
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Maintenance logged"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    query = 'SELECT m.id, m.type, m.cost, v.registration_no FROM maintenance_logs m JOIN vehicles v ON m.vehicle_id = v.id'
    maintenance_logs = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(m) for m in maintenance_logs])