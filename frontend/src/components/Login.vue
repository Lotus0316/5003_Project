<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="identifier">Account</label>
          <input
            type="text"
            id="identifier"
            v-model="identifier"
            placeholder="Enter your SID, username or Email"
            required
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
            :disabled="isLoading"
          />
        </div>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <div v-if="loginMessage" class="success-message">
        {{ loginMessage }}
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { API_BASE_URL } from '@/config/api';
  
  export default {
    name: 'Login',
    data() {
      return {
        identifier: '',
        password: '',
        errorMessage: '',
        loginMessage: '',
        isLoading: false
      };
    },
    methods: {
      async handleLogin() {
        // 重置消息
        this.errorMessage = '';
        this.loginMessage = '';
        this.isLoading = true;
  
        try {
          // 验证表单
          if (!this.identifier || !this.password) {
            throw new Error('Please enter both username and password');
          }
  
          // 发送登录请求
          const response = await axios.post(`${API_BASE_URL}/api/login/`, {
            identifier: this.identifier,
            password: this.password
          });
  
          // 验证响应数据
          const { access, refresh, sid, username } = response.data;
          if (!access || !refresh || !sid || !username) {
            throw new Error('Invalid server response');
          }

          // const authStore = useAuthStore(); // 确保在组件上下文中调用
          // authStore.setAuthData({ access, refresh, sid, username });
  
          // 存储用户信息
          sessionStorage.setItem('access_token', access);
          sessionStorage.setItem('refresh_token', refresh);
          sessionStorage.setItem('isAuthenticated', 'true');
          sessionStorage.setItem('user_sid', sid.toString());
          sessionStorage.setItem('username', username);
          
          // 显示成功消息
          this.loginMessage = `Login successful. Welcome, ${username}!`;
  
          // 延迟跳转以显示成功消息
          setTimeout(() => {
            this.$router.push({ 
              name: 'StudentInfo', 
              params: { sid: sid.toString() } 
            });
          }, 500);
  
        } catch (error) {
          // 清空输入
          this.password = '';
          
          if (error.response) {
            // 服务器响应的错误
            this.errorMessage = error.response.data.error || 'Login failed. Please try again.';
          } else if (error.request) {
            // 请求未收到响应
            this.errorMessage = 'Network error. Please check your connection.';
          } else {
            // 其他错误
            this.errorMessage = error.message || 'An error occurred. Please try again.';
          }
        } finally {
          this.isLoading = false;
        }
      }
    }
  };
  </script>


<style scoped>
/* 你可以在这里自定义应用程序的全局样式 */
.login-container {
  max-width: 400px;
  margin: 10vh auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
}
h1 {
  text-align: center;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.success-message {
  color: green;
  margin-top: 10px;
  text-align: center;
}
.error-message {
  margin-top: 15px;
  color: red;
  text-align: center;
}
</style>
