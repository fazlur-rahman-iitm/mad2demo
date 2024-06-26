<template>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-menu">
                <div class="navbar-end">
                    <router-link to="/" class="navbar-item">Home</router-link>
                    <router-link to="/#" class="navbar-item">Regular Navbar</router-link>
                    
                    <a  @click="logout" class="navbar-item">Logout</a>
                </div>
            </div>
        </div>
    </nav>
    
    <!-- <nav class="navbar">
                <div class="container">
                    <div class="navbar-menu">
                        <div class="navbar-end">
                            <router-link  to="/#" class="navbar-item">Admin Navbar</router-link>
                            
                            <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                        </div>
                    </div>
                </div>
    </nav> -->
</template>

<script>
import { mapState } from 'vuex';
export default {
    name: "NavBar",
    computed: {
        ...mapState(['showRegularNavbar', 'showAdminNavbar']),
    },
    methods: {
        logout() {
            const accessToken = this.$store.state.token;
            this.$axios.post("/logout", null, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            })
                .then(() => {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('user'); 
                })
                .catch(error => {
                    console.error('Logout failed:', error);
                });
        },
    },
    
};
</script>