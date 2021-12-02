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
  <div class="app__container">
    <navbar></navbar>
    <router-view class="page-content"></router-view>
  </div>

</template>

<style>
html, body {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}

* {
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  position: relative;
  width: 100%;
  height: 100%;
}

.app__container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-content {
  margin-top: 30px;
}
</style>
