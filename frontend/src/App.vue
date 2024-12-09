<template>
  <div id="app">
    <BasicLayout/>
    <!-- <test /> -->
  </div>
</template>

<script>
import test from './components/test.vue';
import BasicLayout from './layout/basic-layout.vue';

export default {
  name: 'App',
  components: {
    test,
    BasicLayout
  }
};
</script>

<style>
body {
    margin: 0;
}

</style>
  