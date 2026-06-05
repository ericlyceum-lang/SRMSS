const API_BASE = 'http://localhost:5000/api';

class ApiClient {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (e) {
            console.error("API Error:", e);
            return null;
        }
    }

    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (e) {
            console.error("API Error:", e);
            return null;
        }
    }

    async put(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (e) {
            console.error("API Error:", e);
            return null;
        }
    }

    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, { method: 'DELETE' });
            return await response.json();
        } catch (e) {
            console.error("API Error:", e);
            return null;
        }
    }
}

const api = new ApiClient();