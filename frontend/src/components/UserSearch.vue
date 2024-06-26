<template>
  
<div>
  <input v-model="query"  placeholder="Search..." />
  <button @click="searchUsers">Search</button>
  <ul>
    <li v-for="user in users" :key="user.id">{{ user.id }} , {{ user.name }}, {{ user.email }}</li>
  </ul>
</div>
</template>

<script>

export default {
name: 'UserSearch',
data() {
  return {
    query: '',
    users: [],
    
  };
},
methods: {
      searchUsers() {
        if (this.query.length >=0 ) { // Start searching only if the query is longer than 2 characters
          const accesstoken = localStorage.getItem("access_token")
          
          this.$axios.get(`http://localhost:5000/api/users?search=${this.query}`,{ headers : {
          Authorization: `Bearer ${accesstoken}`
        }})
            .then(response => {
              this.users = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the users:', error);
            });
          
        } else {
          this.users = [];
        }
      }
    }
// methods: {
//   searchUsers() {
//     if (this.query.length > 2) { // Start searching only if the query is longer than 2 characters
//      this.users = this.users.filter(user => user.name.includes(this.query));
     
//      }
//     } 
//   }
}
;
</script>

<style scoped>
/* Add your styles here */
</style>
