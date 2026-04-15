<template>
  <div class="bracket-page">

    <!-- 사이드바 토글 탭 -->
    <button class="sidebar-tab" :class="{ open: sidebarOpen }" @click="sidebarOpen = !sidebarOpen">
      <span class="sidebar-tab-icon">{{ sidebarOpen ? '▶' : '◀' }}</span>
      <span class="sidebar-tab-text">티어표</span>
    </button>

    <!-- 스트리머 사이드바 -->
    <transition name="sidebar-slide">
      <div v-if="sidebarOpen" class="streamer-sidebar">
        <div class="sidebar-header">
          <span class="sidebar-title">📊 스트리머 목록</span>
          <button class="sidebar-close" @click="sidebarOpen = false">✕</button>
        </div>

        <!-- 검색 -->
        <div class="sidebar-search-wrap">
          <input v-model="sideSearch" class="sidebar-search" placeholder="🔍 이름 검색..." />
        </div>

        <!-- 포지션 필터 -->
        <div class="sidebar-filter-group">
          <button
            v-for="p in sidePosFilters" :key="p.value"
            :class="['sf-btn', p.cls, { active: sidePosFilter === p.value }]"
            @click="sidePosFilter = p.value"
          >{{ p.label }}</button>
        </div>

        <!-- 학교 필터 -->
        <div class="sidebar-filter-group">
          <button
            v-for="s in sideSchoolFilters" :key="s.value"
            :class="['sf-btn', s.cls, { active: sideSchoolFilter === s.value }]"
            @click="sideSchoolFilter = s.value"
          >{{ s.label }}</button>
        </div>

        <!-- 결과 수 -->
        <div class="sidebar-count">{{ filteredSideStreamers.length }}명</div>

        <!-- 스트리머 목록 -->
        <div class="sidebar-list">
          <div
            v-for="s in filteredSideStreamers"
            :key="s.name"
            class="sidebar-streamer-row"
          >
            <span class="sb-name">{{ s.name }}</span>
            <div class="sb-badges">
              <span :class="['sb-pos', posClass(s.mainPos)]">{{ posIcon(s.mainPos) }}</span>
              <span :class="['sb-tier', gradeClass(s.mainTier)]">{{ s.mainTier }}</span>
              <template v-if="s.subPos">
                <span class="sb-sep">·</span>
                <span :class="['sb-pos sb-sub', posClass(s.subPos)]">{{ posIcon(s.subPos) }}</span>
                <span :class="['sb-tier', gradeClass(s.subTier)]">{{ s.subTier }}</span>
              </template>
            </div>
          </div>
          <div v-if="filteredSideStreamers.length === 0" class="sidebar-empty">
            해당 조건의 스트리머 없음
          </div>
        </div>
      </div>
    </transition>

    <!-- 메인 컨텐츠 -->
    <div class="bracket-main" :class="{ shifted: sidebarOpen }">
      <div class="container">

        <!-- 매치 타입 선택 -->
        <div class="text-center mb-5">
          <div class="type-selector">
            <button :class="['type-btn', { active: matchType === '5v5' }]" @click="setMatchType('5v5')">5 vs 5</button>
            <button :class="['type-btn', { active: matchType === '6v6' }]" @click="setMatchType('6v6')">6 vs 6</button>
          </div>
          <p class="type-desc">팀당 {{ perTeam }}명 · 총 {{ perTeam * 2 }}명</p>
        </div>

        <!-- 랜덤 배정 버튼 -->
        <div class="text-center mb-4">
          <button class="random-btn" @click="randomize">🎲 랜덤 배정</button>
          <button v-if="assigned" class="reset-btn" @click="resetResult">초기화</button>
        </div>

        <!-- 배정 결과 -->
        <transition name="result-fade">
          <div v-if="assigned" class="match-body">

            <!-- Team A -->
            <div class="team-card team-a">
              <div class="team-header">
                <span class="team-badge a">TEAM A</span>
              </div>
              <div class="player-list">
                <div v-for="(player, i) in teamA" :key="i" class="player-row">
                  <span :class="['player-role', player.cls]">{{ player.icon }} {{ player.label }}</span>
                  <span class="player-name">{{ player.name || '미정' }}</span>
                  <span v-if="player.tier" :class="['result-tier', gradeClass(player.tier)]">{{ player.tier }}</span>
                </div>
              </div>
            </div>

            <!-- VS -->
            <div class="vs-divider">
              <div class="vs-circle">VS</div>
            </div>

            <!-- Team B -->
            <div class="team-card team-b">
              <div class="team-header">
                <span class="team-badge b">TEAM B</span>
              </div>
              <div class="player-list">
                <div v-for="(player, i) in teamB" :key="i" class="player-row">
                  <span :class="['player-role', player.cls]">{{ player.icon }} {{ player.label }}</span>
                  <span class="player-name">{{ player.name || '미정' }}</span>
                  <span v-if="player.tier" :class="['result-tier', gradeClass(player.tier)]">{{ player.tier }}</span>
                </div>
              </div>
            </div>

          </div>
        </transition>

        <!-- 맵 추첨 (배정 완료 후 표시) -->
        <transition name="result-fade">
          <div v-if="assigned" class="map-section mb-5">
            <div class="map-section-title">🗺️ 맵 추첨</div>
            <p class="map-guide">카테고리 또는 맵을 클릭해서 제외할 수 있습니다</p>

            <div class="map-category-grid">
              <div
                v-for="cat in mapCategories"
                :key="cat.name"
                class="map-cat-card"
                :class="{ 'cat-off': !cat.enabled }"
              >
                <div class="map-cat-header" @click="toggleMapCat(cat)">
                  <input type="checkbox" :checked="cat.enabled" @click.stop="toggleMapCat(cat)" class="map-cat-check" />
                  <span class="map-cat-name">{{ cat.name }}</span>
                </div>
                <div class="map-chips">
                  <button
                    v-for="map in cat.maps"
                    :key="map.name"
                    class="map-chip"
                    :class="{ 'chip-excluded': map.excluded, 'chip-cat-off': !cat.enabled }"
                    @click="toggleMap(cat, map)"
                  >{{ map.name }}</button>
                </div>
              </div>
            </div>

            <div class="map-result-row">
              <button class="btn-map-random" @click="recommendMap">🎲 맵 랜덤 추첨</button>
              <transition name="fade" mode="out-in">
                <span v-if="mapResult" key="r" class="map-result-name">{{ mapResult.name }}
                  <span class="map-result-cat">{{ mapResult.category }}</span>
                </span>
                <span v-else key="p" class="map-result-placeholder">추첨 버튼을 눌러주세요</span>
              </transition>
              <span class="map-active-count">{{ mapActiveCount }}개 활성</span>
            </div>
          </div>
        </transition>

        <!-- 참가자 입력 -->
        <div class="input-section mb-5">
          <h3 class="section-title">참가자 등록</h3>

          <div v-for="cfg in roleConfig" :key="cfg.key" class="role-inputs">
            <div class="role-input-header">
              <span :class="['role-badge', cfg.cls]">{{ cfg.icon }} {{ cfg.role }}</span>
            </div>

            <!-- 쌍별 입력 -->
            <div v-for="p in cfg.pairs" :key="p" class="pair-row">
              <span class="pair-num">{{ p }}조</span>
              <div class="pair-cells">
                <!-- 왼쪽 칸 -->
                <div class="name-cell-wrap">
                  <div class="name-cell">
                    <input
                      v-model="participants[cfg.key][(p - 1) * 2]"
                      class="name-input"
                      :placeholder="cfg.role + ' ' + ((p - 1) * 2 + 1)"
                      @focus="openDrop(cfg.key, (p - 1) * 2, cfg.role)"
                      @blur="closeDrop"
                    />
                    <span
                      v-if="getTier(cfg.key, (p - 1) * 2, cfg.role)"
                      :class="['cell-tier', gradeClass(getTier(cfg.key, (p - 1) * 2, cfg.role))]"
                    >{{ getTier(cfg.key, (p - 1) * 2, cfg.role) }}</span>
                  </div>
                  <div v-if="isOpen(cfg.key, (p - 1) * 2)" class="suggestions">
                    <div
                      v-for="s in getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2], cfg.key, (p - 1) * 2)"
                      :key="s.name"
                      class="suggestion-item"
                      @mousedown.prevent="pick(cfg.key, (p - 1) * 2, s.name)"
                    >
                      <span class="sug-name">{{ s.name }}</span>
                      <span :class="['sug-tier', gradeClass(s.tier)]">{{ s.tier }}</span>
                      <span class="sug-pos-type">{{ s.posType }}</span>
                    </div>
                    <div v-if="getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2], cfg.key, (p - 1) * 2).length === 0" class="sug-empty">
                      일치하는 스트리머 없음
                    </div>
                  </div>
                </div>

                <div class="pair-divider">≈</div>

                <!-- 오른쪽 칸 -->
                <div class="name-cell-wrap">
                  <div class="name-cell">
                    <input
                      v-model="participants[cfg.key][(p - 1) * 2 + 1]"
                      class="name-input"
                      :placeholder="cfg.role + ' ' + ((p - 1) * 2 + 2)"
                      @focus="openDrop(cfg.key, (p - 1) * 2 + 1, cfg.role)"
                      @blur="closeDrop"
                    />
                    <span
                      v-if="getTier(cfg.key, (p - 1) * 2 + 1, cfg.role)"
                      :class="['cell-tier', gradeClass(getTier(cfg.key, (p - 1) * 2 + 1, cfg.role))]"
                    >{{ getTier(cfg.key, (p - 1) * 2 + 1, cfg.role) }}</span>
                  </div>
                  <div v-if="isOpen(cfg.key, (p - 1) * 2 + 1)" class="suggestions">
                    <div
                      v-for="s in getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2 + 1], cfg.key, (p - 1) * 2 + 1)"
                      :key="s.name"
                      class="suggestion-item"
                      @mousedown.prevent="pick(cfg.key, (p - 1) * 2 + 1, s.name)"
                    >
                      <span class="sug-name">{{ s.name }}</span>
                      <span :class="['sug-tier', gradeClass(s.tier)]">{{ s.tier }}</span>
                      <span class="sug-pos-type">{{ s.posType }}</span>
                    </div>
                    <div v-if="getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2 + 1], cfg.key, (p - 1) * 2 + 1).length === 0" class="sug-empty">
                      일치하는 스트리머 없음
                    </div>
                  </div>
                </div>
              </div>

              <!-- 묶음 버튼 -->
              <button
                :class="['link-btn', pairLinks[`${cfg.key}-${p-1}`] ? `link-g${pairLinks[`${cfg.key}-${p-1}`]}` : '']"
                @click="cycleLink(cfg.key, p-1)"
                :title="pairLinks[`${cfg.key}-${p-1}`] ? `묶음 ${pairLinks[`${cfg.key}-${p-1}`]}` : '묶음 없음'"
              >
                🔗 {{ pairLinks[`${cfg.key}-${p-1}`] ? `묶음 ${pairLinks[`${cfg.key}-${p-1}`]}` : '묶기' }}
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStreamersStore } from '@/stores/streamers.js'

