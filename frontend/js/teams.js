// Teams JS - GearGuard Admin Panel

let allTeams = [];

document.addEventListener('DOMContentLoaded', function() {
    loadTeams();
    
    // Setup form
    document.getElementById('teamForm').addEventListener('submit', handleFormSubmit);
});

async function loadTeams() {
    try {
        const response = await API.teams.getAll();
        allTeams = response.data;
        renderTeamsGrid(allTeams);
    } catch (error) {
        console.error('Error loading teams:', error);
        showToast('Failed to load teams', 'error');
    }
}

function renderTeamsGrid(teams) {
    const grid = document.getElementById('teamsGrid');
    
    if (teams.length === 0) {
        grid.innerHTML = '<p class="empty-state">No teams found</p>';
        return;
    }
    
    grid.innerHTML = teams.map(team => `
        <div class="team-card">
            <div class="team-header">
                <div>
                    <div class="team-name">${team.name}</div>
                    <div class="team-department">${team.department}</div>
                </div>
                <div class="team-actions">
                    <button class="action-btn action-btn-edit" onclick="editTeam(${team.id})">✏️</button>
                    <button class="action-btn action-btn-delete" onclick="deleteTeam(${team.id})">🗑️</button>
                </div>
            </div>
            <div class="team-info">
                <span class="team-specialization">🔧 ${team.specialization}</span>
            </div>
            <div class="team-stats">
                <div class="team-stat">
                    <div class="team-stat-value">${team.technician_count}</div>
                    <div class="team-stat-label">Technicians</div>
                </div>
            </div>
        </div>
    `).join('');
}

function showAddTeamModal() {
    document.getElementById('modalTitle').textContent = 'Add Team';
    document.getElementById('teamId').value = '';
    document.getElementById('teamForm').reset();
    document.getElementById('teamModal').classList.add('active');
}

function editTeam(id) {
    const team = allTeams.find(t => t.id === id);
    if (!team) return;
    
    document.getElementById('modalTitle').textContent = 'Edit Team';
    document.getElementById('teamId').value = team.id;
    document.getElementById('teamName').value = team.name;
    document.getElementById('teamDepartment').value = team.department;
    document.getElementById('teamSpecialization').value = team.specialization;
    
    document.getElementById('teamModal').classList.add('active');
}

async function deleteTeam(id) {
    if (!confirmDelete('Are you sure you want to delete this team?')) return;
    
    try {
        await API.teams.delete(id);
        showToast('Team deleted successfully');
        loadTeams();
    } catch (error) {
        showToast(error.message || 'Failed to delete team', 'error');
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('teamId').value;
    const data = {
        name: document.getElementById('teamName').value,
        department: document.getElementById('teamDepartment').value,
        specialization: document.getElementById('teamSpecialization').value
    };
    
    try {
        if (id) {
            await API.teams.update(parseInt(id), data);
            showToast('Team updated successfully');
        } else {
            await API.teams.create(data);
            showToast('Team created successfully');
        }
        
        closeTeamModal();
        loadTeams();
    } catch (error) {
        showToast(error.message || 'Failed to save team', 'error');
    }
}

function closeTeamModal() {
    document.getElementById('teamModal').classList.remove('active');
}
