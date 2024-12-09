<template>
    <div class="team-dashboard-container">
        <div class="header">
            <h1>Team Dashboard</h1>
            <div>
                <button style="margin: 10px;" @click="showCreateTeamModal">Create New Team</button>
            </div>
        </div>
        <div class="my-team-section">
            <h2>My Teams</h2>
            <table class="teams-table">
                <thead>
                    <tr>
                        <th>Team Name</th>
                        <th>Course</th>
                        <th>Members</th>
                        <th>Status</th>
                        <th>Actions</th>
                        <th>Information</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="team in myTeams" :key="team.id">
                        <td>{{ team.name }}</td>
                        <td>{{ team.cid }}</td>
                        <td>{{ team.memberCount }}</td>
                        <td>
                            <span class="badge" :class="team.isRecruiting ? 'recruiting' : 'closed'"
                                @click="isTeamLeader(team) ? toggleRecruiting(team.id) : null" style="cursor: pointer;">
                                {{ team.isRecruiting ? 'Recruiting' : 'Closed' }}
                            </span>
                        </td>
                        <td>
                            <button v-if="team.leader != Number(studentId)" class="btn-danger"
                                @click="leaveTeam(team.id)">
                                Leave Team
                            </button>
                            <button style="margin-right: 5px;" v-if="isTeamLeader(team)" @click="showEditTeamModal(team)">Edit</button>
                            <button v-if="isTeamLeader(team)" class="btn-danger" @click="disbandTeam(team.id)">
                                Disband
                            </button>
                        </td>
                        <td>
                            <button class="btn-info" @click="showTeamDetails(team)">Details</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="available-teams-section">
            <h2>Available Teams</h2>
            <table class="teams-table">
                <thead>
                    <tr>
                        <th>Team Name</th>
                        <th>Course</th>
                        <th>Members</th>
                        <th>Status</th>
                        <th>Information</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="team in myTeams" :key="'joined-' + team.id">
                        <td>{{ team.name }} <span class="joined-badge">Joined</span></td>
                        <td>{{ team.cid }}</td>
                        <td>{{ team.memberCount }}</td>
                        <td>
                            <span class="badge" :class="team.isRecruiting ? 'recruiting' : 'closed'">
                                {{ team.isRecruiting ? 'Recruiting' : 'Closed' }}
                            </span>
                        </td>
                        <td>
                            <button class="btn-info" @click="showTeamDetails(team)">Details</button>
                        </td>
                    </tr>
                    <tr v-for="team in availableTeams" :key="team.id">
                        <td>{{ team.name }}</td>
                        <td>{{ team.cid }}</td>
                        <td>{{ team.memberCount }}</td>
                        <td>
                            <span class="badge" :class="team.isRecruiting ? 'recruiting' : 'closed'">
                                {{ team.isRecruiting ? 'Recruiting' : 'Closed' }}
                            </span>
                        </td>
                        <td>
                            <button class="btn-info" @click="showTeamDetails(team)">Details</button>
                            <button class="btn-primary" @click="joinTeam(team.id)">
                                Join
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
                <h2>Create New Team</h2>
                <form @submit.prevent="createTeam">
                    <div class="form-group">
                        <label for="courseName">Course *</label>
                        <select v-model="newTeam.cid" id="courseName" required>
                            <option value="">Select a course</option>
                            <option v-for="course in myCourses" :key="course.cid" :value="course.cid">
                                {{ course.cname }} ({{ course.cid }})
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="teamName">Team Name *</label>
                        <input type="text" v-model="newTeam.name" id="teamName" required placeholder="Enter team name">
                    </div>

                    <div class="form-group">
                        <label for="teamInfo">Info</label>
                        <textarea v-model="newTeam.info" id="teamInfo" rows="3"
                            placeholder="Enter additional info"></textarea>
                    </div>
                    <div class="modal-buttons">
                        <button type="submit">Create</button>
                        <button type="button" @click="closeModal">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <div v-if="showDetailsModal" class="modal-overlay">
            <div class="modal-content">
                <h1>{{ selectedTeam.name }}</h1>
                <div class="team-details" v-if="selectedTeam">
                    <p><strong>Course:</strong> {{ selectedTeam.cid }} </p>
                    <p><strong>Leader:</strong> {{ selectedTeam.leaderName }}</p>
                    <p><strong>Status:</strong>
                        <span class="badge" :class="selectedTeam.isRecruiting ? 'recruiting' : 'closed'">
                            {{ selectedTeam.isRecruiting ? 'Recruiting' : 'Closed' }}
                        </span>
                    </p>
                    <p><strong>Info:</strong> {{ selectedTeam.info }}</p>
                    <p><strong>Members ({{ selectedTeam.members.length }}):</strong></p>
                    <ul>
                        <li v-for="member in selectedTeam.members" :key="member.id">
                            {{ member.name }} - {{ member.email }}
                        </li>
                    </ul>
                    <div class="modal-buttons">
                        <button @click="closeDetailsModal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content">
                <h2>Edit Team</h2>
                <form @submit.prevent="updateTeam">
                    <div class="form-group">
                        <label for="editTeamName">Team Name *</label>
                        <input type="text" v-model="editedTeam.name" id="editTeamName" required
                            placeholder="Enter team name">
                    </div>
                    <div class="form-group">
                        <label for="editTeamInfo">Info</label>
                        <textarea v-model="editedTeam.info" id="editTeamInfo" rows="3"
                            placeholder="Enter additional info"></textarea>
                    </div>
                    <div class="modal-buttons">
                        <button type="submit">Save</button>
                        <button type="button" @click="closeEditModal">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '@/config/api';

