from flask import request, jsonify
from database import get_db
from . import reports_bp

@reports_bp.route('/reports/summary')
def reports_summary():
    """Get comprehensive reports summary"""
    db = get_db()
    
    fc_result = db.execute("SELECT SUM(cost) FROM fuel_logs WHERE status='Approved'").fetchone()[0]
    fuel_cost = fc_result if fc_result else 0
    
    mc_result = db.execute("SELECT SUM(cost) FROM maintenance_logs").fetchone()[0]
    maint_cost = mc_result if mc_result else 0
    
    total_trips = db.execute("SELECT COUNT(*) FROM schedules").fetchone()[0]
    completed_trips = db.execute("SELECT COUNT(*) FROM schedules WHERE status='Completed'").fetchone()[0]
    
    liters_result = db.execute("SELECT SUM(liters) FROM fuel_logs WHERE status='Approved'").fetchone()[0]
    total_liters = liters_result if liters_result else 0
    
    completion_rate = (completed_trips / total_trips * 100) if total_trips > 0 else 0
    
    db.close()
    
    return jsonify({
        "total_fuel_cost": fuel_cost, 
        "total_maint_cost": maint_cost, 
        "total_trips": total_trips,
        "completed_trips": completed_trips,
        "completion_rate": round(completion_rate, 1),
        "total_liters": total_liters
    })