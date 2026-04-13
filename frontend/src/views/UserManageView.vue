<template>
  <div class="manage-page">
    <div class="container">
      <div class="page-header">
        <h2 class="page-title">👥 유저 권한 관리</h2>
        <p class="page-desc">스태프 권한을 부여하거나 해제할 수 있습니다.</p>
      </div>

      <div v-if="loading" class="loading-state">불러오는 중...</div>

      <div v-else class="user-list">
        <!-- 헤더 -->
        <div class="user-header">
          <div class="col-id">ID</div>
          <div class="col-name">유저명</div>
          <div class="col-email">이메일</div>
          <div class="col-role">등급</div>
          <div class="col-toggle">스태프 권한</div>
        </div>

        <div v-for="user in users" :key="user.id" class="user-row">
          <div class="col-id">{{ user.id }}</div>
          <div class="col-name">
            <span class="username">{{ user.username }}</span>
          </div>
          <div class="col-email">{{ user.email || '-' }}</div>
          <div class="col-role">
            <span v-if="user.is_superuser" class="badge-super">슈퍼</span>
            <span v-else-if="user.is_staff" class="badge-staff">스태프</span>
            <span v-else class="badge-user">일반</span>
          </div>
          <div class="col-toggle">
            <button
              v-if="!user.is_superuser"
              :class="['toggle-btn', user.is_staff ? 'on' : 'off']"
              @click="toggleStaff(user)"
            >
              {{ user.is_staff ? '해제' : '부여' }}
            </button>
            <span v-else class="locked">-</span>
          </div>
        </div>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios.js'

const users   = ref([])
const loading = ref(true)
const error   = ref(null)

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await api.get('/accounts/users/')
    users.value = res.data
  } catch {
    error.value = '유저 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const toggleStaff = async (user) => {
  try {
    const res = await api.patch(`/accounts/users/${user.id}/`, { is_staff: !user.is_staff })
    const idx = users.value.findIndex(u => u.id === user.id)
    if (idx !== -1) users.value[idx] = res.data
  } catch {
    error.value = '권한 변경에 실패했습니다.'
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.manage-page { padding: 50px 0 60px; }

.page-header { text-align: center; margin-bottom: 40px; }
.page-title  { font-size: 1.6rem; font-weight: 800; color: #fff; margin-bottom: 8px; }
.page-desc   { font-size: 0.9rem; color: rgba(255,255,255,0.4); }

/* 레이아웃 */
.col-id     { width: 48px;  flex-shrink: 0; font-size: 0.78rem; color: rgba(255,255,255,0.3); }
.col-name   { width: 140px; flex-shrink: 0; }
.col-email  { flex: 1; font-size: 0.85rem; color: rgba(255,255,255,0.45); }
.col-role   { width: 80px;  flex-shrink: 0; display: flex; justify-content: center; }
.col-toggle { width: 80px;  flex-shrink: 0; display: flex; justify-content: center; }

/* 헤더 */
.user-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  border-radius: 10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  color: rgba(255,255,255,0.35);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 유저 행 */
.user-list { display: flex; flex-direction: column; gap: 8px; }

.user-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 12px;
  background: linear-gradient(145deg, #1a1f2e, #151b2a);
  border: 1px solid rgba(255,255,255,0.06);
  transition: all 0.2s;
}
.user-row:hover {
  border-color: rgba(255,255,255,0.12);
  background: linear-gradient(145deg, #1e2438, #181e2e);
}

.username { font-size: 0.95rem; font-weight: 700; color: #fff; }

/* 등급 배지 */
.badge-super { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; background: rgba(255,100,60,0.2); color: #ff643c; border: 1px solid rgba(255,100,60,0.4); }
.badge-staff { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; background: rgba(249,158,26,0.2); color: #f99e1a; border: 1px solid rgba(249,158,26,0.4); }
.badge-user  { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.4); border: 1px solid rgba(255,255,255,0.12); }

/* 토글 버튼 */
.toggle-btn {
  padding: 5px 14px;
  border-radius: 20px;
  border: none;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.toggle-btn.on  { background: rgba(255,80,80,0.15); color: #ff6464; border: 1px solid rgba(255,80,80,0.3); }
.toggle-btn.off { background: rgba(249,158,26,0.15); color: #f99e1a; border: 1px solid rgba(249,158,26,0.35); }
.toggle-btn.on:hover  { background: rgba(255,80,80,0.3); }
.toggle-btn.off:hover { background: rgba(249,158,26,0.3); }

.locked { color: rgba(255,255,255,0.2); font-size: 0.85rem; }

.loading-state { text-align: center; padding: 60px 0; color: rgba(255,255,255,0.35); }
.error-msg     { text-align: center; margin-top: 16px; color: #ff6464; font-size: 0.85rem; }
</style>
