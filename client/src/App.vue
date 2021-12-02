<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar
  }
};

</script>

<template>
  <div>
    <navbar></navbar>
    <router-view class="page-content"></router-view>
  </div>

</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.page-content {
  margin-top: 30px;
}
</style>
