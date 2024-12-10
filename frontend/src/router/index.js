import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import StudentInfo from '../components/StudentInfo.vue';
import NoPermission from '../components/NoPermission.vue';
import TeamDashboard from '../components/TeamDashboard.vue';
import TeamRequest from '../components/TeamRequest.vue'; 


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
    path: '/no-permission/:reason?/:sid?', // 使用动态参数 reason 和 sid，使用 ? 表示它们是可选的
    name: 'NoPermission',
    component: NoPermission
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  },
  {
    path: '/team-dashboard/:sid',
    name: 'TeamDashboard',
    component: TeamDashboard,
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/team-request/:sid',
    name: 'TeamRequest',
    component: TeamRequest,
    props: true,
    meta: {
      requiresAuth: true
    }
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
    const isAuthenticated = sessionStorage.getItem('isAuthenticated');

    if (isAuthenticated) {
      next(); // 如果已登录，允许访问
    } else {
      next({ name: 'NoPermission', params: { reason: 'login'} }); // 如果未登录，重定向到登录页面
    }
  } else {
    next(); // 如果不需要认证，直接访问
  }
});

export default router;