const streamersStore = useStreamersStore()
const streamers = computed(() => streamersStore.streamers)
onMounted(() => streamersStore.fetchStreamers())

const matchType = ref('5v5')
const perTeam = computed(() => matchType.value === '5v5' ? 5 : 6)

const roleConfig = computed(() => [
  {
    key: 'tank', role: '탱커', icon: '🛡️', cls: 'tank',
    perTeam: matchType.value === '5v5' ? 1 : 2,
    pairs:   matchType.value === '5v5' ? 1 : 2,
  },
  { key: 'dps',  role: '딜러', icon: '⚔️', cls: 'dps',  perTeam: 2, pairs: 2 },
  { key: 'heal', role: '힐러', icon: '💊', cls: 'heal', perTeam: 2, pairs: 2 },
])

const participants = reactive({
  tank: Array(4).fill(''),
  dps:  Array(4).fill(''),
  heal: Array(4).fill(''),
})

const pairLinks = reactive({})

const cycleLink = (key, pairIdx) => {
  const k = `${key}-${pairIdx}`
  const cur = pairLinks[k] || 0
  pairLinks[k] = cur >= 3 ? null : cur + 1
}

const teamA    = ref([])
const teamB    = ref([])
const assigned = ref(false)

const randomize = () => {
  const aResult = []
  const bResult = []
  const groupFlips = {}

  for (const cfg of roleConfig.value) {
    for (let p = 0; p < cfg.pairs; p++) {
      const name1 = participants[cfg.key][p * 2]     || ''
      const name2 = participants[cfg.key][p * 2 + 1] || ''
      const group = pairLinks[`${cfg.key}-${p}`]
      let flip
      if (group) {
        if (groupFlips[group] === undefined) groupFlips[group] = Math.random() < 0.5
        flip = groupFlips[group]
      } else {
        flip = Math.random() < 0.5
      }
      const [toA, toB] = flip ? [name1, name2] : [name2, name1]
      aResult.push({ name: toA, icon: cfg.icon, cls: cfg.cls, label: `${cfg.role} ${p + 1}`, tier: getTierByName(toA, cfg.role) })
      bResult.push({ name: toB, icon: cfg.icon, cls: cfg.cls, label: `${cfg.role} ${p + 1}`, tier: getTierByName(toB, cfg.role) })
    }
  }

  teamA.value    = aResult
  teamB.value    = bResult
  assigned.value = true
}

