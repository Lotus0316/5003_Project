<template>
  <div id="app">
    <router-view></router-view>
    <!-- <test /> -->
  </div>
</template>

<script>
import test from './components/test.vue';

export default {
  name: 'App',
  components: {
    test
  }
};
</script>

<style>
/* 你可以在这里自定义应用程序的全局样式 */
</style>
  