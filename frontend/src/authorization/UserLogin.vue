<template>
    <div class="signup-container">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        
        <button type="submit">Login</button>
      </form>
      
    </div>
  </template>
  
  <script>
  
  export default{
    data(){
      return{
        username:'',
        password:'',
      };
    },
    methods:{

      loginUser(){
      const formData = {
                username: this.username,
                password: this.password,

      }
      this.$axios.post('/api/login', formData)
      .then((response) => {
        const access_token = response.data.access_token
        const user = response.data.user

        localStorage.setItem("access_token",access_token)
        localStorage.setItem("user_info", JSON.stringify(user))
        this.$router.push('/')
      })
      .catch((error)=> "something went wrong" + error)
      
    }
  }}
  
  
  </script>
  
  <style>
  
  </style>