const resetResult = () => { assigned.value = false; teamA.value = []; teamB.value = [] }
const setMatchType = (type) => { matchType.value = type; resetResult() }

/* ── 드롭다운 ── */
const dropKey  = ref(null)
const dropRole = ref(null)

const openDrop  = (key, idx, role) => { dropKey.value = `${key}-${idx}`; dropRole.value = role }
const closeDrop = () => { dropKey.value = null }
const isOpen    = (key, idx) => dropKey.value === `${key}-${idx}`

const pick = (key, idx, name) => { participants[key][idx] = name; dropKey.value = null }

const gradeOrder = { '중1':1,'중2':2,'중3':3,'고1':4,'고2':5,'고3':6 }
const gradeClass = (g) => ({ '측정중':'g-tbd','중1':'g-jh1','중2':'g-jh2','중3':'g-jh3','고1':'g-hs1','고2':'g-hs2','고3':'g-hs3' }[g] || '')
const posClass   = (p) => ({ '딜러':'dps','탱커':'tank','힐러':'healer' }[p] || '')
const posIcon    = (p) => ({ '딜러':'⚔️','탱커':'🛡️','힐러':'💊' }[p] || '')

const midGrades  = ['중1','중2','중3']
const highGrades = ['고1','고2','고3']

const getTierByName = (name, role) => {
  if (!name?.trim()) return null
  const s = streamers.value.find(st => st.name === name.trim())
  if (!s) return null
  if (s.mainPos === role) return s.mainTier
  if (s.subPos  === role) return s.subTier
  return null
}

