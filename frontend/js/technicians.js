// Technicians JS - GearGuard Admin Panel

let allTechnicians = [];
let allTeams = [];

document.addEventListener('DOMContentLoaded', function() {
    loadTechnicians();
    loadTeams();
    
    // Setup filters
    document.getElementById('searchInput').addEventListener('input', filterTechnicians);
    document.getElementById('teamFilter').addEventListener('change', filterTechnicians);
    
    // Setup form
    document.getElementById('technicianForm').addEventListener('submit', handleFormSubmit);
});

async function loadTechnicians() {
    try {
        const response = await API.technicians.getAll();
        allTechnicians = response.data;
        renderTechniciansTable(allTechnicians);
    } catch (error) {
        console.error('Error loading technicians:', error);
        showToast('Failed to load technicians', 'error');
    }
}

async function loadTeams() {
    try {
        const response = await API.teams.getAll();
        allTeams = response.data;
        populateTeamSelects();
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

function populateTeamSelects() {
    // Populate filter
    const filterSelect = document.getElementById('teamFilter');
    filterSelect.innerHTML = '<option value="">All Teams</option>';
    
    // Populate form
    const formSelect = document.getElementById('technicianTeam');
    formSelect.innerHTML = '<option value="">Select Team</option>';
    
    allTeams.forEach(team => {
        const filterOption = document.createElement('option');
        filterOption.value = team.id;
        filterOption.textContent = team.name;
        filterSelect.appendChild(filterOption);
        
        const formOption = document.createElement('option');
        formOption.value = team.id;
        formOption.textContent = team.name;
        formSelect.appendChild(formOption);
    });
}

function renderTechniciansTable(technicians) {
    const tbody = document.getElementById('techniciansTableBody');
    
    if (technicians.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">No technicians found</td></tr>';
        return;
    }
    
    tbody.innerHTML = technicians.map(tech => {
        // Find the team by team_id
        const team = allTeams.find(t => t.id === tech.team_id);
        // If not found, try to match by name (for mock/demo data)
        let teamName = team ? (team.name || team.team_name) : '';
        if (!teamName && tech.team_id) {
            // Fallback: show team_id if no name found
            teamName = `Team #${tech.team_id}`;
        }
        return `
            <tr>
                <td>${tech.id}</td>
                <td>${tech.name}</td>
                <td>${tech.email}</td>
                <td>${tech.phone}</td>
                <td>${teamName || 'N/A'}</td>
                <td><span class="badge badge-info">${tech.skill_level}</span></td>
                <td><span class="badge ${getStatusBadgeClass(tech.status)}">${tech.status}</span></td>
                <td>
                    <div class="table-actions">
                        <button class="action-btn action-btn-edit" onclick="editTechnician(${tech.id})">Edit</button>
                        <button class="action-btn action-btn-delete" onclick="deleteTechnician(${tech.id})">Delete</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

function filterTechnicians() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const teamFilter = document.getElementById('teamFilter').value;
    
    let filtered = allTechnicians.filter(tech => {
        const matchesSearch = tech.name.toLowerCase().includes(searchTerm) ||
                            tech.email.toLowerCase().includes(searchTerm) ||
                            tech.phone.includes(searchTerm);
        
        const matchesTeam = !teamFilter || tech.team_id === parseInt(teamFilter);
        
        return matchesSearch && matchesTeam;
    });
    
    renderTechniciansTable(filtered);
}

function showAddTechnicianModal() {
    document.getElementById('modalTitle').textContent = 'Add Technician';
    document.getElementById('technicianId').value = '';
    document.getElementById('technicianForm').reset();
    document.getElementById('technicianModal').classList.add('active');
}

function editTechnician(id) {
    const technician = allTechnicians.find(t => t.id === id);
    if (!technician) return;
    
    document.getElementById('modalTitle').textContent = 'Edit Technician';
    document.getElementById('technicianId').value = technician.id;
    document.getElementById('technicianName').value = technician.name;
    document.getElementById('technicianEmail').value = technician.email;
    document.getElementById('technicianPhone').value = technician.phone;
    document.getElementById('technicianTeam').value = technician.team_id;
    document.getElementById('technicianSkillLevel').value = technician.skill_level;
    document.getElementById('technicianStatus').value = technician.status;
    
    document.getElementById('technicianModal').classList.add('active');
}

async function deleteTechnician(id) {
    if (!confirmDelete('Are you sure you want to delete this technician?')) return;
    
    try {
        await API.technicians.delete(id);
        showToast('Technician deleted successfully');
        loadTechnicians();
    } catch (error) {
        showToast(error.message || 'Failed to delete technician', 'error');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('technicianId').value;
    const data = {
        name: document.getElementById('technicianName').value,
        email: document.getElementById('technicianEmail').value,
        phone: document.getElementById('technicianPhone').value,
        team_id: parseInt(document.getElementById('technicianTeam').value),
        skill_level: document.getElementById('technicianSkillLevel').value,
        status: document.getElementById('technicianStatus').value
    };
    
    try {
        if (id) {
            await API.technicians.update(parseInt(id), data);
            showToast('Technician updated successfully');
        } else {
            await API.technicians.create(data);
            showToast('Technician created successfully');
        }
        
        closeTechnicianModal();
        loadTechnicians();
    } catch (error) {
        showToast(error.message || 'Failed to save technician', 'error');
    }
}

function closeTechnicianModal() {
    document.getElementById('technicianModal').classList.remove('active');
}
