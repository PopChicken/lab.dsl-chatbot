import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/themes/index.css'
import App from './App.vue'
import VueCookies from 'vue-cookies'

const app = createApp(App)

app.config.globalProperties.$cookies = VueCookies;

app.use(ElementPlus)
app.mount('#app')
