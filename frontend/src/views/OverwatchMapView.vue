<template>
  <div class="map-page">
    <div class="container">

      <!-- 안내 문구 -->
      <p class="guide-text">
        ✔ 맵 클릭으로 각각 제외 가능&nbsp;&nbsp;|&nbsp;&nbsp;
        <span class="mz-label">빨간 글씨</span>는 MZ맵입니다
      </p>

      <!-- 카테고리 그리드 -->
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.name"
          class="category-card"
          :class="{ disabled: !cat.enabled }"
        >
          <!-- 카테고리 헤더 -->
          <div class="cat-header" @click="toggleCategory(cat)">
            <input
              type="checkbox"
              :checked="cat.enabled"
              @click.stop="toggleCategory(cat)"
              class="cat-checkbox"
            />
            <span class="cat-name" :class="{ 'cat-disabled': !cat.enabled }">
              {{ cat.name }}
            </span>
          </div>

          <!-- 맵 목록 -->
          <div class="map-chips">
            <button
              v-for="map in cat.maps"
              :key="map.name"
              class="map-chip"
              :class="{
                'chip-excluded': map.excluded,
                'chip-mz': map.mz && !map.excluded,
                'chip-disabled-cat': !cat.enabled,
              }"
              @click="toggleMap(cat, map)"
              :title="map.mz ? 'MZ맵' : ''"
            >
              {{ map.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- 결과 표시 -->
      <div class="result-area">
        <transition name="fade" mode="out-in">
          <div v-if="result" key="result" class="result-box">
            <div class="result-label">추천 맵</div>
            <div class="result-map" :class="{ 'result-mz': result.mz }">
              {{ result.name }}
            </div>
            <div class="result-cat">{{ result.category }}</div>
            <div v-if="result.mz" class="result-mz-badge">MZ맵</div>
          </div>
          <div v-else key="placeholder" class="result-placeholder">
            추천 버튼을 눌러주세요
          </div>
        </transition>
      </div>

      <!-- 버튼 -->
      <div class="btn-row">
        <button class="btn-recommend" @click="recommend">
          🎲 맵 랜덤 추천
        </button>
        <div class="active-count">활성 맵: {{ activeCount }}개</div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const categories = ref([
  {
    name: '쟁탈',
    enabled: true,
    maps: [
      { name: '네팔',      mz: false, excluded: false },
      { name: '리장 타워', mz: false, excluded: false },
      { name: '부산',      mz: false, excluded: false },
      { name: '사모아',    mz: true,  excluded: false },
      { name: '오아시스',  mz: false, excluded: false },
      { name: '일리오스',  mz: false, excluded: false },
    ],
  },
  {
    name: '호위',
    enabled: true,
    maps: [
      { name: '66번 국도',    mz: false, excluded: false },
      { name: '지브롤터',     mz: false, excluded: false },
      { name: '도라도',       mz: false, excluded: false },
      { name: '리알토',       mz: false, excluded: false },
      { name: '삼발리 수도원',mz: true,  excluded: false },
      { name: '서킷 로얄',   mz: true,  excluded: false },
      { name: '쓰레기촌',    mz: false, excluded: false },
      { name: '하바나',       mz: false, excluded: false },
    ],
  },
  {
    name: '혼합',
    enabled: true,
    maps: [
      { name: '눔바니',      mz: false, excluded: false },
      { name: '미드타운',    mz: false, excluded: false },
      { name: '블리자드 월드', mz: false, excluded: false },
      { name: '아이헨발데',  mz: false, excluded: false },
      { name: '왕의 길',     mz: false, excluded: false },
      { name: '파라이수',    mz: true,  excluded: false },
      { name: '할리우드',    mz: false, excluded: false },
    ],
  },
  {
    name: '밀기',
    enabled: true,
    maps: [
      { name: '뉴 퀸 스트리트', mz: false, excluded: false },
      { name: '루나사피',       mz: false, excluded: false },
      { name: '이스페란사',     mz: true,  excluded: false },
      { name: '콜로세오',       mz: true,  excluded: false },
    ],
  },
  {
    name: '플래시포인트',
    enabled: true,
    maps: [
      { name: '뉴 정크 시티', mz: false, excluded: false },
      { name: '수라바사',     mz: true,  excluded: false },
      { name: '아틀리스',     mz: true,  excluded: false },
    ],
  },
  {
    name: '점령',
    enabled: true,
    maps: [
      { name: '볼스카야 인더스트리', mz: false, excluded: false },
      { name: '아누비스 신전',       mz: false, excluded: false },
      { name: '파리',               mz: false, excluded: false },
      { name: '하나무라',            mz: false, excluded: false },
      { name: '호라이즌 달 기지',    mz: false, excluded: false },
    ],
  },
])

const result = ref(null)

const activeCount = computed(() => {
  let count = 0
  for (const cat of categories.value) {
    if (!cat.enabled) continue
    for (const map of cat.maps) {
      if (!map.excluded) count++
    }
  }
  return count
})

const toggleCategory = (cat) => {
  cat.enabled = !cat.enabled
  result.value = null
}

const toggleMap = (cat, map) => {
  if (!cat.enabled) return
  map.excluded = !map.excluded
  result.value = null
}

const recommend = () => {
  const pool = []
  for (const cat of categories.value) {
    if (!cat.enabled) continue
    for (const map of cat.maps) {
      if (!map.excluded) pool.push({ ...map, category: cat.name })
    }
  }
  if (pool.length === 0) {
    result.value = null
    alert('활성화된 맵이 없습니다!')
    return
  }
  result.value = pool[Math.floor(Math.random() * pool.length)]
}
</script>

<style scoped>
.map-page {
  padding: 40px 0 60px;
}

.guide-text {
  text-align: center;
  font-size: 0.82rem;
  color: rgba(255,255,255,0.4);
  margin-bottom: 28px;
}
.mz-label { color: #ff5252; font-weight: 700; }

/* ── 카테고리 그리드 ── */
.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-bottom: 28px;
}

@media (max-width: 900px) {
  .category-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .category-grid { grid-template-columns: 1fr; }
}

.category-card {
  background: #12172a;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px 16px;
  transition: border-color 0.2s, opacity 0.2s;
}
.category-card.disabled {
  opacity: 0.45;
  border-color: rgba(255,255,255,0.04);
}

/* ── 카테고리 헤더 ── */
.cat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  user-select: none;
}
.cat-checkbox {
  width: 16px;
  height: 16px;
  accent-color: #4fc3f7;
  cursor: pointer;
  flex-shrink: 0;
}
.cat-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #4fc3f7;
  letter-spacing: 0.3px;
}
.cat-name.cat-disabled { color: rgba(79,195,247,0.4); }