const getTier = (key, idx, role) => {
  const name = participants[key][idx]?.trim()
  if (!name) return null
  const s = streamers.value.find(st => st.name === name)
  if (!s) return null
  if (s.mainPos === role) return s.mainTier
  if (s.subPos  === role) return s.subTier
  return null
}

const registeredNames = (excludeKey, excludeIdx) => {
  const names = new Set()
  for (const key of ['tank', 'dps', 'heal']) {
    participants[key].forEach((name, idx) => {
      if (name.trim() && !(key === excludeKey && idx === excludeIdx)) names.add(name.trim())
    })
  }
  return names
}

const getSuggestions = (role, query, excludeKey, excludeIdx) => {
  const used = registeredNames(excludeKey, excludeIdx)
  const results = []
  for (const s of streamers.value) {
    if (used.has(s.name)) continue
    const matchQuery = !query.trim() || s.name.includes(query.trim())
    if (!matchQuery) continue
    if (s.mainPos === role) results.push({ name: s.name, tier: s.mainTier, posType: '주포지션' })
    else if (s.subPos === role) results.push({ name: s.name, tier: s.subTier, posType: '보조포지션' })
  }
  return results.sort((a, b) => (gradeOrder[b.tier] ?? 0) - (gradeOrder[a.tier] ?? 0))
}

/* ── 맵 추첨 ── */
const mapCategories = ref([
  { name: '쟁탈',       enabled: true, maps: ['네팔','리장 타워','부산','사모아','오아시스','일리오스'].map(n=>({name:n,excluded:false})) },
  { name: '호위',       enabled: true, maps: ['66번 국도','지브롤터','도라도','리알토','삼발리 수도원','서킷 로얄','쓰레기촌','하바나'].map(n=>({name:n,excluded:false})) },
  { name: '혼합',       enabled: true, maps: ['눔바니','미드타운','블리자드 월드','아이헨발데','왕의 길','파라이수','할리우드'].map(n=>({name:n,excluded:false})) },
  { name: '밀기',       enabled: true, maps: ['뉴 퀸 스트리트','루나사피','이스페란사','콜로세오'].map(n=>({name:n,excluded:false})) },
  { name: '플래시포인트', enabled: true, maps: ['뉴 정크 시티','수라바사','아틀리스'].map(n=>({name:n,excluded:false})) },
  { name: '점령',       enabled: true, maps: ['볼스카야 인더스트리','아누비스 신전','파리','하나무라','호라이즌 달 기지'].map(n=>({name:n,excluded:false})) },
])
const mapResult = ref(null)

const mapActiveCount = computed(() => {
  let c = 0
  for (const cat of mapCategories.value) {
    if (!cat.enabled) continue
    for (const m of cat.maps) { if (!m.excluded) c++ }
  }
  return c
})

const toggleMapCat = (cat) => { cat.enabled = !cat.enabled; mapResult.value = null }
const toggleMap    = (cat, map) => { if (!cat.enabled) return; map.excluded = !map.excluded; mapResult.value = null }

