<template>
  <div class="home">
    <!-- 히어로 섹션 -->
    <section class="hero-section">
      <div class="hero-bg"></div>
      <div class="container position-relative">
        <div class="row align-items-center min-vh-hero">
          <!-- 프로필 이미지 -->
          <div class="col-lg-4 text-center mb-4 mb-lg-0">
            <div class="profile-container">
              <div class="profile-ring">
                <div class="profile-avatar">
                  <img src="/jisangnakwon.png" alt="지상낙원" class="profile-logo-img" />
                </div>
              </div>
              <div class="live-badge mt-3">
                <span class="badge-dot"></span>
                <img src="/soop_logo.png" alt="SOOP" class="soop-badge-logo" />
                방송 중
              </div>
            </div>
          </div>

          <!-- 텍스트 정보 -->
          <div class="col-lg-8 text-center text-lg-start">
            <div class="hero-tag mb-2">🌟 SOOP 스트리머</div>
            <h1 class="hero-title">
              이지상<span class="smile-emoji">:)</span>
            </h1>
            <p class="hero-subtitle">
              매일 웃음과 즐거움을 전달하는 스트리머<br>
              여러분의 하루를 더 행복하게 만들어드릴게요!
            </p>

            <div class="hero-stats mb-4">
              <div class="stat-item">
                <div class="stat-number">매일</div>
                <div class="stat-label">방송</div>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <div class="stat-number">SOOP</div>
                <div class="stat-label">플랫폼</div>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">즐거움</div>
              </div>
            </div>

            <div class="hero-buttons">
              <a
                href="https://www.sooplive.com/station/jrdart"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-soop me-3"
              >
                <img src="/soop_logo.png" alt="SOOP" class="soop-btn-logo" />
                방송 보러가기
              </a>
              <a
                href="https://www.youtube.com/@2%EC%A7%80%EC%83%81"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-youtube me-3"
              >
                <svg class="yt-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
                YouTube
              </a>
              <span v-if="authStore.isLoggedIn" class="welcome-text">
                🎉 {{ authStore.user?.username }}님, 환영합니다!
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 물결 구분선 -->
      <div class="wave-divider">
        <svg viewBox="0 0 1200 80" preserveAspectRatio="none">
          <path d="M0,40 C300,80 900,0 1200,40 L1200,80 L0,80 Z" fill="#111827"/>
        </svg>
      </div>
    </section>

    <!-- 소개 카드 섹션 -->
    <section class="info-section">
      <div class="container">
        <h2 class="section-title text-center mb-5">
          이지상:) 소개
        </h2>
        <div class="row g-4">
          <div class="col-md-4" v-for="card in infoCards" :key="card.title">
            <div class="info-card">
              <div class="card-icon">{{ card.icon }}</div>
              <h3 class="card-title">{{ card.title }}</h3>
              <p class="card-desc">{{ card.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 방송 일정 섹션 -->
    <section class="schedule-section">
      <div class="container">
        <h2 class="section-title text-center mb-5">방송 일정</h2>
        <div class="schedule-grid">
          <div
            v-for="day in schedule"
            :key="day.day"
            class="schedule-card"
            :class="{ active: day.isOn }"
          >
            <div class="day-name">{{ day.day }}</div>
            <div class="day-status">
              <span v-if="day.isOn" class="status-on">📺 방송</span>
              <span v-else class="status-off">휴방</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA 섹션 -->
    <section class="cta-section">
      <div class="container text-center">
        <h2 class="cta-title">지금 바로 함께해요!</h2>
        <p class="cta-desc">이지상:)의 방송을 놓치지 마세요</p>
        <a
          href="https://www.sooplive.com/station/jrdart"
          target="_blank"
          rel="noopener noreferrer"
          class="btn btn-cta"
        >
          <img src="/soop_logo.png" alt="SOOP" class="soop-cta-logo" />
          으로 이동하기
        </a>
      </div>
    </section>

    <!-- 푸터 -->
    <footer class="site-footer">
      <div class="container text-center">
        <p>© 2024 이지상:) 팬 사이트 | 공식 팬 커뮤니티</p>
        <p class="footer-sub">이 사이트는 공식 팬이 제작한 비공식 팬 사이트입니다.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const infoCards = [
  {
    icon: '🎮',
    title: '게임 방송',
    desc: '다양한 게임을 재미있고 유쾌하게 즐기는 게임 방송! 웃음이 끊이지 않는 방송으로 시청자들과 함께 즐깁니다.',
  },
  {
    icon: '😄',
    title: '유쾌한 분위기',
    desc: '항상 밝고 긍정적인 에너지로 시청자들에게 즐거움을 전달합니다. 이지상:)의 방송을 보면 기분이 좋아져요!',
  },
  {
    icon: '💬',
    title: '소통 방송',
    desc: '채팅으로 시청자와 활발하게 소통하는 방송! 여러분의 이야기를 듣고 함께 웃고 즐기는 방송입니다.',
  },
]