/* ── 맵 칩 ── */
.map-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.map-chip {
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.85);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.map-chip:hover {
  border-color: rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
}

/* MZ맵 */
.map-chip.chip-mz {
  color: #ff5252;
  border-color: rgba(255,82,82,0.3);
  background: rgba(255,82,82,0.07);
}
.map-chip.chip-mz:hover {
  background: rgba(255,82,82,0.15);
  border-color: rgba(255,82,82,0.5);
}

/* 제외됨 */
.map-chip.chip-excluded {
  color: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.06);
  background: rgba(0,0,0,0.2);
  text-decoration: line-through;
}
.map-chip.chip-excluded:hover {
  color: rgba(255,255,255,0.4);
  border-color: rgba(255,255,255,0.15);
}

/* 카테고리 비활성화 시 */
.map-chip.chip-disabled-cat {
  cursor: not-allowed;
  pointer-events: none;
}

/* ── 결과 영역 ── */
.result-area {
  min-height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.result-placeholder {
  font-size: 0.95rem;
  color: rgba(255,255,255,0.2);
  font-weight: 600;
}

.result-box {
  text-align: center;
}
.result-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: rgba(255,255,255,0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.result-map {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 4px;
}
.result-map.result-mz { color: #ff5252; }
.result-cat {
  font-size: 0.8rem;
  color: rgba(79,195,247,0.7);
  font-weight: 600;
}
.result-mz-badge {
  display: inline-block;
  margin-top: 6px;
  padding: 2px 10px;
  border-radius: 20px;
  background: rgba(255,82,82,0.15);
  border: 1px solid rgba(255,82,82,0.3);
  color: #ff5252;
  font-size: 0.72rem;
  font-weight: 700;
}

/* ── 버튼 영역 ── */
.btn-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.btn-recommend {
  padding: 14px 48px;
  border-radius: 50px;
  border: none;
  background: linear-gradient(135deg, #43a047, #2e7d32);
  color: #fff;
  font-size: 1.05rem;
  font-weight: 800;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.1s;
  letter-spacing: 0.3px;
}
.btn-recommend:hover { opacity: 0.88; }
.btn-recommend:active { transform: scale(0.97); }

.active-count {
  font-size: 0.78rem;
  color: rgba(255,255,255,0.25);
}

/* ── 트랜지션 ── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s, transform 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(8px); }
</style>
