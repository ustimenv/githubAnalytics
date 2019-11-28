import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
//    {
//      path: '/home/:username/:octo',
//      name: 'Home',
//      component: Home,
//      props : true
//    },
    {
      path: '/home/:username',
      name: 'Home',
      component: Home,
      props : true
    },

    {
      path: '/login',
      name: 'Login',
      component: Login
    },
  ]
})