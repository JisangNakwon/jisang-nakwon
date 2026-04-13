<template>
  <div class="bracket-page">
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
        <div v-if="assigned" class="match-body mb-5">

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
                <div
                  v-if="isOpen(cfg.key, (p - 1) * 2)"
                  class="suggestions"
                >
                  <div
                    v-for="s in getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2])"
                    :key="s.name"
                    class="suggestion-item"
                    @mousedown.prevent="pick(cfg.key, (p - 1) * 2, s.name)"
                  >
                    <span class="sug-avatar">{{ s.avatar }}</span>
                    <span class="sug-name">{{ s.name }}</span>
                    <span :class="['sug-tier', gradeClass(s.tier)]">{{ s.tier }}</span>
                    <span class="sug-pos-type">{{ s.posType }}</span>
                  </div>
                  <div v-if="getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2]).length === 0" class="sug-empty">
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
                <div
                  v-if="isOpen(cfg.key, (p - 1) * 2 + 1)"
                  class="suggestions"
                >
                  <div
                    v-for="s in getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2 + 1])"
                    :key="s.name"
                    class="suggestion-item"
                    @mousedown.prevent="pick(cfg.key, (p - 1) * 2 + 1, s.name)"
                  >
                    <span class="sug-avatar">{{ s.avatar }}</span>
                    <span class="sug-name">{{ s.name }}</span>
                    <span :class="['sug-tier', gradeClass(s.tier)]">{{ s.tier }}</span>
                    <span class="sug-pos-type">{{ s.posType }}</span>
                  </div>
                  <div v-if="getSuggestions(cfg.role, participants[cfg.key][(p - 1) * 2 + 1]).length === 0" class="sug-empty">
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
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStreamersStore } from '@/stores/streamers.js'

const streamersStore = useStreamersStore()
const streamers = computed(() => streamersStore.streamers)
onMounted(() => streamersStore.fetchStreamers())

const matchType = ref('5v5')

const perTeam = computed(() => matchType.value === '5v5' ? 5 : 6)

// 포지션별 설정: perTeam = 팀당 인원, pairs = 쌍 수 (= perTeam)
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

// 묶음 그룹: { 'tank-0': 1, 'dps-0': 1, ... } — null이면 묶음 없음
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

  // 묶음 그룹별로 코인 플립 미리 결정
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

const resetResult = () => {
  assigned.value = false
  teamA.value = []
  teamB.value = []
}

const setMatchType = (type) => {
  matchType.value = type
  resetResult()
}

/* ── 드롭다운 ── */
const dropKey   = ref(null)  // 'dps-2' 형태 (key + index)
const dropRole  = ref(null)

const openDrop  = (key, idx, role) => { dropKey.value = `${key}-${idx}`; dropRole.value = role }
const closeDrop = () => { dropKey.value = null }
const isOpen    = (key, idx) => dropKey.value === `${key}-${idx}`

const pick = (key, idx, name) => {
  participants[key][idx] = name
  dropKey.value = null
}

const gradeOrder = { '중1':1,'중2':2,'중3':3,'고1':4,'고2':5,'고3':6 }
const gradeClass = (g) => ({ '측정중':'g-tbd','중1':'g-jh1','중2':'g-jh2','중3':'g-jh3','고1':'g-hs1','고2':'g-hs2','고3':'g-hs3' }[g] || '')

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

const getSuggestions = (role, query) => {
  const results = []
  for (const s of streamers.value) {
    const matchQuery = !query.trim() || s.name.includes(query.trim())
    if (!matchQuery) continue
    if (s.mainPos === role) results.push({ name: s.name, avatar: s.avatar, tier: s.mainTier, posType: '주포지션' })
    else if (s.subPos === role) results.push({ name: s.name, avatar: s.avatar, tier: s.subTier, posType: '보조포지션' })
  }
  return results.sort((a, b) => (gradeOrder[b.tier] ?? 0) - (gradeOrder[a.tier] ?? 0))
}
</script>

<style scoped>
.bracket-page { padding: 50px 0 60px; }

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
.pair-desc {
  font-size: 0.82rem; color: rgba(255,255,255,0.35);
  margin: -0.6rem 0 0; line-height: 1.6;
}
.pair-desc strong { color: #f99e1a; }

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

.role-total { font-size: 0.75rem; color: rgba(255,255,255,0.3); }

/* 쌍 행 */
.pair-row {
  display: flex; align-items: center; gap: 10px;
}

/* ── 묶음 버튼 ── */
.link-btn {
  flex-shrink: 0;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.04);
  color: rgba(255,255,255,0.3);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}
.link-btn:hover { border-color: rgba(255,255,255,0.3); color: rgba(255,255,255,0.6); }

