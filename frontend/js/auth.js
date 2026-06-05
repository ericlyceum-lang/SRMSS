class AuthManager {
    constructor() {
        this.currentUser = null;
        this.initTheme();
    }

    initTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', theme);
        const btn = document.querySelector('.theme-switch');
        if (btn) btn.innerText = theme === 'dark' ? '☀️' : '🌙';
    }

    toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        document.querySelector('.theme-switch').innerText = next === 'dark' ? '☀️' : '🌙';
    }

    async login(username, password) {
        const response = await api.post('/login', { username, password });
        if (response && response.success) {
            this.currentUser = response.user;
            return true;
        }
        return false;
    }

    logout() {
        this.currentUser = null;
    }

    hasRole(role) {
        return this.currentUser && this.currentUser.role === role;
    }
}

const auth = new AuthManager();