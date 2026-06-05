from flask import request, jsonify
from database import get_db
from . import schedules_bp

@schedules_bp.route('/schedules', methods=['GET', 'POST'])
def api_schedules():
    """Get all schedules or create new schedule"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO schedules (route_id, vehicle_id, driver_id, departure_time, recurrence) VALUES (?,?,?,?,?)',
                (data['route_id'], data['vehicle_id'], data['driver_id'], data['departure_time'], data.get('recurrence', 'Once'))
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Schedule created"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    query = '''SELECT s.id, s.departure_time, s.recurrence, s.status, r.route_name, v.registration_no, d.name as driver_name 
               FROM schedules s 
               JOIN routes r ON s.route_id = r.id 
               JOIN vehicles v ON s.vehicle_id = v.id 
               JOIN drivers d ON s.driver_id = d.id'''
    schedules = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(s) for s in schedules])

@schedules_bp.route('/schedules/check', methods=['POST'])
def check_schedule():
    """Check for schedule conflicts"""
    data = request.json
    db = get_db()
    
    departure_time = data.get('departure_time')
    vehicle_id = data.get('vehicle_id')
    driver_id = data.get('driver_id')
    
    conflict = db.execute(
        'SELECT id FROM schedules WHERE vehicle_id=? AND departure_time=?',
        (vehicle_id, departure_time)
    ).fetchone()
    if conflict:
        db.close()
        return jsonify({"conflict": True, "message": "Vehicle already booked at this exact time."})
    
    conflict = db.execute(
        'SELECT id FROM schedules WHERE driver_id=? AND departure_time=?',
        (driver_id, departure_time)
    ).fetchone()
    if conflict:
        db.close()
        return jsonify({"conflict": True, "message": "Driver already booked at this exact time."})
    
    db.close()
    return jsonify({"conflict": False})