<template>
    <div class="signup-container">
      <h2>SignUp</h2>
      <form @submit.prevent="signupUser">

         <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" v-model="name" required>
        </div> 
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>
        </div>
        
        <div class="form-group">
            <label for="text">Email:</label>
            <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        
        <button type="submit">Sign Up</button>
      </form>
     
    </div>
  </template>
  
  <script>
  
  export default{
    data(){
      return{
        username:'',
        email:'',
        password:'',
        errorMessage:'',
        name: ''
      };
    },
    methods:{
      async signupUser(){
        try{
          await this.$axios.post('/api/signup',{
            username: this.username,
            email: this.email,
            password: this.password,
            name: this.name,

          });
        this.$toast.success('User Signed up Successfully!!', {
                        position: 'top-right',
                        duration: 5000,
                    });
          this.$router.push('/login');
        } catch(error){
          this.errorMessage = error.response ? error.response.data.message:'Signup Failed.Please try again'
        }
      }
    }
  }
  
  
  </script>
  
  <style>
  
  </style>
