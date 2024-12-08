<template>
    <div>
      <!-- 测试按钮 -->
      <button @click="showSuccessMessage">Click to Show Success Message</button>
      <button @click="showErrorMessage">Click to Show Error Message</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TestMessage',
    // 组件加载时自动触发生命周期钩子
    mounted() {
      // 在组件加载时显示一条成功消息，用于测试
      this.$message.success('Test success message from mounted!');
    },
    methods: {
      // 按钮点击时触发的方法
      showSuccessMessage() {
        this.$message.success('This is a success message!');
      },
      showErrorMessage() {
        this.$message.error('This is an error message!');
      }
    }
  };
  </script>
  