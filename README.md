# SRMSS - Smart Road Transport Depot Management System

A professional web-based system for managing smart road transport depot operations with role-based access control.

## 📋 Project Structure

```
SRMSS/
├── backend/                 # Flask API Server
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── database.py         # Database utilities
│   ├── requirements.txt    # Dependencies
│   └── routes/             # API endpoints
│       ├── auth.py
│       ├── users.py
│       ├── vehicles.py
│       ├── drivers.py
│       ├── routes.py
│       ├── schedules.py
│       ├── operations.py
│       ├── fuel.py
│       ├── maintenance.py
│       └── reports.py
│
└── frontend/               # Web Interface
    ├── index.html
    ├── css/styles.css
    └── js/
        ├── app.js
        ├── api.js
        ├── auth.js
        ├── pages.js
        └── utils.js
```

## 🚀 Getting Started

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5000`

### Frontend Setup

Open `frontend/index.html` in your browser or serve locally.

## 👥 Test Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| super | super123 | Supervisor |
| staff | staff123 | Operational Staff |

## ✨ Features

- Dashboard with statistics
- Vehicle management
- Driver registration
- Route planning
- Fuel management
- Maintenance logging
- Reports & analytics
- Role-based access control
- Dark mode support

## 📊 Database

Automatically created SQLite database with tables:
- users
- vehicles
- drivers
- routes
- schedules
- fuel_logs
- maintenance_logs

## 🔗 API Endpoints

- `POST /api/login` - Login
- `GET /api/stats` - Dashboard stats
- `GET/POST /api/vehicles` - Vehicle management
- `GET/POST /api/drivers` - Driver management
- `GET/POST /api/routes` - Route management
- `GET/POST /api/fuel` - Fuel management
- `GET/POST /api/maintenance` - Maintenance logs
- `GET /api/reports/summary` - Reports
