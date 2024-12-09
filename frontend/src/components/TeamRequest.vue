<template>
    <div class="team-request-container">
        <div class="header">
            <h1>Team Request Dashboard</h1>
            <button @click="showCreateRequestModal">Create Request</button>
            <button @click="goBack">Back</button>
        </div>

        <div class="requests-list">
            <h2>Active Team Requests</h2>
            <table class="requests-table">
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Course</th>
                        <th>Info</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in teamRequests" :key="request.id">
                        <td>{{ request.studentName }}</td>
                        <td>{{ request.courseId }}</td>
                        <td>{{ request.info }}</td>
                        <td>
                            <button v-if="isLeaderForCourse(request.courseId)" @click="handleInvite(request.id)"
                                class="invite-btn">
                                Invite
                            </button>
                            <button v-if="isRequestOwner(request.studentId)" @click="cancelRequest(request.id)"
                                class="cancel-btn">
                                Cancel
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
                <h2>Create Team Request</h2>
                <form @submit.prevent="createRequest">
                    <div class="form-group">
                        <label for="courseSelect">Course *</label>
                        <select v-model="newRequest.courseId" id="courseSelect" required>
                            <option value="">Select Course</option>
                            <option v-for="course in myCourses" :key="course.cid" :value="course.cid">
                                {{ course.cname }} ({{ course.cid }})
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="requestInfo">Additional Information</label>
                        <textarea v-model="newRequest.info" id="requestInfo" rows="3"
                            placeholder="Enter any additional information"></textarea>
                    </div>
                    <div class="modal-buttons">
                        <button type="submit">Submit</button>
                        <button type="button" @click="closeModal">Cancel</button>
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
    name: 'TeamRequest',
    data() {
      return {
        studentId: '',
        teamRequests: [],
        myCourses: [],
        leaderCourses: [],
        myTeams: [],
        showModal: false,
        newRequest: {
          courseId: '',
          info: ''
        }
      };
    },
    async created() {
      this.studentId = this.$route.params.sid;
      await Promise.all([
        this.loadRequests(),
        this.loadMyCourses(),
        this.loadMyTeams(),
      ]);
    },
    methods: {
      async loadRequests() {
        const token = sessionStorage.getItem('access_token');
        try {
          const response = await axios.get(
            `${API_BASE_URL}/api/team-requests/`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          this.teamRequests = response.data;
        } catch (error) {
        console.error('Error loading requests:', error);
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
      
      async loadMyTeams() {
        const token = sessionStorage.getItem('access_token');
        try {
          const response = await axios.get(
            `${API_BASE_URL}/api/student/${this.studentId}/teams/`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          this.myTeams = response.data;
          const leaderTeams = this.myTeams.filter(team => String(team.leader) === String(this.studentId));
          this.leaderCourses = leaderTeams.map(team => team.cid);
        } catch (error) {
        console.error('Error loading teams:', error);
        }
      },
      isRequestOwner(requestOwnerID) {
        return String(requestOwnerID) === this.studentId;
      },
      async createRequest() {
        const token = sessionStorage.getItem('access_token');
        try {
          await axios.post(
            `${API_BASE_URL}/api/team-requests/create/`,
            this.newRequest,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          this.closeModal();
          await this.loadRequests();
        } catch (error) {
        alert(error.response?.data?.error || 'Failed to create team request');
        }
      },
  
      async inviteToTeam(requestId) {
      if (!confirm('Are you sure you want to invite this student to your team?')) {
          return;
        }
        const token = sessionStorage.getItem('access_token');
        try {
          await axios.post(
            `${API_BASE_URL}/api/team-requests/${requestId}/invite/`,
            {},
            { headers: { Authorization: `Bearer ${token}` } }
          );
          await this.loadRequests();
        } catch (error) {
        alert(error.response?.data?.error || 'Failed to invite student');
        }
      },


        async handleInvite(requestId) {
            const token = sessionStorage.getItem('access_token');
            try {
                await axios.post(
                    `${API_BASE_URL}/api/team-requests/${requestId}/invite/`,
                    {},
                    { headers: { Authorization: `Bearer ${token}` } }
                );

                await this.loadRequests();

                this.$message.success('Successfully invited the student to your team');
            } catch (error) {
                console.error('Error inviting student:', error);

                let errorMsg = 'Failed to invite student';
                if (error.response && error.response.data && error.response.data.error) {
                    errorMsg = error.response.data.error;
                }
                this.$message.error(errorMsg);
            }
        },

        isLeaderForCourse(courseId) {
            return this.leaderCourses.includes(courseId);
        },
      
        async cancelRequest(requestId) {
            if (!confirm('Are you sure you want to cancel this request?')) {
                return;
            }
            const token = sessionStorage.getItem('access_token');
            try {
                await axios.delete(
                    `${API_BASE_URL}/api/team-requests/${requestId}/cancel/`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                await this.loadRequests();
                alert('Request has been successfully cancelled');
            } catch (error) {
                console.error('Failed to cancel request:', error);
                alert(error.response?.data?.error || 'Failed to cancel request');
            }
        },
      goBack() {
        this.$router.push({
          name: 'StudentInfo',
          params: { sid: this.studentId }
        });
      },
  
      showCreateRequestModal() {
        this.showModal = true;
      },
  
      closeModal() {
        this.showModal = false;
        this.newRequest = {
          courseId: '',
          info: ''
        };
      }
    }
  };
  </script>
  
  <style scoped>
  .team-request-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .requests-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .requests-table th,
  .requests-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group select,
  .form-group textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  .modal-buttons {
    display: flex;
    justify-content: flex-end;
  }
  
  .modal-buttons button {
    margin-left: 10px;
    padding: 8px 16px;
  }

  .cancel-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
}

.cancel-btn:hover {
    background-color: #c82333;
}
  </style>