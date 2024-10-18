<template>
    <div class="no-permission">
        <h1>Access Denied.<br>Please log in to continue.</h1>
        <p>{{ countdown }} seconds before redirecting to the login page...</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NoPermission',
    data() {
      return {
        countdown: 10 // 倒计时时间（秒）
      };
    },
    mounted() {
      this.startCountdown();
    },
    methods: {
      startCountdown() {
        const timer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown -= 1;
          } else {
            clearInterval(timer);
            this.$router.push({ name: 'Login' }); // 倒计时结束后跳转到登录页面
          }
        }, 1000);
      }
    }
  };
  </script>
  
  <style scoped>
  .no-permission {
    text-align: center;
    margin-top: 50px;
  }
  </style>
  