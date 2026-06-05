class Utils {
    static formatCurrency(amount) {
        return `Rs. ${parseFloat(amount).toFixed(2)}`;
    }

    static getBadgeClass(status) {
        const classes = {
            'Approved': 'badge-green',
            'Pending': 'badge-yellow',
            'Rejected': 'badge-red'
        };
        return classes[status] || 'badge-yellow';
    }

    static notify(message, type = 'success') {
        const notification = document.createElement('div');
        notification.style.cssText = `position: fixed; top: 20px; right: 20px; padding: 15px 20px; background: ${type === 'success' ? '#16a34a' : '#ef4444'}; color: white; border-radius: 6px; z-index: 9999;`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}

const utils = new Utils();