export default {
    name: 'TeamDashboard',
    data() {
        return {
            studentId: '',
            myTeams: [],
            availableTeams: [],
            hasTeam: false,
            recruitingTeams: [],
            showModal: false,
            showDetailsModal: false,
            selectedTeam: null,
            myCourses: [],
            teamsByCourse: new Map(),
            showEditModal: false,
            editedTeam: {
                id: '',
                name: '',
                info: '',
            },
            newTeam: {
                name: '',
                cid: '',
                info: ''
            }
        };
    },
    computed: {
       
    },

    async created() {
        this.studentId = this.$route.params.sid;
        await this.loadMyCourses();
        await this.loadTeamData();
    },
    methods: {
        async loadTeamData() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.get(`${API_BASE_URL}/api/teams/`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                const allTeams = response.data.map(team => ({
                    id: team.tid,
                    name: team.tname,
                    memberCount: team.members.length,
                    members: team.members,
                    isRecruiting: team.is_recruiting,
                    leader: team.leader,
                    leaderName: team.leader_name, 
                    cid: team.cid,
                    info: team.info
                }));

                this.myTeams = allTeams.filter(team =>
                    team.members.some(member => member.id === Number(this.studentId))
                );

                this.availableTeams = allTeams.filter(team =>
                    team.isRecruiting && 
                    this.myCourses.some(course => course.cid === team.cid) &&
                    !team.members.some(member => member.id === Number(this.studentId))
                );

                this.recruitingTeams = allTeams.filter(team => team.isRecruiting);
                this.teamsByCourse = new Map(allTeams.map(team => [team.cid, team]));
                this.hasTeam = this.myTeams.length > 0;
            } catch (error) {
                console.error('Failed to load TeamData:', error);
            }
        },
        isTeamLeader(team) {
            return String(team.leader) === String(this.studentId);
        },
        showEditTeamModal(team) {
            this.editedTeam = { ...team };
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
        },
        async updateTeam() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/teams/update/${this.editedTeam.id}/`,
                    {
                        name: this.editedTeam.name,
                        info: this.editedTeam.info,
                    },
                    {
                        headers: { Authorization: `Bearer ${token}` },
                    }
                );
                if (response.data.status === 'success') {
                    alert('Team updated successfully!');
                    this.closeEditModal();
                    this.closeDetailsModal();
                    await this.loadTeamData();
                } else {
                    alert(response.data.message || 'Failed to update team');
                }
            } catch (error) {
                console.error('Error updating team:', error);
                alert(error.response?.data?.error || 'Failed to update team');
            }
        },
        async loadMyCourses() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.get(
                    `${API_BASE_URL}/api/student/${this.studentId}/courses/`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                this.myCourses = response.data;
            } catch (error) {
                console.error('Error loading courses:', error);
            }
        },
        async leaveTeam(teamId) {
            if (confirm('Are you sure you want to leave this team?')) {
                const token = sessionStorage.getItem('access_token');
                try {
                    await axios.post(`${API_BASE_URL}/api/teams/${teamId}/leave/`, {}, {
                        headers: { Authorization: `Bearer ${token}` }
                    });
                    await this.loadTeamData();
                } catch (error) {
                    console.error('Failed to leave team:', error);
                    alert(error.response?.data?.message || 'Failed to leave team');
                }
            }
        },
        showTeamDetails(team) {
            this.selectedTeam = team;
            this.showDetailsModal = true;
        },

        closeDetailsModal() {
            this.showDetailsModal = false;
            this.selectedTeam = null;
        },
        async disbandTeam(teamId) {
            if (!confirm('Are you sure you want to disband this team? This action cannot be undone.')) {
                return;
            }

            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.delete(
                    `${API_BASE_URL}/api/teams/disband/${teamId}/`,
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );

                if (response.data.status === 'success') {
                    await this.loadTeamData(); 
                    alert('Team disbanded successfully');
                }
            } catch (error) {
                console.error('Error disbanding team:', error);
                const errorMessage = error.response?.data?.error ||
                    error.response?.data?.message ||
                    'Failed to disband team';
                alert(errorMessage);
            }
        },
        async createTeam() {
            const token = sessionStorage.getItem('access_token');
            try {
                if (!this.newTeam.name || !this.newTeam.cid) {
                    alert('Please fill in team name and select a course');
                    return;
                }

                const response = await axios.post(
                    `${API_BASE_URL}/api/teams/create/`,
                    {
                        name: this.newTeam.name,
                        cid: this.newTeam.cid,
                        info: this.newTeam.info || ''
                    },
                    {
                        headers: {'Authorization': `Bearer ${token}`},
                        withCredentials: true
                    }
                );

                if (response.data.status === 'success') {
                    alert('Team created successfully!');
                    this.closeModal();
                    await this.loadTeamData();
                    this.newTeam = {
                        name: '',
                        cid: '',
                        info: ''
                    };
                } else {
                    alert(response.data.message || 'Failed to create team');
                }
            } catch (error) {
                console.error('Error creating team:', error);
                const errorMessage = error.response?.data?.error ||
                    error.response?.data?.message ||
                    'Failed to create team';
                alert(errorMessage);
            }
        },
        async joinTeam(teamId) {
            if (!confirm('Are you sure you want to join this team?')) {
                return;
            }
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/teams/join/${teamId}/`,
                    {},
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );
                if (response.data.status === 'success') {
                    alert('Successfully joined team');
                    await this.loadTeamData();
                }
            } catch (error) {
                console.error('Failed to join', error);
                const errorMessage = error.response?.data?.error ||
                    error.response?.data?.message ||
                    'Failed to join';
                alert(errorMessage);
            }
        },
        
        async toggleRecruiting(teamId) {
            if (!confirm('Are you sure you want to toggle the recruiting status of this team?')) {
                return;
            }
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/teams/toggle-recruiting/${teamId}/`,
                    {},
                    {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );
                if (response.data.status === 'success') {
                    const team = this.myTeams.find(t => t.id === teamId);
                    if (team) {
                        team.isRecruiting = response.data.is_recruiting;
                    }
                    alert('Recruiting status updated successfully');
                }
            } catch (error) {
                console.error('Error toggling recruiting status:', error);
                const errorMessage = error.response?.data?.error ||
                    error.response?.data?.message ||
                    'Failed to toggle recruiting status';
                alert(errorMessage);
            }
        },

        
        showCreateTeamModal() {
            this.showModal = true;
        },
        closeModal() {
            this.showModal = false;
            this.newTeam = {
                name: '',
                cid: '',
                info: ''
            };
        }
    }
};
</script>

<style scoped>
.team-dashboard-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.btn-info {
  background-color: #17a2b8;
  margin-right: 5px;
}

.btn-info:hover {
  background-color: #138496;
}

.team-details {
  margin: 15px 0;
}

.team-details ul {
  list-style: none;
  padding: 0;
}

.team-details li {
  margin: 5px 0;
  padding: 5px;
  background-color: #f8f9fa9c;
  border-radius: 4px;
}

button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

.btn-disabled {
  background-color: #6c757d;
  color: white;
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-disabled:hover {
  background-color: #6c757d;
}

.teams-list {
    width: 100%;
    margin-top: 20px;
}

.teams-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.377);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 10px;
    overflow: hidden;
}

.teams-table th,
.teams-table td {
    padding: 12px 15px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}

.teams-table th {
    background-color: #f8f9fa9f;
    font-weight: 600;
}

.badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
}
.recruiting {
    background-color: #28a745;
    color: white;
}
.closed {
    background-color: #dc3545;
    color: white;
}
.badge:hover {
    opacity: 0.8;
}
.team-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.team-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.team-details {
    font-size: 0.9em;
}


.joined-badge {
  font-size: 0.8em;
  background-color: #28a745;
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
}

.join-button {
    margin-top: 10px;
    background-color: #007bff;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
}

.modal-content {
    background-color: rgba(255, 255, 255, 0.822);
    padding: 0 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    max-height: 70%;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 97%;
    padding: 8px;
    border: 1px solid #ddddddf6;
    border-radius: 4px;
}

.modal-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.modal-buttons button {
    padding: 8px 16px;
}

.modal-buttons button:last-child {
    background-color: #dc3545;
}

.modal-buttons button:last-child:hover {
    background-color: #c82333;
}
</style>