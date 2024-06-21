<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <h1>This is home page</h1>
     <button @click="logout">Logout</button>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    
  },
  methods: {
    logout(){

      //getting the access_token from localstorage
      const accesstoken = localStorage.getItem("access_token")

      //sending it to backend 
      this.$axios.post('/api/logout', null, {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      //after it is logged out from backend
      .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info')
        this.$router.push('/login')
      })
      .catch(error => {
        console.log('logout failed', error)
      })
    }
  },
}
</script>
