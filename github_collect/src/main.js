import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

//Vue.config.productionTip = false
//const GitHub = require('octocat');




/*new Vue({
  store,
  render: h => h(App)
}).$mount('#app')*/
//new Vue({
//  el: '#app',
//  store,
//  router,
//  render: h => h(App)
//}).$mount('#app')

//new Vue({
//  el: '#app',
//  store,
//  router,
//  template: '<App/>',
//  components: { App }
//})

Vue.prototype.$octo;


new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App },
  render: h => h(App)
})//.$mount('#app')