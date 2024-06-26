<template>
    <div v-if="loggedIn == true && role == 'admin'">
        <h1>this is an Admin dashboard</h1>
      
    </div>
    <div v-else>
        <h2>You are not an Admin so can't see the content of this page</h2>
    </div>
  </template>

<script>
export default {
    name: 'AdminDashboard',
    data() {
        return {
            loggedIn:true,
            role:'user'
        }
    },
    computed(){
        const token = localStorage.getItem('access_token')
        if (token) {this.loggedIn=true;}
    }
}
</script>