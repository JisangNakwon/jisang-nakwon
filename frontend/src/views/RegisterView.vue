<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-auth">
        <div class="col-md-5 col-lg-4">
          <div class="auth-card">
            <!-- 헤더 -->
            <div class="auth-header text-center mb-4">
              <div class="auth-logo">:)</div>
              <h2 class="auth-title">회원가입</h2>
              <p class="auth-sub">이지상:) 팬 클럽에 합류하세요!</p>
            </div>

            <!-- 에러 메시지 -->
            <div v-if="errorMsg" class="alert-custom mb-3">
              {{ errorMsg }}
            </div>

            <!-- 성공 메시지 -->
            <div v-if="successMsg" class="alert-success mb-3">
              {{ successMsg }}
            </div>

            <!-- 폼 -->
            <form @submit.prevent="handleRegister">
              <div class="form-group mb-3">
                <label class="form-label-custom">아이디</label>
                <input
                  v-model="form.username"
                  type="text"
                  class="form-input"
                  placeholder="사용할 아이디를 입력하세요"
                  required
                  autocomplete="username"
                />
              </div>

              <div class="form-group mb-3">
                <label class="form-label-custom">이메일 <span class="optional">(선택)</span></label>
                <input
                  v-model="form.email"
                  type="email"
                  class="form-input"
                  placeholder="이메일을 입력하세요"
                  autocomplete="email"
                />
              </div>

              <div class="form-group mb-3">
                <label class="form-label-custom">비밀번호</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-input"
                  placeholder="8자 이상 입력하세요"
                  required
                  autocomplete="new-password"
                />
              </div>

              <div class="form-group mb-4">
                <label class="form-label-custom">비밀번호 확인</label>
                <input
                  v-model="form.password2"
                  type="password"
                  class="form-input"
                  :class="{ 'input-error': form.password2 && form.password !== form.password2 }"
                  placeholder="비밀번호를 다시 입력하세요"
                  required
                  autocomplete="new-password"
                />
                <span
                  v-if="form.password2 && form.password !== form.password2"
                  class="error-text"
                >
                  비밀번호가 일치하지 않습니다
                </span>
              </div>

              <button
                type="submit"
                class="btn-auth w-100"
                :disabled="loading || (form.password2 && form.password !== form.password2)"
              >
                <span v-if="loading" class="spinner"></span>
                <span v-else>가입하기</span>
              </button>
            </form>

            <div class="auth-footer text-center mt-4">
              <span class="text-muted-custom">이미 계정이 있으신가요?</span>
              <router-link to="/login" class="auth-link ms-2">로그인</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ username: '', email: '', password: '', password2: '' })
const errorMsg = ref('')
const successMsg = ref('')
const loading = ref(false)

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (form.value.password !== form.value.password2) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  loading.value = true
  try {
    await authStore.register(
      form.value.username,
      form.value.email,
      form.value.password,
      form.value.password2
    )
    successMsg.value = '회원가입이 완료되었습니다! 로그인 페이지로 이동합니다...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    const data = err.response?.data
    if (data) {
      const messages = Object.values(data).flat()
      errorMsg.value = messages[0] || '회원가입 중 오류가 발생했습니다.'
    } else {
      errorMsg.value = '회원가입 중 오류가 발생했습니다.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 100vh;
}

.min-vh-auth {
  min-height: 100vh;
}

.auth-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.auth-logo {
  font-size: 3rem;
  font-weight: 900;
  color: #ffc107;
  margin-bottom: 0.5rem;
}

.auth-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.5rem;
}

.auth-sub {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.alert-custom {
  background: rgba(255, 71, 87, 0.15);
  border: 1px solid rgba(255, 71, 87, 0.4);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #ff6b81;
  font-size: 0.9rem;
}

.alert-success {
  background: rgba(46, 213, 115, 0.15);
  border: 1px solid rgba(46, 213, 115, 0.4);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #2ed573;
  font-size: 0.9rem;
}

.form-label-custom {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.optional {
  color: rgba(255, 255, 255, 0.4);
  font-weight: 400;
  font-size: 0.8rem;
}

.form-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #fff;
  font-size: 0.95rem;
  transition: all 0.3s;
  outline: none;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.form-input:focus {
  border-color: #ffc107;
  background: rgba(255, 193, 7, 0.05);
  box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.1);
}

.form-input.input-error {
  border-color: rgba(255, 71, 87, 0.6);
}

.error-text {
  color: #ff6b81;
  font-size: 0.8rem;
  margin-top: 0.4rem;
  display: block;
}

.btn-auth {
  background: linear-gradient(135deg, #ffc107, #ff6b35);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.85rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-auth:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
}

.btn-auth:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.text-muted-custom {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.auth-link {
  color: #ffc107;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.auth-link:hover {
  color: #ffd54f;
}
</style>
