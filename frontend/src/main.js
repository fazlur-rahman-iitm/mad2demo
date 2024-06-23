import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import VueToast from 'vue-toastification';
import 'vue-toastification/dist/theme-default.css';

// vue app creation
const app = createApp(App)


// global configuration for axios
app.config.globalProperties.$axios = axios

//default base url configuration for axios
axios.defaults.baseURL='http://127.0.0.1:5000'

// setting up interceptor to send to backend api everytime with each axios request
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('acess_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

//adding router to the app
app.use(router)

// adding toast
app.use(VueToast)

app.mount('#app')
