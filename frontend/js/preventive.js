// Preventive Maintenance JS - GearGuard Admin Panel

let allSchedules = [];
let allEquipment = [];

document.addEventListener('DOMContentLoaded', function() {
    loadSchedules();
    loadEquipment();
    
    // Setup form
    document.getElementById('scheduleForm').addEventListener('submit', handleFormSubmit);
});

async function loadSchedules() {
    try {
        const response = await API.schedules.getAll();
        allSchedules = response.data;
        renderSchedulesTable(allSchedules);
        updateStats();
    } catch (error) {
        console.error('Error loading schedules:', error);
        showToast('Failed to load schedules', 'error');
    }
}

async function loadEquipment() {
    try {
        const response = await API.equipment.getAll();
        allEquipment = response.data;
        populateEquipmentSelect();
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

function populateEquipmentSelect() {
    const select = document.getElementById('scheduleEquipment');
    select.innerHTML = '<option value="">Select Equipment</option>';
    
    allEquipment.forEach(equipment => {
        const option = document.createElement('option');
        option.value = equipment.id;
        option.textContent = `${equipment.name} (${equipment.type})`;
        select.appendChild(option);
    });
}

function renderSchedulesTable(schedules) {
    const tbody = document.getElementById('schedulesTableBody');
    
    if (schedules.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">No schedules found</td></tr>';
        return;
    }
    
    tbody.innerHTML = schedules.map(schedule => {
        // Find equipment for warranty info
        let warranty = '';
        if (allEquipment && Array.isArray(allEquipment)) {
            const eq = allEquipment.find(e => e.id === schedule.equipment_id);
            warranty = eq && eq.warranty ? eq.warranty : (eq && eq.warranty_expiry ? `Until ${eq.warranty_expiry}` : 'N/A');
        }
        return `
        <tr>
            <td>${schedule.id}</td>
            <td>${schedule.equipment_name}</td>
            <td>${warranty}</td>
            <td>${schedule.task_name}</td>
            <td><span class="badge badge-info">${schedule.frequency}</span></td>
            <td>${schedule.last_completed ? formatDate(schedule.last_completed) : 'N/A'}</td>
            <td>${formatDate(schedule.next_due)}</td>
            <td><span class="badge ${getStatusBadgeClass(schedule.status)}">${schedule.status}</span></td>
            <td>
                <div class="table-actions">
                    <button class="action-btn action-btn-edit" onclick="editSchedule(${schedule.id})">Edit</button>
                    ${schedule.status !== 'completed' ? 
                        `<button class="action-btn action-btn-complete" onclick="completeSchedule(${schedule.id})">Complete</button>` : ''}
                    <button class="action-btn action-btn-delete" onclick="deleteSchedule(${schedule.id})">Delete</button>
                </div>
            </td>
        </tr>
        `;
    }).join('');
}

function updateStats() {
    const totalSchedules = allSchedules.length;
    const overdueSchedules = allSchedules.filter(s => s.is_overdue && s.status !== 'completed').length;
    
    // Calculate due this week
    const today = new Date();
    const nextWeek = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
    const dueThisWeek = allSchedules.filter(s => {
        const dueDate = new Date(s.next_due);
        return dueDate >= today && dueDate <= nextWeek && s.status !== 'completed';
    }).length;
    
    document.getElementById('totalSchedules').textContent = totalSchedules;
    document.getElementById('overdueCount').textContent = overdueSchedules;
    document.getElementById('upcomingCount').textContent = dueThisWeek;
}

function showAddScheduleModal() {
    document.getElementById('modalTitle').textContent = 'New Preventive Schedule';
    document.getElementById('scheduleId').value = '';
    document.getElementById('scheduleForm').reset();
    document.getElementById('scheduleModal').classList.add('active');
}

function editSchedule(id) {
    const schedule = allSchedules.find(s => s.id === id);
    if (!schedule) return;
    
    document.getElementById('modalTitle').textContent = 'Edit Preventive Schedule';
    document.getElementById('scheduleId').value = schedule.id;
    document.getElementById('scheduleEquipment').value = schedule.equipment_id;
    document.getElementById('scheduleTask').value = schedule.task_name;
    document.getElementById('scheduleFrequency').value = schedule.frequency;
    document.getElementById('scheduleNextDue').value = schedule.next_due;
    document.getElementById('scheduleLastCompleted').value = schedule.last_completed || '';
    
    document.getElementById('scheduleModal').classList.add('active');
}

async function deleteSchedule(id) {
    if (!confirmDelete('Are you sure you want to delete this schedule?')) return;
    
    try {
        await API.schedules.delete(id);
        showToast('Schedule deleted successfully');
        loadSchedules();
    } catch (error) {
        showToast(error.message || 'Failed to delete schedule', 'error');
    }
}

async function completeSchedule(id) {
    if (!confirm('Mark this schedule as completed? This will update the next due date.')) return;
    
    try {
        await API.schedules.complete(id);
        showToast('Schedule marked as completed');
        loadSchedules();
    } catch (error) {
        showToast(error.message || 'Failed to complete schedule', 'error');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('scheduleId').value;
    const data = {
        equipment_id: parseInt(document.getElementById('scheduleEquipment').value),
        task_name: document.getElementById('scheduleTask').value,
        frequency: document.getElementById('scheduleFrequency').value,
        next_due: document.getElementById('scheduleNextDue').value,
        last_completed: document.getElementById('scheduleLastCompleted').value || null
    };
    
    try {
        if (id) {
            await API.schedules.update(parseInt(id), data);
            showToast('Schedule updated successfully');
        } else {
            await API.schedules.create(data);
            showToast('Schedule created successfully');
        }
        
        closeScheduleModal();
        loadSchedules();
    } catch (error) {
        showToast(error.message || 'Failed to save schedule', 'error');
    }
}

function closeScheduleModal() {
    document.getElementById('scheduleModal').classList.remove('active');
}
