<template>
    <div class="student-info-container">
      <h1>Welcome, {{ student.name }}</h1>
      <p><strong>Student ID:</strong> {{ student.sid }}</p>
      <p><strong>Major:</strong> {{ student.cur_major }}</p>
      <p><strong>Email:</strong> {{ student.email }}</p>
      
     <div class="course-management">
      <div class="section-header">
        <h2>Course Management</h2>
        <div class="button-group">
          <button @click="showAddModal = true">Add Course</button>
          <button @click="openEnrollModal">Enroll Course</button>
        </div>
      </div>

      <div class="my-courses" v-if="myCourses.length">
      <h3>My Courses</h3>
      <table class="courses-table">
        <thead>
          <tr>
            <th>Course</th>
            <th>Time</th>
            <th>Room</th>
            <th>Semester</th>
            <th>Info</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in myCourses" :key="course.cid">
            <td>{{ course.cname }}</td>
            <td>{{ course.ctime }}</td>
            <td>{{ course.room }}</td>
            <td>{{ course.semester }}</td>
            <td>{{ course.info }}</td>
            <td>
              <button @click="dropCourse(course.cid)" class="btn btn-drop">Drop</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

      <div class="team-dashboard">
        <h2>Team Dashboard</h2>
        <button @click="goToTeamDashboard">Go to Team Dashboard</button>
      </div>


      <div class="team-request-dashboard">
        <h2>Team Request Dashboard</h2>
        <button @click="goToTeamRequest">Go to Team Request Dashboard</button>
      </div>

    </div>

    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Add New Course</h2>
        <form @submit.prevent="addCourse">
          <div class="form-group">
            <label for="courseId">Course ID</label>
            <input v-model="newCourse.cid" type="text" id="courseId" required>
          </div>
          <div class="form-group">
            <label for="courseName">Course Name</label>
            <input v-model="newCourse.cname" type="text" id="courseName" required>
          </div>
          <div class="form-group">
            <label for="semester">Semester</label>
            <input v-model="newCourse.semester" type="text" id="semester" required>
          </div>
          <div class="form-group">
            <label for="room">Room</label>
            <input v-model="newCourse.room" type="text" id="room" required>
          </div>
          <div class="form-group">
            <label for="time">Time</label>
            <input v-model="newCourse.ctime" type="text" id="time" required>
          </div>
          <div class="form-group">
            <label for="info">Info</label>
            <input v-model="newCourse.info" type="text" id="info" required>
          </div>
          <div class="modal-buttons">
            <button type="submit" class="btn">Add</button>
            <button type="button" @click="closeAddModal" class="btn btn-cancel">Cancel</button>
          </div>
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEnrollModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Enroll Course</h2>
        <form @submit.prevent="enrollCourse">
          <div class="form-group">
            <label for="courseSelect">Select Course</label>
            <select v-model="selectedCourse" id="courseSelect" required>
              <option value="">Choose a course</option>
              <option v-for="course in availableCourses" 
                      :key="course.cid" 
                      :value="course.cid">
                {{ course.cname }}
              </option>
            </select>
          </div>
          <div class="modal-buttons">
            <button type="submit">Enroll</button>
            <button type="button" @click="closeEnrollModal">Cancel</button>
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
    name: 'StudentInfo',
    data() {
      return {
        student: {
          sid: '',
          name: '',
          cur_major: '',
          email: ''
        },
        showAddModal: false,
        showEnrollModal: false,
        myCourses: [],
        availableCourses: [],
        selectedCourse: '',
        successMessage: '',
          errorMessage: '',
          newCourse: {
              cid: '',
              cname: '',
              semester: '',
              room: '',
              ctime: '',
              info: ''
          }
      }
    },
    async created() {
        await this.loadStudentInfo(),
        await Promise.all([
            this.loadMyCourses(),
            this.loadAvailableCourses()
        ]);
    },

    methods: {
        goToTeamDashboard() {
            this.$router.push({
                name: 'TeamDashboard',
                params: { sid: this.student.sid }
            });
        },
        goToTeamRequest() {
            this.$router.push({
                name: 'TeamRequest',
                params: { sid: this.student.sid }
            });
        },
        async loadStudentInfo() {
            const sid = this.$route.params.sid;
            const token = sessionStorage.getItem('access_token');

            try {
                const response = await axios.get(`${API_BASE_URL}/api/student/${sid}/`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.student = response.data;
            } catch (error) {
                if (error.response) {
                    const status = error.response.status;

                    if (status === 403) {
                        const currentSid = error.response.data.csid;
                        this.$router.push({
                            name: 'NoPermission',
                            params: {
                                reason: 'unauthorized',
                                sid: currentSid
                            }
                        });
                    } else if (status === 401) {
                        this.$router.push({ name: 'Login' });
                    } else {
                        console.error('Error loading student info:', error);
                    }
                }
            }
        },
        async loadMyCourses() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.get(
                    `${API_BASE_URL}/api/student/${this.student.sid}/courses/`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                this.myCourses = response.data;
            } catch (error) {
                console.error('Error loading courses:', error);
            }
        },
        async loadAvailableCourses() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.get(
                    `${API_BASE_URL}/api/classes/`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );
                this.availableCourses = response.data.filter(course => 
                    !this.myCourses.some(myCourse => myCourse.cid === course.cid)
        );
            } catch (error) {
                console.error('Error loading courses:', error);
            }
        },
        showAddCourseModal() {
            this.showAddModal = true;
        },
        openEnrollModal() {
            this.showEnrollModal = true;
        },
        closeAddModal() {
            this.showAddModal = false;
            this.newCourse = {
                cid: '',
                cname: '',
                semester: '',
                room: '',
                ctime: ''
            };
        },
        closeEnrollModal() {
            this.showEnrollModal = false;
            this.selectedCourse = '';
        },
        async addCourse() {
            const token = sessionStorage.getItem('access_token');
            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/classes/add/`,
                    this.newCourse,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                this.successMessage = 'Course added successfully!';
                this.errorMessage = '';
                await this.loadAvailableCourses();
                this.closeAddModal();
            } catch (error) {
                this.errorMessage = error.response?.data?.error || 'Failed to add course.';
                this.successMessage = '';
                console.error('Error adding course:', error);
            }
        },
        async enrollCourse() {
            console.log('Enroll Course clicked, Course ID:', this.selectedCourse);
            const token = sessionStorage.getItem('access_token');
            this.errorMessage = '';
            this.successMessage = '';
            if (!this.selectedCourse) {
                this.errorMessage = 'Please select a course to enroll.';
                return;
            }
            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/student/${this.student.sid}/enroll/`,
                    { cid: this.selectedCourse },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                if (response.data.status === 'success') {
                    this.successMessage = 'Course enrolled successfully!';
                    await this.loadMyCourses();
                    await this.loadAvailableCourses();
                    this.closeEnrollModal();
                } else {
                    this.errorMessage = response.data.message || 'Enrollment failed, please try again.';
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                } else {
                    this.errorMessage = 'Enrollment failed, please try again.';
                }
                console.error('Enrollment error:', error);
            }
        },
        async dropCourse(courseId) {
            if (!confirm('Are you sure you want to drop this course?')) {
                return;
            }
            const token = sessionStorage.getItem('access_token');
            try {
                await axios.delete(
                    `${API_BASE_URL}/api/student/${this.student.sid}/courses/drop/${courseId}/`,
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert('Course dropped successfully!');
                await this.loadMyCourses();
            } catch (error) {
                alert(error.response?.data?.error || 'Failed to drop course.');
                console.error('Error dropping course:', error);
            }
        },
    },
    computed: {
    availableCourses() {
      return this.availableCourses.filter(course => 
        !this.myCourses.some(myCourse => myCourse.cid === course.cid)
      );
    }
  },
};
  </script>
  
  <style scoped>
  .student-info-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  .team-dashboard {
    margin-top: 20px;
    }
    
    .course-section {
        margin: 20px 0;
    }
    
    .button-group {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .course-list {
        display: grid;
        gap: 15px;
        margin-top: 15px;
    }
    
    .course-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
        background-color: #fff;
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
        align-items: center;
    }

    .modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        width: 90%;
        max-width: 500px;
    }

    .btn {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .btn:hover {
        background-color: #0056b3;
    }

    .btn-cancel {
        background-color: #dc3545;
    }

    .btn-cancel:hover {
        background-color: #c82333;
    }

    .success-message {
        color: green;
        margin-top: 10px;
        text-align: center;
    }

    .error-message {
        color: red;
        margin-top: 10px;
        text-align: center;
    }

    .btn-drop {
        background-color: #dc3545;
    }

    .btn-drop:hover {
        background-color: #c82333;
    }
</style>
  