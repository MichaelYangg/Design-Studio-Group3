import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/transaction',
                    component: () => import(/* webpackChunkName: "transaction" */ '../components/page/Transaction.vue'),
                    meta: { title: '交易信息' }
                },
                {
                    path: '/dailyjournal',
                    component: () => import(/* webpackChunkName: "dailyjournal" */ '../components/page/Daily_journal.vue'),
                    meta: { title: '日结账本' }
                },
                {
                    path: '/monthlyjournal',
                    component: () => import(/* webpackChunkName: "monthlyjournal" */ '../components/page/Monthly_journal.vue'),
                    meta: { title: '月结账本' }
                },
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
