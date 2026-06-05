from flask import request, jsonify
from database import get_db
from . import fuel_bp

@fuel_bp.route('/fuel', methods=['GET', 'POST'])
def api_fuel():
    """Get all fuel logs or create new entry"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO fuel_logs (vehicle_id, date, liters, cost, status) VALUES (?,?,?,?,?)',
                (data['vehicle_id'], data['date'], data['liters'], data['cost'], 'Pending')
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Fuel entry submitted"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    query = 'SELECT f.id, f.liters, f.cost, f.status, v.registration_no FROM fuel_logs f JOIN vehicles v ON f.vehicle_id = v.id'
    fuel_logs = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(f) for f in fuel_logs])

@fuel_bp.route('/fuel/pending')
def pending_fuel():
    """Get pending fuel approvals"""
    db = get_db()
    
    query = 'SELECT f.id, f.liters, v.registration_no FROM fuel_logs f JOIN vehicles v ON f.vehicle_id = v.id WHERE f.status="Pending"'
    pending = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(p) for p in pending])

@fuel_bp.route('/fuel/approve/<int:id>', methods=['POST'])
def approve_fuel(id):
    """Approve fuel request"""
    db = get_db()
    db.execute('UPDATE fuel_logs SET status="Approved" WHERE id=?', (id,))
    db.commit()
    db.close()
    return jsonify({"success": True, "message": "Fuel approved"})

@fuel_bp.route('/fuel/reject/<int:id>', methods=['POST'])
def reject_fuel(id):
    """Reject fuel request"""
    db = get_db()
    db.execute('UPDATE fuel_logs SET status="Rejected" WHERE id=?', (id,))
    db.commit()
    db.close()
    return jsonify({"success": True, "message": "Fuel rejected"})