// Equipment JS - GearGuard Admin Panel

let allEquipment = [];
let allTeams = [];

document.addEventListener('DOMContentLoaded', function() {
    loadEquipment();
    loadTeams();
    
    // Setup filters
    document.getElementById('searchInput').addEventListener('input', filterEquipment);
    document.getElementById('statusFilter').addEventListener('change', filterEquipment);
    
    // Setup form
    document.getElementById('equipmentForm').addEventListener('submit', handleFormSubmit);
});

async function loadEquipment() {
    try {
        const response = await API.equipment.getAll();
        allEquipment = response.data;
        renderEquipmentTable(allEquipment);
    } catch (error) {
        console.error('Error loading equipment:', error);
        showToast('Failed to load equipment', 'error');
    }
}

async function loadTeams() {
    try {
        const response = await API.teams.getAll();
        allTeams = response.data;
        populateTeamSelect();
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

function populateTeamSelect() {
    const select = document.getElementById('equipmentTeam');
    select.innerHTML = '<option value="">Select Team</option>';
    
    allTeams.forEach(team => {
        const option = document.createElement('option');
        option.value = team.id;
        option.textContent = team.name;
        select.appendChild(option);
    });
}

function renderEquipmentTable(equipment) {
    const tbody = document.getElementById('equipmentTableBody');
    
    if (equipment.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">No equipment found</td></tr>';
        return;
    }
    
    tbody.innerHTML = equipment.map(item => `
        <tr>
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.type}</td>
            <td>${item.department}</td>
            <td><span class="badge ${getStatusBadgeClass(item.status)}">${item.status}</span></td>
            <td>${formatDate(item.purchase_date)}</td>
            <td>
                ${item.open_requests_count > 0 ? 
                    `<span class="badge badge-warning">${item.open_requests_count}</span>` : 
                    '<span class="badge badge-success">0</span>'}
            </td>
            <td>
                <div class="table-actions">
                    <button class="action-btn action-btn-edit" onclick="editEquipment(${item.id})">Edit</button>
                    <button class="action-btn action-btn-delete" onclick="deleteEquipment(${item.id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function filterEquipment() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    
    let filtered = allEquipment.filter(item => {
        const matchesSearch = item.name.toLowerCase().includes(searchTerm) ||
                            item.type.toLowerCase().includes(searchTerm) ||
                            item.department.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || item.status === statusFilter;
        
        return matchesSearch && matchesStatus;
    });
    
    renderEquipmentTable(filtered);
}

function showAddEquipmentModal() {
    document.getElementById('modalTitle').textContent = 'Add Equipment';
    document.getElementById('equipmentId').value = '';
    document.getElementById('equipmentForm').reset();
    document.getElementById('equipmentModal').classList.add('active');
}

function editEquipment(id) {
    const equipment = allEquipment.find(e => e.id === id);
    if (!equipment) return;
    
    document.getElementById('modalTitle').textContent = 'Edit Equipment';
    document.getElementById('equipmentId').value = equipment.id;
    document.getElementById('equipmentName').value = equipment.name;
    document.getElementById('equipmentType').value = equipment.type;
    document.getElementById('equipmentDepartment').value = equipment.department;
    document.getElementById('equipmentTeam').value = equipment.assigned_team_id;
    document.getElementById('equipmentStatus').value = equipment.status;
    document.getElementById('purchaseDate').value = equipment.purchase_date;
    
    document.getElementById('equipmentModal').classList.add('active');
}

async function deleteEquipment(id) {
    if (!confirmDelete('Are you sure you want to delete this equipment?')) return;
    
    try {
        await API.equipment.delete(id);
        showToast('Equipment deleted successfully');
        loadEquipment();
    } catch (error) {
        showToast(error.message || 'Failed to delete equipment', 'error');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('equipmentId').value;
    const data = {
        name: document.getElementById('equipmentName').value,
        type: document.getElementById('equipmentType').value,
        department: document.getElementById('equipmentDepartment').value,
        assigned_team_id: parseInt(document.getElementById('equipmentTeam').value),
        status: document.getElementById('equipmentStatus').value,
        purchase_date: document.getElementById('purchaseDate').value
    };
    
    try {
        if (id) {
            await API.equipment.update(parseInt(id), data);
            showToast('Equipment updated successfully');
        } else {
            await API.equipment.create(data);
            showToast('Equipment created successfully');
        }
        
        closeEquipmentModal();
        loadEquipment();
    } catch (error) {
        showToast(error.message || 'Failed to save equipment', 'error');
    }
}

function closeEquipmentModal() {
    document.getElementById('equipmentModal').classList.remove('active');
}
