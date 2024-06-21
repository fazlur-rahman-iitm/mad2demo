import {createStore} from 'vuex'

const store = createStore({
    state:{
        showRegularNavbar:true,
        showAdminNavbar: false
    },
    mutations:{
        setRetgularNavbar(state, value){
            state.isAuthenticated = value;
            localStorage.setItem('showRegularNavbar', value);
        },
        setAdminNavbar(state, value){
            state.isAuthenticated = value;
            localStorage.setItem('showAdminNavbar', value);
        }
    }

})

const showRegularNavbar = localStorage.getItem('showRegularNavbar');
if (showRegularNavbar) {
  store.commit('showRegularNavbar', JSON.parse(showRegularNavbar));}

const showAdminNavbar = localStorage.getItem('showAdminNavbar');
if (showRegularNavbar) {
    store.commit('showAdminNavbar', JSON.parse(showAdminNavbar));}




export default store