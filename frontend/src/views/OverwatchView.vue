<template>
  <div class="ow-page">

    <!-- 헤더 -->
    <section class="ow-header">
      <div class="ow-header-bg"></div>
      <div class="container position-relative text-center">
        <img src="/overwatch_logo.png" alt="Overwatch" class="ow-logo-hero" />
        <h1 class="ow-main-title">Overwatch</h1>

        <!-- 서브 탭 네비게이션 -->
        <div class="ow-subnav">
          <router-link to="/overwatch/skills" class="ow-tab" active-class="ow-tab-active">
            📊 티어표
          </router-link>
          <router-link to="/overwatch/bracket" class="ow-tab" active-class="ow-tab-active">
            ⚡ 팀짜기
          </router-link>
        </div>
      </div>
    </section>

    <!-- 서브 페이지 렌더링 -->
    <router-view />

    <!-- 푸터 -->
    <footer class="ow-footer">
      <div class="container text-center">
        <p>© Ji-Sang Nakwon | Overwatch</p>
      </div>
    </footer>

  </div>
</template>

<style scoped>
.ow-page {
  min-height: 100vh;
  background: #0d0d1a;
  color: #e0e0e0;
}

/* 헤더 */
.ow-header {
  position: relative;
  background: linear-gradient(135deg, #1a0a00 0%, #2b1a00 40%, #1a1a2e 100%);
  padding: 24px 0 0;
  overflow: hidden;
}

.ow-header-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(249, 158, 26, 0.2) 0%, transparent 65%);
  pointer-events: none;
}

.ow-logo-hero {
  height: 52px;
  width: auto;
  object-fit: contain;
  margin-bottom: 0.4rem;
  filter: drop-shadow(0 0 16px rgba(249, 158, 26, 0.5));
}

.ow-main-title {
  font-family: 'Permanent Marker', cursive;
  font-size: clamp(1.2rem, 3vw, 1.7rem);
  color: #fff;
  margin-bottom: 0.6rem;
}

/* 서브 탭 */
.ow-subnav {
  display: inline-flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px 50px 0 0;
  padding: 6px 8px 0;
}

.ow-tab {
  padding: 10px 28px;
  border-radius: 40px 40px 0 0;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.25s;
  border-bottom: 3px solid transparent;
}

.ow-tab:hover {
  color: #f99e1a;
  background: rgba(249, 158, 26, 0.08);
}

.ow-tab-active {
  color: #f99e1a !important;
  background: rgba(249, 158, 26, 0.12) !important;
  border-bottom-color: #f99e1a !important;
}

/* 푸터 */
.ow-footer {
  padding: 30px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.ow-footer p {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.85rem;
  margin: 0;
}
</style>
