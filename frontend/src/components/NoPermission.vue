<template>
  <div class="no-permission">
    <h1>{{ message }}</h1>
    <p>{{ countdown }} seconds before redirecting...</p>
  </div>
</template>

<script>
export default {
  name: 'NoPermission',
  data() {
    return {
      countdown: 5, // 倒计时时间（秒）
      message: '' // 默认消息
    };
  },
  mounted() {
    // 获取 sid 参数
    this.sid = this.$route.params.sid;

    // 根据路由传递的参数来设置不同的提示信息
    if (this.$route.params.reason === 'unauthorized') {
      this.message = 'Access Denied. You have no permission to this page.';
    } else {
      this.message = 'Access Denied. Please log in to continue.';
    }
    
    this.startCountdown();
  },
  methods: {
    startCountdown() {
      const timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown -= 1;
        } else {
          clearInterval(timer);
          // 根据不同的原因跳转到不同的页面
          if (this.$route.params.reason === 'login') {
            this.$router.push({ name: 'Login' }); // 未登录的情况跳转到登录页面
          } else {
            // 确保跳转到 StudentInfo 时传递 sid 参数
            const sid = this.sid;
            if (sid) {
              this.$router.push({ name: 'StudentInfo', params: { sid } }); // 无权限则跳转回有权限页面
            } else {
              console.error('Missing required param "sid"');
            }
          }
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
