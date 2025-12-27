// API Helper - GearGuard Admin Panel

const API_BASE_URL = 'http://localhost:5000/api';

// Generic API request function
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// API Methods
const API = {
    // Equipment
    equipment: {
        getAll: () => apiRequest('/equipment'),
        getById: (id) => apiRequest(`/equipment/${id}`),
        create: (data) => apiRequest('/equipment', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => apiRequest(`/equipment/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => apiRequest(`/equipment/${id}`, {
            method: 'DELETE'
        }),
        getStatistics: () => apiRequest('/equipment/statistics')
    },
    
    // Teams
    teams: {
        getAll: () => apiRequest('/teams'),
        getById: (id) => apiRequest(`/teams/${id}`),
        create: (data) => apiRequest('/teams', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => apiRequest(`/teams/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => apiRequest(`/teams/${id}`, {
            method: 'DELETE'
        })
    },
    
    // Technicians
    technicians: {
        getAll: () => apiRequest('/technicians'),
        getById: (id) => apiRequest(`/technicians/${id}`),
        create: (data) => apiRequest('/technicians', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => apiRequest(`/technicians/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => apiRequest(`/technicians/${id}`, {
            method: 'DELETE'
        }),
        getByTeam: (teamId) => apiRequest(`/technicians/team/${teamId}`)
    },
    
    // Maintenance Requests
    requests: {
        getAll: () => apiRequest('/requests'),
        getById: (id) => apiRequest(`/requests/${id}`),
        create: (data) => apiRequest('/requests', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => apiRequest(`/requests/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => apiRequest(`/requests/${id}`, {
            method: 'DELETE'
        }),
        getStatistics: () => apiRequest('/requests/statistics'),
        assignTechnician: (id, technicianId) => apiRequest(`/requests/${id}/assign`, {
            method: 'POST',
            body: JSON.stringify({ technician_id: technicianId })
        })
    },
    
    // Dashboard
    dashboard: {
        getOverview: () => apiRequest('/dashboard/overview'),
        getActivities: () => apiRequest('/dashboard/activities'),
        getAlerts: () => apiRequest('/dashboard/alerts'),
        getTeamPerformance: () => apiRequest('/dashboard/teams/performance'),
        getEquipmentDistribution: () => apiRequest('/dashboard/equipment/status-distribution'),
        getRequestTrends: (days) => apiRequest(`/dashboard/requests/trends?days=${days}`),
        getUpcomingPreventive: () => apiRequest('/dashboard/preventive/upcoming')
    },
    
    // Preventive Schedules
    schedules: {
        getAll: () => apiRequest('/preventive-schedules'),
        create: (data) => apiRequest('/preventive-schedules', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        update: (id, data) => apiRequest(`/preventive-schedules/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),
        delete: (id) => apiRequest(`/preventive-schedules/${id}`, {
            method: 'DELETE'
        }),
        complete: (id) => apiRequest(`/preventive-schedules/${id}/complete`, {
            method: 'POST'
        })
    }
};

// Utility Functions
function showToast(message, type = 'success') {
    // Simple toast notification (you can enhance this)
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function getStatusBadgeClass(status) {
    const statusMap = {
        'operational': 'badge-success',
        'maintenance': 'badge-warning',
        'breakdown': 'badge-danger',
        'scrap': 'badge-secondary',
        'new': 'badge-info',
        'in_progress': 'badge-warning',
        'repaired': 'badge-success',
        'scheduled': 'badge-info',
        'overdue': 'badge-danger',
        'completed': 'badge-success',
        'active': 'badge-success',
        'inactive': 'badge-secondary'
    };
    return statusMap[status] || 'badge-secondary';
}

function getPriorityBadgeClass(priority) {
    const priorityMap = {
        'low': 'badge-info',
        'medium': 'badge-warning',
        'high': 'badge-danger',
        'critical': 'badge-danger'
    };
    return priorityMap[priority] || 'badge-secondary';
}

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
