import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import LoginPage from '../views/LoginPage.vue';

Vue.use(VueRouter);

const isAuthenticated = (to, from, next) => {
    const token = localStorage.getItem('access_token');
    if(token) {
        next();
    } else {
        next('/login');
    }
};

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: Dashboard,
        beforeEnter: isAuthenticated,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem('access_token')) {
                next('/');
            } else {
                next();
            }
        }
    },
];

const router = new VueRouter({
    mode: 'history',
    routes
});

export default router;