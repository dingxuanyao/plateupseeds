import { createApp } from "vue";
import App from "@/App.vue";
import vue3GoogleLogin from 'vue3-google-login'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import vfmPlugin from 'vue-final-modal'
import VueGtag from "vue-gtag";
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;


const app = createApp(App)
app.use(vfmPlugin)
app.use(VueGtag, {
    config: { id: "G-TMRLFCWB5Y" },
})

app.use(vue3GoogleLogin, {
    clientId: GOOGLE_CLIENT_ID
});

app.mount("#app");
