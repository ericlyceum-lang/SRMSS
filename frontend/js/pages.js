class PageRenderer {
    static async renderDashboard(title, container) {
        title.innerText = "Home";
        const stats = await api.get('/stats');

        if (!stats) {
            container.innerHTML = "<div class='panel'>Error loading stats.</div>";
            return;
        }

        container.innerHTML = `
            <div class="panel">
                <h3>Dashboard</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                    <div class="stat-card"><h4>Total Vehicles</h4><div class="value">${stats.vehicles}</div></div>
                    <div class="stat-card"><h4>Active Drivers</h4><div class="value">${stats.drivers}</div></div>
                    <div class="stat-card"><h4>Scheduled Trips</h4><div class="value">${stats.trips}</div></div>
                </div>
            </div>
        `;
    }

    static async renderVehicles(title, container) {
        title.innerText = "Vehicles";
        const items = await api.get('/vehicles');
        const rows = items.map(i => `<tr><td>${i.registration_no}</td><td>${i.type}</td><td>${i.capacity}</td><td>${i.mileage || 0}</td></tr>`).join('');
        container.innerHTML = `
            <div class="panel">
                <h3>Add Vehicle</h3>
                <div class="form-row">
                    <input type="text" id="v_reg" placeholder="Reg No">
                    <input type="text" id="v_type" placeholder="Type">
                    <input type="number" id="v_cap" placeholder="Capacity">
                    <button class="btn btn-primary" onclick="app.saveVehicle()">Add</button>
                </div>
            </div>
            <div class="panel">
                <h3>Vehicle List</h3>
                <table><thead><tr><th>Reg</th><th>Type</th><th>Cap</th><th>Mileage</th></tr></thead><tbody>${rows}</tbody></table>
            </div>
        `;
    }

    static async renderDrivers(title, container) {
        title.innerText = "Drivers";
        const items = await api.get('/drivers');
        const rows = items.map(i => `<tr><td>${i.name}</td><td>${i.license_no}</td><td>${i.license_expiry || 'N/A'}</td></tr>`).join('');
        container.innerHTML = `
            <div class="panel">
                <h3>Add Driver</h3>
                <div class="form-row">
                    <input type="text" id="d_name" placeholder="Name">
                    <input type="text" id="d_lic" placeholder="License No">
                    <input type="date" id="d_exp">
                    <button class="btn btn-primary" onclick="app.saveDriver()">Add</button>
                </div>
            </div>
            <div class="panel">
                <h3>Driver List</h3>
                <table><thead><tr><th>Name</th><th>License</th><th>Expiry</th></tr></thead><tbody>${rows}</tbody></table>
            </div>
        `;
    }

    static async renderFuel(title, container) {
        title.innerText = "Fuel Logs";
        const logs = await api.get('/fuel');
        const vehicles = await api.get('/vehicles');
        const vOpts = vehicles.map(v => `<option value="${v.id}">${v.registration_no}</option>`).join('');
        const rows = logs.map(l => `<tr><td>${l.registration_no}</td><td>${l.liters}L</td><td>${utils.formatCurrency(l.cost)}</td><td><span class="badge ${utils.getBadgeClass(l.status)}">${l.status}</span></td></tr>`).join('');
        container.innerHTML = `
            <div class="panel">
                <h3>Log Fuel Entry</h3>
                <div class="form-row">
                    <select id="f_veh">${vOpts}</select>
                    <input type="date" id="f_date">
                    <input type="number" id="f_lit" placeholder="Liters">
                    <input type="number" id="f_cost" placeholder="Cost">
                    <button class="btn btn-primary" onclick="app.saveFuel()">Submit</button>
                </div>
            </div>
            <div class="panel">
                <h3>History</h3>
                <table><thead><tr><th>Vehicle</th><th>Fuel</th><th>Cost</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table>
            </div>
        `;
    }

    static async renderReports(title, container) {
        title.innerText = "Reports";
        const data = await api.get('/reports/summary');
        if (!data) {
            container.innerHTML = `<div class="panel"><p>Error generating report.</p></div>`;
            return;
        }
        container.innerHTML = `
            <div class="panel">
                <h3>Performance Summary</h3>
                <table>
                    <tr><td>Total Fuel Cost</td><td>${utils.formatCurrency(data.total_fuel_cost)}</td></tr>
                    <tr><td>Total Maintenance Cost</td><td>${utils.formatCurrency(data.total_maint_cost)}</td></tr>
                    <tr><td>Scheduled Trips</td><td>${data.total_trips}</td></tr>
                    <tr><td>Completed Trips</td><td>${data.completed_trips}</td></tr>
                    <tr><td>Completion Rate</td><td>${data.completion_rate}%</td></tr>
                </table>
            </div>
        `;
    }
}

const renderer = new PageRenderer();