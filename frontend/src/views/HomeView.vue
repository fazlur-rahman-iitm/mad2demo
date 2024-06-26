<template>
  <div class="home">

     <h1>This is home page</h1>
     <div v-if="loggedIn == false"><router-link to="/login">Kindly Login</router-link></div>
     
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    
  },
  data() {
    return {
      loggedIn:false
    }
  },
  created(){
    const token = localStorage.getItem('access_token')
    if (token) {this.loggedIn=true;}
  },
  
}
</script>
