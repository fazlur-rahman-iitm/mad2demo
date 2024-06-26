<template>
    <div v-if="loggedIn == true && role == 'artist' || role == 'admin'">
        <h1>this is an Artist dashboard</h1>
      
    </div>
    <div v-else-if="loggedIn == true && role == 'user'">
        <h2>You are not an Artist so can't see the content of this page</h2>
    </div>
    <div v-else>
        <h2>You are not logged in Kindly login to see the content</h2>
    </div>
  </template>

<script>
export default {
    name: 'ArtistDashboard',
    data() {
        return {
            loggedIn:true,
            role:'admin'
        }
    },
    computed(){
        const token = localStorage.getItem('access_token')
        if (token) {this.loggedIn=true;}
    }
}
</script>