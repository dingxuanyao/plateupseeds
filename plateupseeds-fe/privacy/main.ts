import { createApp } from "vue";
// import { createPinia } from 'pinia';
import App from "./Privacy.vue";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// const pinia = createPinia()
const app = createApp(App)
app.mount("#app");
