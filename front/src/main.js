import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import echarts from 'echarts/lib/echarts'
import { Button, Notification } from 'element-ui'
import './styles/main.scss'

Vue.config.productionTip = false

Vue.use(Button)
Vue.prototype.$notify = Notification;
Vue.prototype.$echarts = echarts
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
