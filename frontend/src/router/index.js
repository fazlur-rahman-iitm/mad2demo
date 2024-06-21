import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserLogin from '../authorization/UserLogin.vue'
import UserSignup from '../authorization/UserSignup.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/signup',
    name: 'UserSignup',
    component: UserSignup
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
  },
   {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      showAdminNavbar: true,
   },}

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// router.beforeEach((to, from, next) => {
//   if (to.meta.showAdminNavbar) {
//       this.$store.commit('setRegularNavbar', false);
//       this.$store.commit('setAdminNavbar', true);
      
//   } else  {
//     this.$store.commit('setRegularNavbar', true);
//     this.$store.commit('setAdminNavbar', false);
//   }
//   next();
// });

export default router
