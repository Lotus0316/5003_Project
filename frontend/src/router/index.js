import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import StudentInfo from '../components/StudentInfo.vue';
import NoPermission from '../components/NoPermission.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/student-info/:sid',
    name: 'StudentInfo',
    component: StudentInfo,
    props: true,
    meta: {
      requiresAuth: true // 指定需要认证的路由
    }
  },
  {
    path: '/no-permission',
    name: 'NoPermission',
    component: NoPermission // 添加无权限页面的路由
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// 添加全局前置守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.meta.requiresAuth) {
    // 检查用户是否已登录（例如从 localStorage 获取登录标志）
    const isAuthenticated = localStorage.getItem('isAuthenticated');

    if (isAuthenticated) {
      next(); // 如果已登录，允许访问
    } else {
      next({ name: 'NoPermission' }); // 如果未登录，重定向到登录页面
    }
  } else {
    next(); // 如果不需要认证，直接访问
  }
});

export default router;