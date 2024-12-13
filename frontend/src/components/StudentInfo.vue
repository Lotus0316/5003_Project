<template>
  <div style="max-width: 2600px;">
    <div class="hori-wrap">
      <div class="student-info-container">
        <h1 style="font-size: x-large;">Welcome, {{ student.name }}</h1>
        <p><strong>Student ID:</strong> {{ student.sid }}</p>
        <p><strong>Major:</strong> {{ student.cur_major }}</p>
        <p><strong>Email:</strong> {{ student.email }}</p>
      </div>
      <div class="course-management">
        <div class="my-courses" v-if="myCourses.length">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h1 style="font-size: x-large;">My Courses</h1>
              <button @click="openEnrollModal">Enroll Course</button>
            </div>
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
          <div v-else>
            <div style=" width: 650px; display: flex; justify-content: space-between; align-items: center;">
              <h1 style="font-size: x-large;">My Courses</h1>
              <button @click="openEnrollModal">Enroll Course</button>
            </div>
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
            </table>
          </div>
        </div>
    </div>
    
    <div v-if="showEnrollModal" class="modal-overlay">
      <div class="modal-content" style="display: flexbox;">
        <h2 style="margin-bottom: 10px;">Enroll Course</h2>
        <form @submit.prevent="enrollCourse">
          <div class="form-group">
            <label for="courseSelect">Select Course</label>
            <select v-model="selectedCourse" id="courseSelect" required>
              <option value="">Choose a course</option>
              <option v-for="course in availableCourses" 
                      :key="course.cid" 
                      :value="course.cid">
                {{ course.cname }} ({{ course.cid }})
              </option>
            </select>
          </div>
          <div class="modal-buttons">
            <button type="submit">Enroll</button>
            <button type="button" class="btn-cancel" @click="cancelEnrollment">Cancel</button>
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
          email: '',
          shouldShowMessage: false
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
        openEnrollModal() {
            this.showEnrollModal = true;
        },

        cancelEnrollment() {
          this.shouldShowMessage = true; // 设置标志位为 true
          this.closeEnrollModal();
        },

        closeEnrollModal() {
            this.showEnrollModal = false;
            this.selectedCourse = '';
            if (this.shouldShowMessage) {
              this.$message({
                  message: 'Course enrollment has been canceled.',
                  type: 'info'
              });
            }
            this.shouldShowMessage = false;
        },

        async enrollCourse() {
            console.log('Enroll Course clicked, Course ID:', this.selectedCourse);
            const token = sessionStorage.getItem('access_token');
            this.errorMessage = '';
            this.successMessage = '';

            if (!this.selectedCourse) {
                this.$message.error('Please select a course to enroll.');
                return;
            }

            try {
                const response = await axios.post(
                    `${API_BASE_URL}/api/student/${this.student.sid}/enroll/`,
                    { cid: this.selectedCourse },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                
                if (response.data.status === 'success') {
                    this.$message.success('Course enrolled successfully!');
                    await this.loadMyCourses();
                    await this.loadAvailableCourses();
                    this.closeEnrollModal();
                } else {
                    this.$message.error(response.data.message || 'Enrollment failed, please try again.');
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data.error) {
                    this.$message.error(error.response.data.error);
                } else {
                    this.$message.error('Enrollment failed, please try again.');
                }
                console.error('Enrollment error:', error);
            }
        },

        async dropCourse(courseId) {
            this.$confirm('Are you sure you want to drop this course?', 'Confirm Drop', {
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
                type: 'warning',
            })
            .then(async () => {
                const token = sessionStorage.getItem('access_token');
                try {
                    await axios.delete(
                        `${API_BASE_URL}/api/student/${this.student.sid}/courses/drop/${courseId}/`,
                        { headers: { Authorization: `Bearer ${token}` } }
                    );
                    // 使用 Element UI 的消息提示替代 alert
                    this.$message({
                        type: 'success',
                        message: 'Course dropped successfully!',
                    });
                    await this.loadMyCourses();
                } catch (error) {
                    this.$message.error(error.response?.data?.error || 'Failed to drop course.');
                }
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: 'Course drop canceled',
                });
            });
        }
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
  .my-courses {
    width: 650px;
  }

  .hori-wrap {
    display: flex;
  }
  .student-info-container {
    margin: 0 40px auto auto;
    padding: 20px;
  }
  .student-info-container p {
    font-size: large;
  }
  .course-management {
    margin: 0 auto auto auto;
    padding: 20px;
  }
  .team-dashboard {
    margin-top: 20px;
    }
    
    .course-section {
        margin: 20px 0;
    }
    
    button {
    padding: 5px 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    .button-group {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .courses-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
      background: rgba(255, 255, 255, 0.377);
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border-radius: 10px;
      overflow: hidden;
    }

    .courses-table th,
    .courses-table td {
        padding: 10px 10px;
        text-align: center;
        border-bottom: 1px solid #ddd;
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
      background-color: rgba(255, 255, 255, 0.822);
      padding: 0 20px;
      border-radius: 8px;
      width: 90%;
      max-width: 500px;
      max-height: 30%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .form-group input,
    .form-group select,
    .form-group textarea {
        width: 97%;
        padding: 8px;
        margin: 10px 0 20px 0;
        border: 1px solid #ddddddf6;
        border-radius: 4px;
    }

    .modal-buttons {
        display: flex;
        justify-content: flex-begin;
        gap: 10px;
        margin: 10px 0 20px 0;
    }

    .btn {
        padding: 5px 10px;
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
  