import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'


// vue app creation
const app = createApp(App)

// global configuration for axios
app.config.globalProperties.$axios = axios

//default base url configuration for axios
axios.defaults.baseURL='http://127.0.0.1:5000'

//adding router to the app
app.use(router)

app.mount('#app')