const recommendMap = () => {
  const pool = []
  for (const cat of mapCategories.value) {
    if (!cat.enabled) continue
    for (const m of cat.maps) { if (!m.excluded) pool.push({ name: m.name, category: cat.name }) }
  }
  if (!pool.length) { alert('활성화된 맵이 없습니다!'); return }
  mapResult.value = pool[Math.floor(Math.random() * pool.length)]
}

/* ── 스트리머 사이드바 ── */
const sidebarOpen     = ref(false)
const sideSearch      = ref('')
const sidePosFilter   = ref('전체')
const sideSchoolFilter = ref('전체')

const sidePosFilters = [
  { value: '전체', label: '전체',   cls: 'sf-all' },
  { value: '딜러', label: '⚔️ 딜러', cls: 'sf-dps' },
  { value: '탱커', label: '🛡️ 탱커', cls: 'sf-tank' },
  { value: '힐러', label: '💊 힐러', cls: 'sf-heal' },
]
const sideSchoolFilters = [
  { value: '전체',     label: '전체',     cls: 'sf-all' },
  { value: '중학교',   label: '중학교',   cls: 'sf-mid' },
  { value: '고등학교', label: '고등학교', cls: 'sf-high' },
]

const filteredSideStreamers = computed(() => {
  return streamers.value.filter(s => {
    const nameMatch = !sideSearch.value.trim() || s.name.includes(sideSearch.value.trim())
    const posMatch  =
      sidePosFilter.value === '전체' ||
      s.mainPos === sidePosFilter.value ||
      s.subPos  === sidePosFilter.value
    const schoolMatch =
      sideSchoolFilter.value === '전체'    ? true :
      sideSchoolFilter.value === '중학교'  ? midGrades.includes(s.mainTier) :
      highGrades.includes(s.mainTier)
    return nameMatch && posMatch && schoolMatch
  }).sort((a, b) => (gradeOrder[b.mainTier] ?? 0) - (gradeOrder[a.mainTier] ?? 0))
})
</script>

<style scoped>
.bracket-page {
  padding: 50px 0 60px;
  position: relative;
}

/* ── 메인 컨텐츠 ── */
.bracket-main {
  transition: padding-right 0.35s ease;
}
.bracket-main.shifted {
  padding-right: 320px;
}

/* ── 사이드바 토글 탭 ── */
.sidebar-tab {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 200;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 8px;
  background: #1e2538;
  border: 1px solid rgba(255,255,255,0.12);
  border-right: none;
  border-radius: 10px 0 0 10px;
  cursor: pointer;
  transition: background 0.2s, right 0.35s ease;
  color: rgba(255,255,255,0.6);
}
.sidebar-tab.open {
  right: 300px;
  background: rgba(249,158,26,0.15);
  border-color: rgba(249,158,26,0.35);
  color: #f99e1a;
}
.sidebar-tab:hover { background: rgba(255,255,255,0.08); color: #fff; }
.sidebar-tab.open:hover { background: rgba(249,158,26,0.25); }

.sidebar-tab-icon { font-size: 0.65rem; }
.sidebar-tab-text {
  writing-mode: vertical-rl;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
}

/* ── 사이드바 패널 ── */
.streamer-sidebar {
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  width: 300px;
  background: #141929;
  border-left: 1px solid rgba(255,255,255,0.1);
  z-index: 190;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-slide-enter-active,
.sidebar-slide-leave-active { transition: transform 0.35s ease; }
.sidebar-slide-enter-from,
.sidebar-slide-leave-to { transform: translateX(100%); }

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 16px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  flex-shrink: 0;
}
.sidebar-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #fff;
}
.sidebar-close {
  background: none;
  border: none;
  color: rgba(255,255,255,0.4);
  font-size: 0.95rem;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  transition: color 0.15s;
}
.sidebar-close:hover { color: #fff; }

.sidebar-search-wrap {
  padding: 10px 12px 6px;
  flex-shrink: 0;
}
.sidebar-search {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.06);
  color: #fff;
  font-size: 0.83rem;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s;
}
.sidebar-search::placeholder { color: rgba(255,255,255,0.25); }
.sidebar-search:focus { border-color: rgba(249,158,26,0.5); }

.sidebar-filter-group {
  display: flex;
  gap: 5px;
  padding: 4px 12px;
  flex-wrap: wrap;
  flex-shrink: 0;
}
.sf-btn {
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.45);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.sf-btn:hover { border-color: rgba(255,255,255,0.25); color: rgba(255,255,255,0.8); }

