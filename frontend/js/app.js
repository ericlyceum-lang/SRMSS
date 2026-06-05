class SRMSSApp {
    constructor() {
        this.currentUser = null;
    }

    async login() {
        const username = document.getElementById('login_user').value;
        const password = document.getElementById('login_pass').value;
        if (!username || !password) {
            utils.notify('Please enter credentials', 'error');
            return;
        }
        const success = await auth.login(username, password);
        if (success) {
            this.currentUser = auth.currentUser;
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('app-container').classList.remove('hidden');
            document.getElementById('user-role-display').innerText = this.currentUser.role;
            this.updateMenuVisibility();
            this.loadPage('dashboard');
        } else {
            utils.notify('Login Failed', 'error');
        }
    }

    logout() {
        auth.logout();
        this.currentUser = null;
        document.getElementById('app-container').classList.add('hidden');
        document.getElementById('login-screen').style.display = 'flex';
        document.getElementById('login_user').value = '';
        document.getElementById('login_pass').value = '';
    }

    toggleTheme() {
        auth.toggleTheme();
    }

    updateMenuVisibility() {
        const items = ['dashboard', 'vehicles', 'drivers', 'fuel', 'reports'];
        items.forEach(id => document.getElementById(`nav-${id}`).style.display = 'none');
        document.getElementById('nav-dashboard').style.display = 'block';
        if (auth.hasRole('Operational Staff') || auth.hasRole('Supervisor') || auth.hasRole('Administrator')) {
            document.getElementById('nav-vehicles').style.display = 'block';
            document.getElementById('nav-drivers').style.display = 'block';
            document.getElementById('nav-fuel').style.display = 'block';
            document.getElementById('nav-reports').style.display = 'block';
        }
    }

    loadPage(page) {
        const content = document.getElementById('content-area');
        const title = document.getElementById('page-title');
        content.innerHTML = '<div style="text-align:center; padding: 50px;">Loading...</div>';
        document.querySelectorAll('#nav-menu li').forEach(el => el.classList.remove('active'));
        document.getElementById(`nav-${page}`)?.classList.add('active');
        
        switch(page) {
            case 'dashboard': renderer.renderDashboard(title, content); break;
            case 'vehicles': renderer.renderVehicles(title, content); break;
            case 'drivers': renderer.renderDrivers(title, content); break;
            case 'fuel': renderer.renderFuel(title, content); break;
            case 'reports': renderer.renderReports(title, content); break;
        }
    }

    async saveVehicle() {
        const data = {
            registration_no: document.getElementById('v_reg').value,
            type: document.getElementById('v_type').value,
            capacity: document.getElementById('v_cap').value
        };
        await api.post('/vehicles', data);
        utils.notify('Vehicle added');
        this.loadPage('vehicles');
    }

    async saveDriver() {
        const data = {
            name: document.getElementById('d_name').value,
            license_no: document.getElementById('d_lic').value,
            license_expiry: document.getElementById('d_exp').value
        };
        await api.post('/drivers', data);
        utils.notify('Driver added');
        this.loadPage('drivers');
    }

    async saveFuel() {
        const data = {
            vehicle_id: document.getElementById('f_veh').value,
            date: document.getElementById('f_date').value,
            liters: document.getElementById('f_lit').value,
            cost: document.getElementById('f_cost').value
        };
        await api.post('/fuel', data);
        utils.notify('Fuel entry submitted');
        this.loadPage('fuel');
    }
}

const app = new SRMSSApp();