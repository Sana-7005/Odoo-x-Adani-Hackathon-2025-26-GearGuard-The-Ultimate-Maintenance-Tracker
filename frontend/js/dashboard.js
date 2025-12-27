// Dashboard JS - GearGuard Admin Panel

document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

async function loadDashboard() {
    try {
        await Promise.all([
            loadOverviewStats(),
            loadEquipmentChart(),
            loadTeamPerformance(),
            loadCriticalAlerts(),
            loadUpcomingTasks(),
            loadRecentActivities()
        ]);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

async function loadOverviewStats() {
    try {
        const response = await API.dashboard.getOverview();
        const data = response.data;
        
        // Update stat cards
        document.getElementById('totalEquipment').textContent = data.equipment.total;
        document.getElementById('openRequests').textContent = data.requests.open;
        document.getElementById('overdueSchedules').textContent = data.schedules.overdue;
        document.getElementById('activeTechnicians').textContent = data.technicians.active;
    } catch (error) {
        console.error('Error loading overview stats:', error);
    }
}

async function loadEquipmentChart() {
    try {
        const response = await API.dashboard.getEquipmentDistribution();
        const data = response.data;
        
        const chartContainer = document.getElementById('equipmentStatusChart');
        chartContainer.innerHTML = '';
        
        data.forEach(item => {
            const barHtml = `
                <div class="chart-bar">
                    <div class="chart-label">${item.status}</div>
                    <div class="chart-bar-container">
                        <div class="chart-bar-fill" style="width: ${(item.count / getTotalCount(data) * 100)}%; background-color: ${item.color};">
                            <span class="chart-value">${item.count}</span>
                        </div>
                    </div>
                </div>
            `;
            chartContainer.innerHTML += barHtml;
        });
    } catch (error) {
        console.error('Error loading equipment chart:', error);
    }
}

function getTotalCount(data) {
    return data.reduce((sum, item) => sum + item.count, 0);
}

async function loadTeamPerformance() {
    try {
        const response = await API.dashboard.getTeamPerformance();
        const data = response.data;
        
        const container = document.getElementById('teamPerformance');
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">No team data available</p>';
            return;
        }
        
        data.forEach(team => {
            const performanceHtml = `
                <div class="performance-item">
                    <div class="performance-header">
                        <span class="performance-name">${team.team_name}</span>
                        <span class="performance-rate">${team.completion_rate}%</span>
                    </div>
                    <div class="performance-bar">
                        <div class="performance-bar-fill" style="width: ${team.completion_rate}%;"></div>
                    </div>
                    <div class="performance-details">
                        <span>Total: ${team.total_requests}</span>
                        <span>Completed: ${team.completed}</span>
                        <span>Open: ${team.open}</span>
                        <span>Technicians: ${team.technician_count}</span>
                    </div>
                </div>
            `;
            container.innerHTML += performanceHtml;
        });
    } catch (error) {
        console.error('Error loading team performance:', error);
    }
}

async function loadCriticalAlerts() {
    try {
        const response = await API.dashboard.getAlerts();
        const data = response.data;
        
        const container = document.getElementById('criticalAlerts');
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">No critical alerts</p>';
            return;
        }
        
        data.slice(0, 5).forEach(alert => {
            const alertHtml = `
                <div class="alert-item ${alert.severity}">
                    <div class="alert-message">${alert.message}</div>
                    <div class="alert-details">${alert.details}</div>
                </div>
            `;
            container.innerHTML += alertHtml;
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

async function loadUpcomingTasks() {
    try {
        const response = await API.dashboard.getUpcomingPreventive();
        const data = response.data;
        
        const container = document.getElementById('upcomingTasks');
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">No upcoming tasks</p>';
            return;
        }
        
        data.forEach(task => {
            const taskHtml = `
                <div class="task-item">
                    <div class="task-info">
                        <div class="task-name">${task.task}</div>
                        <div class="task-equipment">${task.equipment}</div>
                    </div>
                    <div class="task-due">
                        <div class="task-date">${formatDate(task.due_date)}</div>
                        <div class="task-days">${task.days_until} days</div>
                    </div>
                </div>
            `;
            container.innerHTML += taskHtml;
        });
    } catch (error) {
        console.error('Error loading upcoming tasks:', error);
    }
}

async function loadRecentActivities() {
    try {
        const response = await API.dashboard.getActivities();
        const data = response.data;
        
        const container = document.getElementById('recentActivities');
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">No recent activities</p>';
            return;
        }
        
        data.forEach(activity => {
            const activityHtml = `
                <div class="activity-item">
                    <div class="activity-icon">📋</div>
                    <div class="activity-content">
                        <div class="activity-title">${activity.title}</div>
                        <div class="activity-meta">
                            <span class="badge ${getStatusBadgeClass(activity.status)}">${activity.status}</span>
                            <span class="badge ${getPriorityBadgeClass(activity.priority)}">${activity.priority}</span>
                            <span>${formatDate(activity.date)}</span>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += activityHtml;
        });
    } catch (error) {
        console.error('Error loading recent activities:', error);
    }
}