.link-btn.link-g1 { background: rgba(249,158,26,0.15); border-color: rgba(249,158,26,0.5); color: #f99e1a; }
.link-btn.link-g2 { background: rgba(91,133,232,0.15); border-color: rgba(91,133,232,0.5); color: #7da0f0; }
.link-btn.link-g3 { background: rgba(76,175,130,0.15); border-color: rgba(76,175,130,0.5); color: #5dcf9e; }

.pair-num {
  font-size: 0.72rem; font-weight: 700;
  color: rgba(255,255,255,0.25); width: 24px; flex-shrink: 0; text-align: center;
}

.pair-cells {
  display: flex; align-items: flex-start; gap: 8px; flex: 1;
}

.name-cell-wrap {
  flex: 1;
  position: relative;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 8px 14px;
  transition: border-color 0.2s, background 0.2s;
}
.name-cell:focus-within {
  border-color: rgba(249,158,26,0.5);
  background: rgba(255,255,255,0.08);
}

.cell-tier {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 1px 7px;
  border-radius: 20px;
  flex-shrink: 0;
}

.name-input {
  width: 100%; background: transparent; border: none; outline: none;
  color: #fff; font-size: 0.9rem; font-weight: 600;
}
.name-input::placeholder { color: rgba(255,255,255,0.2); font-weight: 400; }

/* ── 드롭다운 ── */
.suggestions {
  position: absolute;
  top: calc(100% + 4px);
  left: 0; right: 0;
  background: #1e2438;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  overflow: hidden;
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.suggestion-item:hover { background: rgba(249,158,26,0.12); }

.sug-avatar { font-size: 1rem; width: 22px; text-align: center; flex-shrink: 0; }
.sug-name   { flex: 1; font-size: 0.88rem; font-weight: 700; color: #fff; }
.sug-pos-type { font-size: 0.68rem; color: rgba(255,255,255,0.3); flex-shrink: 0; }

.sug-tier {
  font-size: 0.7rem; font-weight: 800;
  padding: 1px 7px; border-radius: 20px; flex-shrink: 0;
}
.g-jh1 { background:rgba(100,149,237,0.25); color:#6495ed; border:1px solid rgba(100,149,237,0.4); }
.g-jh2 { background:rgba(100,200,220,0.25); color:#64c8dc; border:1px solid rgba(100,200,220,0.4); }
.g-jh3 { background:rgba(80,200,160,0.25);  color:#50c8a0; border:1px solid rgba(80,200,160,0.4); }
.g-hs1 { background:rgba(255,193,7,0.2);    color:#ffc107; border:1px solid rgba(255,193,7,0.4); }
.g-hs2 { background:rgba(249,158,26,0.25);  color:#f99e1a; border:1px solid rgba(249,158,26,0.5); }
.g-hs3 { background:rgba(255,100,60,0.25);  color:#ff643c; border:1px solid rgba(255,100,60,0.5); }

.sug-empty {
  padding: 10px 12px;
  font-size: 0.82rem;
  color: rgba(255,255,255,0.3);
  text-align: center;
}

.pair-divider {
  font-size: 1rem; color: rgba(255,255,255,0.2);
  font-weight: 700; flex-shrink: 0;
}

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
  border: 1px solid rgba(255,255,255,0.2);
  background: transparent; color: rgba(255,255,255,0.5);
  font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.reset-btn:hover { color: #fff; border-color: rgba(255,255,255,0.4); }

/* ── 결과 ── */
.match-body { display: grid; grid-template-columns: 1fr auto 1fr; align-items: start; }

.team-card {
  background: linear-gradient(145deg, #1a1f2e, #151b2a);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 1.5rem;
}
.team-card.team-a { border-left: 3px solid #5b85e8; }
.team-card.team-b { border-right: 3px solid #f99e1a; }

.team-header { margin-bottom: 1.2rem; }

.team-badge {
  font-size: 0.78rem; font-weight: 800;
  padding: 4px 14px; border-radius: 20px; letter-spacing: 1px;
}
.team-badge.a { background:rgba(91,133,232,0.25); color:#7da0f0; border:1px solid rgba(91,133,232,0.4); }
.team-badge.b { background:rgba(249,158,26,0.25);  color:#f99e1a; border:1px solid rgba(249,158,26,0.4); }

.player-list { display: flex; flex-direction: column; gap: 8px; }

.player-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 12px; border-radius: 10px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
}

.player-role {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.75rem; font-weight: 700;
  padding: 2px 10px; border-radius: 20px;
  white-space: nowrap; flex-shrink: 0; width: 76px; justify-content: center;
}
.player-role.tank { background:rgba(91,133,232,0.2);  color:#7da0f0; border:1px solid rgba(91,133,232,0.35); }
.player-role.dps  { background:rgba(255,107,53,0.2);  color:#ff8c5a; border:1px solid rgba(255,107,53,0.35); }
.player-role.heal { background:rgba(76,175,130,0.2);  color:#5dcf9e; border:1px solid rgba(76,175,130,0.35); }

.player-name { font-size: 0.92rem; font-weight: 700; color: #fff; flex: 1; }

.result-tier {
  font-size: 0.7rem; font-weight: 800;
  padding: 1px 7px; border-radius: 20px; flex-shrink: 0;
}

/* ── VS ── */
.vs-divider {
  display: flex; align-items: center; justify-content: center;
  padding: 0 1.5rem; padding-top: 3.5rem;
}
.vs-circle {
  width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(135deg, #f99e1a, #ff6b35);
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 0.9rem; color: #fff;
  box-shadow: 0 0 24px rgba(249,158,26,0.5); flex-shrink: 0;
}

/* ── 트랜지션 ── */
.result-fade-enter-active { transition: opacity 0.35s, transform 0.35s; }
.result-fade-enter-from   { opacity: 0; transform: translateY(16px); }

/* ── 모바일 ── */
@media (max-width: 768px) {
  .match-body { grid-template-columns: 1fr; gap: 16px; }
  .vs-divider { padding: 0; }
  .team-card.team-a { border-left: none; border-top: 3px solid #5b85e8; }
  .team-card.team-b { border-right: none; border-top: 3px solid #f99e1a; }
  .input-section { padding: 1.25rem; }
}
</style>
