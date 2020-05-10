import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: 'add_record',
    name: 'AddRecord',
    component: () => import('@/views/AddRecord.vue')
  },
  {
    path: 'components',
    name: 'Components',
    component: () => import('@/views/Components.vue')
  },
  {
    path: 'statistics',
    name: 'Statistics',
    component: () => import('@/views/Statistics.vue')
  },
  {
    path: "*",
    redirect: "/",
    name: "redirect"
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