.sf-btn.sf-all.active  { background:rgba(255,255,255,0.12); border-color:rgba(255,255,255,0.4); color:#fff; }
.sf-btn.sf-dps.active  { background:rgba(255,107,53,0.2);  border-color:#ff8c5a; color:#ff8c5a; }
.sf-btn.sf-tank.active { background:rgba(91,133,232,0.2);  border-color:#7da0f0; color:#7da0f0; }
.sf-btn.sf-heal.active { background:rgba(76,175,130,0.2);  border-color:#5dcf9e; color:#5dcf9e; }
.sf-btn.sf-mid.active  { background:rgba(100,200,220,0.2); border-color:#64c8dc; color:#64c8dc; }
.sf-btn.sf-high.active { background:rgba(249,158,26,0.2);  border-color:#f99e1a; color:#f99e1a; }

.sidebar-count {
  padding: 4px 14px 6px;
  font-size: 0.72rem;
  color: rgba(255,255,255,0.25);
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.sidebar-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px 0;
}
.sidebar-list::-webkit-scrollbar { width: 4px; }
.sidebar-list::-webkit-scrollbar-track { background: transparent; }
.sidebar-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

.sidebar-streamer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background 0.12s;
}
.sidebar-streamer-row:hover { background: rgba(255,255,255,0.04); }

.sb-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  flex-shrink: 0;
}

.sb-badges {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.sb-pos {
  font-size: 0.72rem;
  padding: 1px 7px;
  border-radius: 20px;
  font-weight: 600;
  white-space: nowrap;
}
.sb-pos.dps    { background:rgba(255,107,53,0.2);  color:#ff8c5a; border:1px solid rgba(255,107,53,0.3); }
.sb-pos.tank   { background:rgba(91,133,232,0.2);  color:#7da0f0; border:1px solid rgba(91,133,232,0.3); }
.sb-pos.healer { background:rgba(76,175,130,0.2);  color:#5dcf9e; border:1px solid rgba(76,175,130,0.3); }
.sb-pos.sb-sub { opacity: 0.65; }

.sb-tier {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 20px;
}

.sb-sep { color: rgba(255,255,255,0.2); font-size: 0.75rem; }

.sidebar-empty {
  text-align: center;
  padding: 30px 16px;
  font-size: 0.82rem;
  color: rgba(255,255,255,0.25);
}

/* ── 매치 타입 ── */
.type-selector {
  display: inline-flex;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 50px; padding: 4px; gap: 4px; margin-bottom: 0.75rem;
}
.type-btn {
  padding: 8px 32px; border-radius: 50px; border: none;
  background: transparent; color: rgba(255,255,255,0.5);
  font-size: 1rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
}
.type-btn:hover { color: #fff; }
.type-btn.active {
  background: linear-gradient(135deg, #f99e1a, #ff6b35);
  color: #fff; box-shadow: 0 0 16px rgba(249,158,26,0.4);
}
.type-desc { color: rgba(255,255,255,0.35); font-size: 0.85rem; margin: 0; }

/* ── 참가자 입력 ── */
.input-section {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 1.5rem 2rem;
  display: flex; flex-direction: column; gap: 1.4rem;
}
.section-title {
  font-size: 0.85rem; font-weight: 700;
  color: rgba(255,255,255,0.4); letter-spacing: 1px;
  text-transform: uppercase; margin: 0;
}
.role-inputs { display: flex; flex-direction: column; gap: 8px; }
.role-input-header { display: flex; align-items: center; gap: 10px; }
.role-badge {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.78rem; font-weight: 700;
  padding: 3px 12px; border-radius: 20px;
}
.role-badge.tank { background:rgba(91,133,232,0.2);  color:#7da0f0; border:1px solid rgba(91,133,232,0.35); }
.role-badge.dps  { background:rgba(255,107,53,0.2);  color:#ff8c5a; border:1px solid rgba(255,107,53,0.35); }
.role-badge.heal { background:rgba(76,175,130,0.2);  color:#5dcf9e; border:1px solid rgba(76,175,130,0.35); }

.pair-row { display: flex; align-items: center; gap: 10px; }

.link-btn {
  flex-shrink: 0; padding: 4px 10px; border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.12); background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.3); font-size: 0.72rem; font-weight: 600;
  cursor: pointer; white-space: nowrap; transition: all 0.2s;
}
.link-btn:hover { border-color: rgba(255,255,255,0.3); color: rgba(255,255,255,0.6); }
.link-btn.link-g1 { background:rgba(249,158,26,0.15); border-color:rgba(249,158,26,0.5); color:#f99e1a; }
.link-btn.link-g2 { background:rgba(91,133,232,0.15); border-color:rgba(91,133,232,0.5); color:#7da0f0; }
.link-btn.link-g3 { background:rgba(76,175,130,0.15); border-color:rgba(76,175,130,0.5); color:#5dcf9e; }

.pair-num {
  font-size: 0.72rem; font-weight: 700;
  color: rgba(255,255,255,0.25); width: 24px; flex-shrink: 0; text-align: center;
}
.pair-cells { display: flex; align-items: flex-start; gap: 8px; flex: 1; }
.name-cell-wrap { flex: 1; position: relative; }
.name-cell {
  display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px; padding: 8px 14px; transition: border-color 0.2s, background 0.2s;
}
.name-cell:focus-within { border-color: rgba(249,158,26,0.5); background: rgba(255,255,255,0.08); }
.cell-tier { font-size: 0.7rem; font-weight: 800; padding: 1px 7px; border-radius: 20px; flex-shrink: 0; }
.name-input {
  width: 100%; background: transparent; border: none; outline: none;
  color: #fff; font-size: 0.9rem; font-weight: 600;
}
.name-input::placeholder { color: rgba(255,255,255,0.2); font-weight: 400; }

.suggestions {
  position: absolute; top: calc(100% + 4px); left: 0; right: 0;
  background: #1e2438; border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px; overflow: hidden; z-index: 100;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
.suggestion-item {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; cursor: pointer; transition: background 0.15s;
}
.suggestion-item:hover { background: rgba(249,158,26,0.12); }
.sug-name   { flex: 1; font-size: 0.88rem; font-weight: 700; color: #fff; }
.sug-pos-type { font-size: 0.68rem; color: rgba(255,255,255,0.3); flex-shrink: 0; }
.sug-tier { font-size: 0.7rem; font-weight: 800; padding: 1px 7px; border-radius: 20px; flex-shrink: 0; }
.sug-empty { padding: 10px 12px; font-size: 0.82rem; color: rgba(255,255,255,0.3); text-align: center; }

.pair-divider { font-size: 1rem; color: rgba(255,255,255,0.2); font-weight: 700; flex-shrink: 0; }

/* ── 랜덤 버튼 ── */
.random-btn {
  padding: 12px 40px; border-radius: 50px; border: none;
  background: linear-gradient(135deg, #f99e1a, #ff6b35);
  color: #fff; font-size: 1rem; font-weight: 800;
  cursor: pointer; transition: all 0.2s;
  box-shadow: 0 4px 20px rgba(249,158,26,0.35);
}
.random-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 28px rgba(249,158,26,0.5); }
.reset-btn {
  margin-left: 12px; padding: 12px 24px; border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.2); background: transparent;
  color: rgba(255,255,255,0.5); font-size: 0.9rem; font-weight: 600;
  cursor: pointer; transition: all 0.2s;
}
.reset-btn:hover { color: #fff; border-color: rgba(255,255,255,0.4); }

/* ── 결과 ── */
.match-body { display: grid; grid-template-columns: 1fr auto 1fr; align-items: start; }
.team-card {
  background: linear-gradient(145deg, #1a1f2e, #151b2a);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1.5rem;
}
.team-card.team-a { border-left: 3px solid #5b85e8; }
.team-card.team-b { border-right: 3px solid #f99e1a; }
.team-header { margin-bottom: 1.2rem; }
.team-badge { font-size: 0.78rem; font-weight: 800; padding: 4px 14px; border-radius: 20px; letter-spacing: 1px; }
.team-badge.a { background:rgba(91,133,232,0.25); color:#7da0f0; border:1px solid rgba(91,133,232,0.4); }
.team-badge.b { background:rgba(249,158,26,0.25);  color:#f99e1a; border:1px solid rgba(249,158,26,0.4); }
.player-list { display: flex; flex-direction: column; gap: 8px; }
.player-row {
  display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 10px;
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
}
.player-role {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.75rem; font-weight: 700; padding: 2px 10px; border-radius: 20px;
  white-space: nowrap; flex-shrink: 0; width: 76px; justify-content: center;
}
.player-role.tank { background:rgba(91,133,232,0.2);  color:#7da0f0; border:1px solid rgba(91,133,232,0.35); }
.player-role.dps  { background:rgba(255,107,53,0.2);  color:#ff8c5a; border:1px solid rgba(255,107,53,0.35); }
.player-role.heal { background:rgba(76,175,130,0.2);  color:#5dcf9e; border:1px solid rgba(76,175,130,0.35); }
.player-name { font-size: 0.92rem; font-weight: 700; color: #fff; flex: 1; }
.result-tier { font-size: 0.7rem; font-weight: 800; padding: 1px 7px; border-radius: 20px; flex-shrink: 0; }

.vs-divider { display: flex; align-items: center; justify-content: center; padding: 0 1.5rem; padding-top: 3.5rem; }
.vs-circle {
  width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(135deg, #f99e1a, #ff6b35);
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 0.9rem; color: #fff;
  box-shadow: 0 0 24px rgba(249,158,26,0.5); flex-shrink: 0;
}

/* ── 맵 추첨 ── */
.map-section {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 1.4rem 1.8rem; margin-top: 24px;
}
.map-section-title { font-size: 0.85rem; font-weight: 700; color: rgba(255,255,255,0.4); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
.map-guide { font-size: 0.78rem; color: rgba(255,255,255,0.25); margin: 0 0 16px; }
.map-category-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 18px; }
@media (max-width: 900px) { .map-category-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .map-category-grid { grid-template-columns: 1fr; } }
.map-cat-card { background: #12172a; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 12px 14px; transition: opacity 0.2s; }
.map-cat-card.cat-off { opacity: 0.4; }
.map-cat-header { display: flex; align-items: center; gap: 7px; margin-bottom: 10px; cursor: pointer; user-select: none; }
.map-cat-check { width: 14px; height: 14px; accent-color: #4fc3f7; cursor: pointer; flex-shrink: 0; }
.map-cat-name { font-size: 0.82rem; font-weight: 700; color: #4fc3f7; }
.map-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.map-chip {
  padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.8);
  font-size: 0.77rem; font-weight: 500; cursor: pointer; transition: all 0.15s; white-space: nowrap;
}
.map-chip:hover { border-color: rgba(255,255,255,0.28); background: rgba(255,255,255,0.09); }
.map-chip.chip-excluded { color: rgba(255,255,255,0.18); border-color: rgba(255,255,255,0.05); background: rgba(0,0,0,0.2); text-decoration: line-through; }
.map-chip.chip-excluded:hover { color: rgba(255,255,255,0.35); border-color: rgba(255,255,255,0.12); }
.map-chip.chip-cat-off { pointer-events: none; }
.map-result-row { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.btn-map-random {
  padding: 10px 28px; border-radius: 50px; border: none;
  background: linear-gradient(135deg, #43a047, #2e7d32); color: #fff;
  font-size: 0.9rem; font-weight: 800; cursor: pointer;
  transition: opacity 0.15s, transform 0.1s; white-space: nowrap; flex-shrink: 0;
}
.btn-map-random:hover { opacity: 0.88; }
.btn-map-random:active { transform: scale(0.97); }
.map-result-name { font-size: 1.15rem; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px; }
.map-result-cat { font-size: 0.72rem; font-weight: 600; color: rgba(79,195,247,0.7); }
.map-result-placeholder { font-size: 0.88rem; color: rgba(255,255,255,0.2); }
.map-active-count { font-size: 0.75rem; color: rgba(255,255,255,0.2); margin-left: auto; }

/* ── 티어 배지 (공통) ── */
.g-tbd { background:rgba(255,255,255,0.07); color:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.15); }
.g-jh1 { background:rgba(100,149,237,0.25); color:#6495ed; border:1px solid rgba(100,149,237,0.4); }
.g-jh2 { background:rgba(100,200,220,0.25); color:#64c8dc; border:1px solid rgba(100,200,220,0.4); }
.g-jh3 { background:rgba(80,200,160,0.25);  color:#50c8a0; border:1px solid rgba(80,200,160,0.4); }
.g-hs1 { background:rgba(255,193,7,0.2);    color:#ffc107; border:1px solid rgba(255,193,7,0.4); }
.g-hs2 { background:rgba(249,158,26,0.25);  color:#f99e1a; border:1px solid rgba(249,158,26,0.5); }
.g-hs3 { background:rgba(255,100,60,0.25);  color:#ff643c; border:1px solid rgba(255,100,60,0.5); }

/* ── 트랜지션 ── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.result-fade-enter-active { transition: opacity 0.35s, transform 0.35s; }
.result-fade-enter-from   { opacity: 0; transform: translateY(16px); }

/* ── 모바일 ── */
@media (max-width: 768px) {
  .match-body { grid-template-columns: 1fr; gap: 16px; }
  .vs-divider { padding: 0; }
  .team-card.team-a { border-left: none; border-top: 3px solid #5b85e8; }
  .team-card.team-b { border-right: none; border-top: 3px solid #f99e1a; }
  .input-section { padding: 1.25rem; }
  .bracket-main.shifted { padding-right: 0; }
  .streamer-sidebar { width: 100%; }
  .sidebar-tab.open { right: 0; }
}
</style>
