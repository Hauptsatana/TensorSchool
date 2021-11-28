import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'

const myVueRoot = createApp(App);
myVueRoot.mount('#app')

window.$myVueRoot = myVueRoot;