const schedule = [
  { day: '월', isOn: true },
  { day: '화', isOn: true },
  { day: '수', isOn: true },
  { day: '목', isOn: true },
  { day: '금', isOn: true },
  { day: '토', isOn: true },
  { day: '일', isOn: false },
]
</script>

<style scoped>
/* 히어로 섹션 */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #533483 100%);
  padding: 80px 0 0;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(83, 52, 131, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.min-vh-hero {
  min-height: 85vh;
  padding-bottom: 60px;
}

/* 프로필 */
.profile-container {
  display: inline-block;
}

.profile-ring {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffc107, #ff6b35, #e91e8c);
  padding: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 60px rgba(255, 193, 7, 0.4);
  animation: pulse-ring 3s ease-in-out infinite;
}

@keyframes pulse-ring {
  0%, 100% { box-shadow: 0 0 40px rgba(255, 193, 7, 0.4); }
  50% { box-shadow: 0 0 80px rgba(255, 193, 7, 0.7); }
}

.profile-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.profile-logo-img {
  width: 78%;
  height: 78%;
  object-fit: contain;
  object-position: center;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 6px 16px;
  color: #fff;
  font-size: 0.9rem;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff4757;
  animation: blink 1.5s ease-in-out infinite;
}

.soop-badge-logo {
  height: 18px;
  width: auto;
  object-fit: contain;
}

.soop-btn-logo {
  height: 22px;
  width: auto;
  object-fit: contain;
  vertical-align: middle;
}

.soop-cta-logo {
  height: 28px;
  width: auto;
  object-fit: contain;
  vertical-align: middle;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}

/* 텍스트 */
.hero-tag {
  color: #ffc107;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.hero-title {
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 900;
  color: #fff;
  line-height: 1.1;
  margin-bottom: 1rem;
}

.smile-emoji {
  color: #ffc107;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.7;
  margin-bottom: 2rem;
}

/* 통계 */
.hero-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffc107;
}

.stat-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
}

/* 버튼 */
.btn-soop {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #ff6b35, #ffc107);
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255, 107, 53, 0.4);
}

.btn-soop:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 107, 53, 0.6);
  color: #fff;
}

.btn-youtube {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #ff0000;
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255, 0, 0, 0.35);
}

.btn-youtube:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 0, 0, 0.55);
  color: #fff;
}

.yt-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.btn-outline-fan {
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: #fff;
  padding: 13px 28px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-outline-fan:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #fff;
  color: #fff;
}

.welcome-text {
  color: #ffc107;
  font-weight: 600;
  font-size: 1rem;
}

/* 물결 */
.wave-divider {
  height: 80px;
  margin-top: -1px;
}

.wave-divider svg {
  width: 100%;
  height: 100%;
}

/* 소개 섹션 */
.info-section {
  background: #111827;
  padding: 80px 0;
}

.section-title {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
}

.info-card {
  background: linear-gradient(135deg, #1f2937, #1a1a2e);
  border: 1px solid rgba(255, 193, 7, 0.2);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s;
  height: 100%;
}

.info-card:hover {
  transform: translateY(-6px);
  border-color: rgba(255, 193, 7, 0.5);
  box-shadow: 0 12px 40px rgba(255, 193, 7, 0.15);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffc107;
  margin-bottom: 0.75rem;
}

.card-desc {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.7;
  font-size: 0.95rem;
}

/* 방송 일정 */
.schedule-section {
  background: #0d0d1a;
  padding: 80px 0;
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
  max-width: 700px;
  margin: 0 auto;
}

.schedule-card {
  background: #1f2937;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.2rem 0.5rem;
  text-align: center;
  transition: all 0.3s;
}

.schedule-card.active {
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  border-color: rgba(255, 193, 7, 0.4);
}

.day-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
}

.status-on {
  font-size: 0.75rem;
  color: #ffc107;
  font-weight: 600;
}

.status-off {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.3);
}

/* CTA */
.cta-section {
  background: linear-gradient(135deg, #0f3460, #533483);
  padding: 80px 0;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #fff;
  margin-bottom: 1rem;
}

.cta-desc {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 2rem;
}

.btn-cta {
  background: linear-gradient(135deg, #ffc107, #ff6b35);
  color: #fff;
  border: none;
  padding: 16px 40px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255, 193, 7, 0.4);
}

.btn-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 40px rgba(255, 193, 7, 0.6);
  color: #fff;
}

/* 푸터 */
.site-footer {
  background: #0d0d1a;
  padding: 40px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.site-footer p {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.footer-sub {
  font-size: 0.8rem !important;
  color: rgba(255, 255, 255, 0.3) !important;
}

@media (max-width: 768px) {
  .hero-stats {
    justify-content: center;
  }
  .hero-buttons {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  .schedule-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
