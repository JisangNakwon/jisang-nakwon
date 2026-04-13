<template>
  <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
    <div class="container">
      <!-- 브랜드 -->
      <router-link class="navbar-brand d-flex align-items-center gap-2" to="/">
        <img src="/soop_logo.png" alt="SOOP" class="navbar-soop-logo" />
        <span class="brand-title">Ji-Sang Nakwon</span>
      </router-link>

      <!-- 모바일 토글 -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 메뉴 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link d-flex align-items-center gap-1" to="/overwatch">
              <img src="/overwatch_logo.png" alt="Overwatch" class="nav-ow-logo" />
              Overwatch
            </router-link>
          </li>
        </ul>

        <!-- 로그인/로그아웃 -->
        <ul class="navbar-nav">
          <template v-if="authStore.isLoggedIn">
            <li v-if="authStore.user?.is_superuser" class="nav-item me-2">
              <router-link class="btn btn-sm btn-manage" to="/admin/users">
                👥 유저 관리
              </router-link>
            </li>
            <li class="nav-item d-flex align-items-center me-3">
              <span class="text-warning fw-semibold">
                👤 {{ authStore.user?.username }}님
                <span v-if="authStore.user?.is_superuser" class="badge-super-nav">슈퍼</span>
                <span v-else-if="authStore.user?.is_staff" class="badge-staff-nav">스태프</span>
              </span>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-light btn-sm" @click="handleLogout">
                로그아웃
              </button>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="btn btn-outline-light btn-sm" to="/login">
                로그인
              </router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  color: rgba(255, 255, 255, 0.8) !important;
  transition: color 0.2s;
}
.nav-link:hover,
.nav-link.router-link-active {
  color: #ffc107 !important;
}
.navbar-soop-logo {
  height: 28px;
  width: auto;
  object-fit: contain;
}
.brand-title {
  font-family: 'Permanent Marker', cursive;
  font-size: 1.3rem;
  color: #ffc107;
  letter-spacing: 0.5px;
  line-height: 1;
}
.nav-ow-logo {
  height: 22px;
  width: 22px;
  object-fit: contain;
}
.btn-manage {
  background: rgba(249,158,26,0.15);
  border: 1px solid rgba(249,158,26,0.4);
  color: #f99e1a;
  font-weight: 600;
}
.btn-manage:hover {
  background: rgba(249,158,26,0.3);
  color: #f99e1a;
}
.badge-super-nav {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 10px;
  background: rgba(255,100,60,0.25);
  color: #ff643c;
  border: 1px solid rgba(255,100,60,0.4);
  margin-left: 4px;
  vertical-align: middle;
}
.badge-staff-nav {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 10px;
  background: rgba(249,158,26,0.2);
  color: #f99e1a;
  border: 1px solid rgba(249,158,26,0.35);
  margin-left: 4px;
  vertical-align: middle;
}
</style>
