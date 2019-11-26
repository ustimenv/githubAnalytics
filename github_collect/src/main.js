import Vue from 'vue'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false


var octokit = new require("@octokit/rest")({
	auth: process.env.VUE_APP_PERSONAL_AUTH,
})


new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
