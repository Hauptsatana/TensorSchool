<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Navbar from './components/Navbar.vue';
import Catalog from './components/Catalog.vue';


export default {
  components: {
    Navbar,
    Catalog
  }
};

</script>

<template>
  <div>
    <navbar></navbar>
    <catalog class="page-content"></catalog>
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
