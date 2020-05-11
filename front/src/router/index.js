import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import $vm from '@/main'
import { Notification } from 'element-ui'
import $store from '@/store'

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

router.beforeEach((to, from, next) => {
  console.log(to);
  // document.title = to.meta.title;
  console.log($store.state.auth);

  if (to.name == 'Home') {
    next();
    return;
  }
  else if ($store.state.auth.isStaff) {
    next()
  }
  else {
    Notification.info({ title: '请先登录管理员账号' })
    next({ name: 'Home' });
  }
});

export default router
