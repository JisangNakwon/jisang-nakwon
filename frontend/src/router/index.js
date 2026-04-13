import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import OverwatchView from '../views/OverwatchView.vue'
import OverwatchSkillsView from '../views/OverwatchSkillsView.vue'
import OverwatchBracketView from '../views/OverwatchBracketView.vue'
import UserManageView from '../views/UserManageView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  {
    path: '/overwatch',
    component: OverwatchView,
    redirect: '/overwatch/skills',
    children: [
      { path: 'skills',  name: 'OverwatchSkills',  component: OverwatchSkillsView },
      { path: 'bracket', name: 'OverwatchBracket', component: OverwatchBracketView },
    ],
  },
  {
    path: '/admin/users',
    name: 'UserManage',
    component: UserManageView,
    meta: { superOnly: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guestOnly: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.guestOnly && token) {
    next('/')
  } else if (to.meta.superOnly) {
    // 슈퍼유저 전용 페이지: 토큰 없으면 로그인으로
    if (!token) return next('/login')
    // 실제 superuser 여부는 페이지에서 API 응답으로 판단 (403 반환)
    next()
  } else {
    next()
  }
})

export default router
