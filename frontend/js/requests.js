// Requests JS - GearGuard Admin Panel

let allRequests = [];
let allEquipment = [];
let allTeams = [];
let allTechnicians = [];

document.addEventListener('DOMContentLoaded', function() {
    loadRequests();
    loadEquipment();
    loadTeams();
    loadTechnicians();
    
    // Setup filters
    document.getElementById('searchInput').addEventListener('input', filterRequests);
    document.getElementById('statusFilter').addEventListener('change', filterRequests);
    document.getElementById('typeFilter').addEventListener('change', filterRequests);
    document.getElementById('priorityFilter').addEventListener('change', filterRequests);
    
    // Setup form
    document.getElementById('requestForm').addEventListener('submit', handleFormSubmit);
});

async function loadRequests() {
    try {
        const response = await API.requests.getAll();
        allRequests = response.data;
        renderRequestsTable(allRequests);
    } catch (error) {
        console.error('Error loading requests:', error);
        showToast('Failed to load requests', 'error');
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

async function loadTeams() {
    try {
        const response = await API.teams.getAll();
        allTeams = response.data;
        // Populate assign team select
        const teamSelect = document.getElementById('requestAssignedTeam');
        if (teamSelect) {
            teamSelect.innerHTML = '<option value="">Auto (based on equipment)</option>';
            allTeams.forEach(team => {
                const opt = document.createElement('option');
                opt.value = team.id;
                opt.textContent = team.name;
                teamSelect.appendChild(opt);
            });
        }
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

async function loadTechnicians() {
    try {
        const response = await API.technicians.getAll();
        allTechnicians = response.data;
        // Populate assign technician select
        const techSelect = document.getElementById('requestAssignedTechnician');
        if (techSelect) {
            techSelect.innerHTML = '<option value="">Unassigned</option>';
            allTechnicians.forEach(tech => {
                const opt = document.createElement('option');
                opt.value = tech.id;
                opt.textContent = tech.name;
                techSelect.appendChild(opt);
            });
        }
    } catch (error) {
        console.error('Error loading technicians:', error);
    }
}

function populateEquipmentSelect() {
    const select = document.getElementById('requestEquipment');
    select.innerHTML = '<option value="">Select Equipment</option>';
    
    allEquipment.forEach(equipment => {
        const option = document.createElement('option');
        option.value = equipment.id;
        option.textContent = `${equipment.name} (${equipment.type})`;
        select.appendChild(option);
    });
}

function renderRequestsTable(requests) {
    const tbody = document.getElementById('requestsTableBody');
    
    if (requests.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center">No requests found</td></tr>';
        return;
    }
    
    tbody.innerHTML = requests.map(request => {
        const teamName = request.assigned_team_name || request.assigned_team || request.assigned_team_id ? (request.assigned_team_name || `Team #${request.assigned_team_id || ''}`) : 'Auto';
        const techName = request.assigned_technician_name || request.assigned_technician || request.assigned_technician_id ? (request.assigned_technician_name || `Tech #${request.assigned_technician_id || ''}`) : 'Unassigned';
        return `
        <tr>
            <td>${request.id}</td>
            <td>${request.equipment_name}</td>
            <td><span class="badge badge-info">${request.type}</span></td>
            <td><span class="badge ${getPriorityBadgeClass(request.priority)}">${request.priority}</span></td>
            <td><span class="badge ${getStatusBadgeClass(request.status)}">${request.status.replace('_', ' ')}</span></td>
            <td>${teamName}</td>
            <td>${techName}</td>
            <td>${request.description ? (request.description.substring(0, 50) + (request.description.length > 50 ? '...' : '')) : ''}</td>
            <td>${formatDate(request.requested_date)}</td>
            <td>
                <div class="table-actions">
                    <button class="action-btn action-btn-edit" onclick="editRequest(${request.id})">Edit</button>
                    <button class="action-btn action-btn-delete" onclick="deleteRequest(${request.id})">Delete</button>
                </div>
            </td>
        </tr>
        `;
    }).join('');
}

function filterRequests() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    const priorityFilter = document.getElementById('priorityFilter').value;
    
    let filtered = allRequests.filter(request => {
        const matchesSearch = request.equipment_name.toLowerCase().includes(searchTerm) ||
                            request.description.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || request.status === statusFilter;
        const matchesType = !typeFilter || request.type === typeFilter;
        const matchesPriority = !priorityFilter || request.priority === priorityFilter;
        
        return matchesSearch && matchesStatus && matchesType && matchesPriority;
    });
    
    renderRequestsTable(filtered);
}

function showAddRequestModal() {
    document.getElementById('modalTitle').textContent = 'New Maintenance Request';
    document.getElementById('requestId').value = '';
    document.getElementById('requestForm').reset();
    document.getElementById('requestModal').classList.add('active');
}

function editRequest(id) {
    const request = allRequests.find(r => r.id === id);
    if (!request) return;
    
    document.getElementById('modalTitle').textContent = 'Edit Maintenance Request';
    document.getElementById('requestId').value = request.id;
    document.getElementById('requestEquipment').value = request.equipment_id;
    document.getElementById('requestType').value = request.type;
    document.getElementById('requestPriority').value = request.priority;
    document.getElementById('requestStatus').value = request.status;
    document.getElementById('requestDescription').value = request.description;
    document.getElementById('requestNotes').value = request.notes || '';
    // Set assigned team and technician if present
    if (document.getElementById('requestAssignedTeam')) {
        document.getElementById('requestAssignedTeam').value = request.assigned_team_id || '';
    }
    if (document.getElementById('requestAssignedTechnician')) {
        document.getElementById('requestAssignedTechnician').value = request.assigned_technician_id || '';
    }
    
    document.getElementById('requestModal').classList.add('active');
}

async function deleteRequest(id) {
    if (!confirmDelete('Are you sure you want to delete this request?')) return;
    
    try {
        await API.requests.delete(id);
        showToast('Request deleted successfully');
        loadRequests();
    } catch (error) {
        showToast(error.message || 'Failed to delete request', 'error');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('requestId').value;
    const data = {
        equipment_id: parseInt(document.getElementById('requestEquipment').value),
        type: document.getElementById('requestType').value,
        priority: document.getElementById('requestPriority').value,
        status: document.getElementById('requestStatus').value,
        description: document.getElementById('requestDescription').value,
        notes: document.getElementById('requestNotes').value,
        assigned_team_id: document.getElementById('requestAssignedTeam') ? (document.getElementById('requestAssignedTeam').value ? parseInt(document.getElementById('requestAssignedTeam').value) : null) : null,
        assigned_technician_id: document.getElementById('requestAssignedTechnician') ? (document.getElementById('requestAssignedTechnician').value ? parseInt(document.getElementById('requestAssignedTechnician').value) : null) : null
    };
    
    try {
        if (id) {
            await API.requests.update(parseInt(id), data);
            showToast('Request updated successfully');
        } else {
            await API.requests.create(data);
            showToast('Request created successfully');
        }
        
        closeRequestModal();
        loadRequests();
    } catch (error) {
        showToast(error.message || 'Failed to save request', 'error');
    }
}

function closeRequestModal() {
    document.getElementById('requestModal').classList.remove('active');
}
