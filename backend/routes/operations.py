from flask import request, jsonify
from database import get_db
from . import operations_bp

@operations_bp.route('/operations/today')
def operations_today():
    """Get today's operations"""
    db = get_db()
    
    query = '''SELECT s.id, s.status, s.departure_time, r.route_name, v.registration_no, d.name as driver_name
               FROM schedules s 
               JOIN routes r ON s.route_id = r.id 
               JOIN vehicles v ON s.vehicle_id = v.id 
               JOIN drivers d ON s.driver_id = d.id
               WHERE date(s.departure_time) = date('now')'''
    
    operations = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(o) for o in operations])

@operations_bp.route('/operations/status/<int:id>', methods=['POST'])
def update_operation_status(id):
    """Update operation status"""
    data = request.json
    db = get_db()
    
    db.execute('UPDATE schedules SET status = ? WHERE id = ?', (data.get('status'), id))
    db.commit()
    db.close()
    
    return jsonify({"success": True, "message": "Status updated"})

@operations_bp.route('/monitoring/vehicles')
def monitoring_vehicles():
    """Get vehicle utilization for monitoring"""
    db = get_db()
    
    query = '''SELECT v.id, v.registration_no, v.type, v.capacity, v.mileage, COUNT(s.id) as trip_count 
               FROM vehicles v 
               LEFT JOIN schedules s ON v.id = s.vehicle_id 
               GROUP BY v.id'''
    
    vehicles = db.execute(query).fetchall()
    db.close()
    return jsonify([dict(v) for v in vehicles])