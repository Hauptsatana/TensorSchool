import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import { createRouter, createWebHashHistory } from 'vue-router';

import Catalog from './components/Catalog.vue';
import Contacts from './components/Contacts.vue';

const routes = [
   { path: '/', component: Catalog },
   { path: '/contacts', component: Contacts }
]

const router = createRouter({
   history: createWebHashHistory(),
   routes: routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');

window.$app = app;
