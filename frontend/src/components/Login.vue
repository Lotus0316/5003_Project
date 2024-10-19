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
        />
      </div>
      <button type="submit">Login</button>
    </form>

    <!-- 显示登录成功或失败的消息 -->
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

export default {
  name: 'Login',
  data() {
    return {
      identifier: '', // 用户输入的 SID、用户名或 Email
      password: '', // 用户输入的密码
      errorMessage: '', // 登录失败的错误信息
      loginMessage: '' // 登录成功后的消息
    };
  },
  methods: {
    async handleLogin() {
      try {
        // 发送登录请求到 Django 后端获取令牌
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          identifier: this.identifier,
          password: this.password
        });

        // 登录成功后的处理，获取访问令牌和其他信息
        const { access, refresh, sid, username } = response.data;

        // 将令牌保存到 sessionStorage
        if (access && refresh) {
          sessionStorage.setItem('access_token', access);
          sessionStorage.setItem('refresh_token', refresh);
          sessionStorage.setItem('isAuthenticated', 'true'); // 添加前端守卫认证标志
        }

        // 清空错误信息
        this.errorMessage = '';

        // 显示登录成功信息
        this.loginMessage = `Login successful. Welcome, ${username}!`;

        // 跳转到 StudentInfo 页面，传递 sid 作为参数
        this.$router.push({ name: 'StudentInfo', params: { sid } });
      } catch (error) {
        // 处理登录失败的情况
        this.identifier = '';
        this.password = '';
        this.loginMessage = ''; // 清空成功登录的消息

        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Invalid credentials. Please try again.';
        }
      }
    }
  }
};
</script>


<style scoped>
/* 你可以在这里自定义应用程序的全局样式 */
.login-container {
  max-width: 400px;
  margin: 0 auto;
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
