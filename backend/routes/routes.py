from flask import request, jsonify
from database import get_db
from . import routes_bp

@routes_bp.route('/routes', methods=['GET', 'POST'])
def api_routes():
    """Get all routes or create new route"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute(
                'INSERT INTO routes (route_name, start_point, end_point, distance_km, path_geometry, stops) VALUES (?,?,?,?,?,?)',
                (data['route_name'], data['start_point'], data['end_point'], data['distance_km'], 
                 data.get('path_geometry', ''), data.get('stops', ''))
            )
            db.commit()
            db.close()
            return jsonify({"success": True, "message": "Route created"}), 201
        except Exception as e:
            db.close()
            return jsonify({"success": False, "message": str(e)}), 400
    
    routes = db.execute('SELECT * FROM routes').fetchall()
    db.close()
    return jsonify([dict(r) for r in routes])

@routes_bp.route('/routes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def route_detail(id):
    """Get, update, or delete specific route"""
    db = get_db()
    
    if request.method == 'GET':
        route = db.execute('SELECT * FROM routes WHERE id = ?', (id,)).fetchone()
        db.close()
        if route:
            return jsonify(dict(route))
        return jsonify({"error": "Route not found"}), 404
    
    elif request.method == 'PUT':
        data = request.json
        db.execute(
            'UPDATE routes SET route_name=?, start_point=?, end_point=?, distance_km=?, path_geometry=?, stops=? WHERE id=?',
            (data.get('route_name'), data.get('start_point'), data.get('end_point'), 
             data.get('distance_km'), data.get('path_geometry'), data.get('stops'), id)
        )
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Route updated"})
    
    elif request.method == 'DELETE':
        db.execute('DELETE FROM routes WHERE id = ?', (id,))
        db.commit()
        db.close()
        return jsonify({"success": True, "message": "Route deleted"}), 200