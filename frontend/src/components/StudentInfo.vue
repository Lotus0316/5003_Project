<template>
    <div class="student-info-container">
      <h1>Welcome, {{ student.name }}</h1>
      <p><strong>Student ID:</strong> {{ student.sid }}</p>
      <p><strong>Major:</strong> {{ student.cur_major }}</p>
      <p><strong>Email:</strong> {{ student.email }}</p>
  
      <div class="team-dashboard">
        <h2>Team Dashboard</h2>
        <button @click="goToTeamDashboard">Go to Team Dashboard</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'StudentInfo',
    data() {
      return {
        student: {
          sid: '',
          name: '',
          cur_major: '',
          email: ''
        }
      };
    },
    async created() {
        const sid = this.$route.params.sid;
        const token = sessionStorage.getItem('access_token'); // 获取保存的令牌

        try {
            // 获取学生的详细信息
            const response = await axios.get(`http://127.0.0.1:8000/api/student/${sid}/`, {
            headers: {
                Authorization: `Bearer ${token}` // 将令牌添加到请求头中
            }
            });
            this.student = response.data;
        } catch (error) {
            // 处理无权限的错误
            if (error.response) {
            const status = error.response.status;

            if (status === 403) {
                // 获取后端返回的 csid
                const currentSid = error.response.data.csid;

                // 无权限，重定向到 NoPermission 页面，传递 reason 和 当前用户sid 参数
                this.$router.push({ name: 'NoPermission', params: { reason: 'unauthorized', sid: currentSid } });
            } else if (status === 401) {
                // 未登录，重定向到登录页面
                this.$router.push({ name: 'Login' });
            } else {
                console.error('Unexpected error:', error);
            }
            }
        }
    },

    methods: {
      goToTeamDashboard() {
        // 将来实现组队看板的入口，这里可以做跳转
        alert('Team Dashboard functionality coming soon...');
      }
    }
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
  </style>
  