<template>
    <div v-if="loggedIn == true && role == 'user'">
        
        <h1>All Songs</h1>
        <ul>
          <li v-for="song in songs" :key="song.id">
            {{ song.title }} by {{ song.artist }}
          </li>
        </ul>
    </div>
    <div v-else>
        <h2>You are not logged in Kindly login to see the content</h2>
    </div>
</template>

        

<script>
export default {
    name: 'UserDashboard',
    data() {
        return {
            loggedIn:false,
            role:'user',
            songs:[]
        }
    },
    async mounted() {
              try {
                const response = await this.$axios.get('/api/songs')
                this.songs = response.data
              } catch (error) {
                console.error(error)
              }},
    created(){
        const token = localStorage.getItem('access_token')
        if (token) {this.loggedIn=true;}
    }
}
</script>