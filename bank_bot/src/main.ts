import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/themes/index.css'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import { createPinia } from 'pinia'
import i18n from './languages'

const app = createApp(App)

app.config.globalProperties.$cookies = VueCookies;

app.use(ElementPlus)
app.use(createPinia())
app.use(i18n)
app.mount('#app')
