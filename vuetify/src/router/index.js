import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ '../views/home.vue')
  },
  {
    path: '/myevents',
    name: 'myevents',
    component: () => import(/* webpackChunkName: "about" */ '../views/myevents.vue')
  },
  {
    path: '/events',
    name: 'events',
    component: () => import(/* webpackChunkName: "about" */ '../views/events.vue')
  },
  {
    path: '/logout',
    name: 'logout',
    component: () => import(/* webpackChunkName: "about" */ '../views/logout.vue')
  },
  {
    path: '/superuser',
    name: 'superuser',
    component: () => import(/* webpackChunkName: "about" */ '../views/superuser.vue')
  },
]

const router = new VueRouter({
  routes
})

export default router
