import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

axios.defaults.headers.post['Content-Type'] = 'application/json';

axios.interceptors.request.use(config => {
  const accessToken = localStorage.getItem('access_token');

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');