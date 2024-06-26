<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <!-- <router-link to="/dashboard">Dashboard</router-link> |
    <router-link to="/artist/dashboard">Artist Dashboard</router-link> |
    <router-link to="/admin/dashboard">Admin Dashboard</router-link>  |  -->
    <router-link to="/user/search">Search</router-link> |

    
    <button @click="logout" v-if="loggedIn">Logout</button>

    <!-- <router-link to="/login" v-else>Login</router-link> -->
    
    
    


  </nav>
  <router-view/>
</template>

<script>
export default {
  
  data() {
    return {
      loggedIn:false
    }
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
        this.$router.push('/')
        window.location.reload();
        
      })
      .catch(error => {
        console.log('logout failed', error)
      })
    }
  },
  created() {
    // Check if the user is logged in when the component is created
    const token = localStorage.getItem('access_token')
    if (token) {this.loggedIn=true;}
  },


}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
