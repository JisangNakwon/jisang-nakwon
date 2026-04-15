<template>
  <div class="skills-page">
    <div class="container">

      <!-- 필터 버튼 -->
      <div class="filter-area mb-4">
        <div class="filter-group">
          <span class="filter-label">주포지션</span>
          <div class="filter-btns">
            <button
              v-for="p in posFilters" :key="p.value"
              :class="['filter-btn', p.cls, { active: selectedPos === p.value }]"
              @click="selectedPos = p.value"
            >{{ p.icon }} {{ p.label }}</button>
          </div>
        </div>
        <div class="filter-group">
          <span class="filter-label">부포지션</span>
          <div class="filter-btns">
            <button
              v-for="p in posFilters" :key="p.value"
              :class="['filter-btn', p.cls, { active: selectedSubPos === p.value }]"
              @click="selectedSubPos = p.value"
            >{{ p.icon }} {{ p.label }}</button>
          </div>
        </div>
        <div class="filter-group">
          <span class="filter-label">학교</span>
          <div class="filter-btns">
            <button
              v-for="s in schoolFilters" :key="s.value"
              :class="['filter-btn', s.cls, { active: selectedSchool === s.value }]"
              @click="selectedSchool = s.value"
            >{{ s.label }}</button>
          </div>
        </div>
        <div class="filter-result">{{ sortedStreamers.length }}명의 스트리머</div>
        <button v-if="isStaff" class="btn-add-streamer" @click="openAdd">+ 스트리머 추가</button>
      </div>

      <!-- 테이블 헤더 -->
      <div class="list-header">
        <div class="col-name">스트리머</div>
        <div class="col-grade sortable" @click="toggleSort('tier')">
          티어 <span class="sort-icon">{{ sortIcon('tier') }}</span>
        </div>
        <div class="col-pos-group sortable" @click="toggleSort('mainPos')">
          주포지션 <span class="sort-icon">{{ sortIcon('mainPos') }}</span>
        </div>
        <div class="col-pos-group sortable" @click="toggleSort('subPos')">
          보조포지션 <span class="sort-icon">{{ sortIcon('subPos') }}</span>
        </div>
        <div class="col-note">비고</div>
        <div v-if="isStaff" class="col-actions"></div>
      </div>

      <!-- 스트리머 리스트 -->
      <transition-group name="row-fade" tag="div" class="streamer-list">
        <div
          v-for="streamer in sortedStreamers"
          :key="streamer.name"
          class="streamer-row"
        >
          <!-- 이름 -->
          <div class="col-name">
            <span class="row-name">{{ streamer.name }}</span>
          </div>

          <!-- 최고 티어 -->
          <div class="col-grade">
            <span :class="['tier-badge', gradeClass(highTier(streamer))]">
              {{ highTier(streamer) }}
            </span>
          </div>

          <!-- 주포지션 + 티어 + 모스트 -->
          <div class="col-pos-group">
            <div class="pos-header">
              <span :class="['pos-tag', posClass(streamer.mainPos)]">
                {{ posIcon(streamer.mainPos) }} {{ streamer.mainPos }}
              </span>
              <span :class="['tier-badge', gradeClass(streamer.mainTier)]">
                {{ streamer.mainTier }}
              </span>
            </div>
            <div class="most-list">
              <span v-for="(champ, i) in streamer.mainMost" :key="i" class="most-chip">
                {{ i + 1 }}. {{ champ }}
              </span>
            </div>
          </div>

          <!-- 보조포지션 + 티어 + 모스트 -->
          <div class="col-pos-group">
            <div class="pos-header">
              <span :class="['pos-tag pos-sub', posClass(streamer.subPos)]">
                {{ posIcon(streamer.subPos) }} {{ streamer.subPos }}
              </span>
              <span :class="['tier-badge', gradeClass(streamer.subTier)]">
                {{ streamer.subTier }}
              </span>
            </div>
            <div class="most-list">
              <span v-for="(champ, i) in streamer.subMost" :key="i" class="most-chip">
                {{ i + 1 }}. {{ champ }}
              </span>
            </div>
          </div>

          <!-- 비고 -->
          <div class="col-note">
            <span class="note-text">{{ streamer.note }}</span>
          </div>

          <!-- 관리 버튼 (스태프만) -->
          <div v-if="isStaff" class="col-actions">
            <button class="btn-edit" @click.stop="openEdit(streamer)" title="수정">✏️</button>
            <button class="btn-delete" @click.stop="deleteStreamer(streamer)" title="삭제">🗑️</button>
          </div>

        </div>
      </transition-group>

      <!-- 결과 없음 -->
      <div v-if="sortedStreamers.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <div class="empty-text">해당 조건의 스트리머가 없습니다</div>
      </div>

    </div>

    <!-- ── 스태프 전용 추가/수정 모달 ── -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h3>{{ editTarget ? '스트리머 수정' : '스트리머 추가' }}</h3>
          <button class="modal-close" @click="showModal = false">✕</button>
        </div>
        <div class="modal-body">

          <!-- 기본 정보 -->
          <div class="form-field">
            <label class="field-label">이름 <span class="required">*</span></label>
            <input v-model="form.name" class="form-input" placeholder="스트리머 이름 입력" />
          </div>

          <!-- 주포지션 -->
          <div class="form-section-title">주포지션</div>
          <div class="form-grid-2">
            <div class="form-field">
              <label class="field-label">포지션</label>
              <select v-model="form.mainPos" class="form-select">
                <option>딜러</option>
                <option>탱커</option>
                <option>힐러</option>
              </select>
            </div>
            <div class="form-field">
              <label class="field-label">티어</label>
              <select v-model="form.mainTier" class="form-select">
                <option>측정중</option>
                <option>중1</option><option>중2</option><option>중3</option>
                <option>고1</option><option>고2</option><option>고3</option>
              </select>
            </div>
          </div>
          <div class="form-field">
            <label class="field-label">모스트 픽</label>
            <div class="form-grid-3">
              <input v-model="form.mainMost[0]" class="form-input" placeholder="1순위" />
              <input v-model="form.mainMost[1]" class="form-input" placeholder="2순위" />
              <input v-model="form.mainMost[2]" class="form-input" placeholder="3순위" />
            </div>
          </div>

          <!-- 보조포지션 -->
          <div class="form-section-title">
            보조포지션
            <label class="sub-toggle">
              <input type="checkbox" v-model="form.hasSubPos" />
              있음
            </label>
          </div>
          <template v-if="form.hasSubPos">
            <div class="form-grid-2">
              <div class="form-field">
                <label class="field-label">포지션</label>
                <select v-model="form.subPos" class="form-select">
                  <option>딜러</option>
                  <option>탱커</option>
                  <option>힐러</option>
                </select>
              </div>
              <div class="form-field">
                <label class="field-label">티어</label>
                <select v-model="form.subTier" class="form-select">
                  <option>측정중</option>
                  <option>중1</option><option>중2</option><option>중3</option>
                  <option>고1</option><option>고2</option><option>고3</option>
                </select>
              </div>
            </div>
            <div class="form-field">
              <label class="field-label">모스트 픽</label>
              <div class="form-grid-3">
                <input v-model="form.subMost[0]" class="form-input" placeholder="1순위" />
                <input v-model="form.subMost[1]" class="form-input" placeholder="2순위" />
                <input v-model="form.subMost[2]" class="form-input" placeholder="3순위" />
              </div>
            </div>
          </template>

          <!-- 비고 -->
          <div class="form-field">
            <label class="field-label">비고</label>
            <input v-model="form.note" class="form-input" placeholder="메모 (선택)" />
          </div>

        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showModal = false">취소</button>
          <button class="btn-save" @click="saveForm">저장</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStreamersStore } from '@/stores/streamers.js'
import { useAuthStore }      from '@/stores/auth.js'

const streamersStore = useStreamersStore()
const authStore      = useAuthStore()
const isStaff        = computed(() => authStore.user?.is_staff)

onMounted(() => streamersStore.fetchStreamers())

const streamers = computed(() => streamersStore.streamers)

// ── 모달 ──
const showModal  = ref(false)
const editTarget = ref(null)   // null = 신규, object = 수정 대상

const emptyForm = () => ({
  name: '',
  mainPos: '딜러', mainTier: '측정중', mainMost: ['', '', ''],
  hasSubPos: false,
  subPos:  '힐러', subTier:  '측정중', subMost:  ['', '', ''],
  note: '',
})
const form = ref(emptyForm())

const openAdd = () => {
  editTarget.value = null
  form.value = emptyForm()
  showModal.value = true
}

const openEdit = (s) => {
  editTarget.value = s
  form.value = {
    name: s.name,
    mainPos: s.mainPos, mainTier: s.mainTier, mainMost: [...s.mainMost],
    hasSubPos: !!s.subPos,
    subPos:  s.subPos  || '힐러', subTier: s.subTier || '측정중', subMost: [...s.subMost],
    note: s.note,
  }
  showModal.value = true
}

const saveForm = async () => {
  const payload = {
    name: form.value.name,
    mainPos: form.value.mainPos, mainTier: form.value.mainTier, mainMost: form.value.mainMost,
    subPos:  form.value.hasSubPos ? form.value.subPos  : '',
    subTier: form.value.hasSubPos ? form.value.subTier : '',
    subMost: form.value.hasSubPos ? form.value.subMost : [],
    note: form.value.note,
  }
  if (editTarget.value) {
    await streamersStore.updateStreamer(editTarget.value.id, payload)
  } else {
    await streamersStore.addStreamer(payload)
  }
  showModal.value = false
}

const deleteStreamer = async (s) => {
  if (confirm(`"${s.name}" 을(를) 삭제하시겠습니까?`)) {
    await streamersStore.deleteStreamer(s.id)
  }
}

const selectedPos    = ref('전체')
const selectedSubPos = ref('전체')
const selectedSchool = ref('전체')
const sortKey        = ref(null)
const sortDir        = ref('asc')

const posFilters = [
  { value: '전체', label: '전체', icon: '👥', cls: 'btn-all' },
  { value: '딜러', label: '딜러', icon: '⚔️', cls: 'btn-dps' },
  { value: '탱커', label: '탱커', icon: '🛡️', cls: 'btn-tank' },
  { value: '힐러', label: '힐러', icon: '💊', cls: 'btn-healer' },
]

const schoolFilters = [
  { value: '전체',     label: '전체',     cls: 'btn-all' },
  { value: '중학교',   label: '중학교',   cls: 'btn-mid' },
  { value: '고등학교', label: '고등학교', cls: 'btn-high' },
  { value: '측정중',   label: '측정중',   cls: 'btn-tbd' },
]

const midGrades  = ['중1', '중2', '중3']
const highGrades = ['고1', '고2', '고3']
const gradeOrder = { '중1':1, '중2':2, '중3':3, '고1':4, '고2':5, '고3':6 }
const posOrder   = { '딜러':1, '탱커':2, '힐러':3 }

const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDir.value = 'asc'
  }
}

const sortIcon = (key) => {
  if (sortKey.value !== key) return '↕'
  return sortDir.value === 'asc' ? '↑' : '↓'
}

const sortedStreamers = computed(() => {
  const filtered = streamers.value.filter(s => {
    const posMatch    = selectedPos.value === '전체' || s.mainPos === selectedPos.value
    const subPosMatch = selectedSubPos.value === '전체' || s.subPos === selectedSubPos.value
    const schoolMatch =
      selectedSchool.value === '전체'    ? true :
      selectedSchool.value === '중학교'  ? midGrades.includes(s.mainTier) :
      selectedSchool.value === '고등학교' ? highGrades.includes(s.mainTier) :
      s.mainTier === '측정중'
    return posMatch && subPosMatch && schoolMatch
  })

  if (!sortKey.value) return filtered

  return [...filtered].sort((a, b) => {
    let va, vb
    if (sortKey.value === 'tier') {
      va = gradeOrder[highTier(a)] ?? 0
      vb = gradeOrder[highTier(b)] ?? 0
    } else if (sortKey.value === 'mainPos') {
      va = posOrder[a.mainPos] ?? 0
      vb = posOrder[b.mainPos] ?? 0
    } else {
      va = posOrder[a.subPos] ?? 0
      vb = posOrder[b.subPos] ?? 0
    }
    return sortDir.value === 'asc' ? va - vb : vb - va
  })
})

const highTier   = (s) => (gradeOrder[s.mainTier] ?? 0) >= (gradeOrder[s.subTier] ?? 0) ? s.mainTier : s.subTier
const gradeClass = (g) => ({ '측정중':'g-tbd','중1':'g-jh1','중2':'g-jh2','중3':'g-jh3','고1':'g-hs1','고2':'g-hs2','고3':'g-hs3' }[g] || '')
const posClass   = (p) => ({ '딜러':'dps','탱커':'tank','힐러':'healer' }[p] || '')
const posIcon    = (p) => ({ '딜러':'⚔️','탱커':'🛡️','힐러':'💊' }[p] || '')
</script>

<style scoped>
.skills-page { padding: 50px 0 60px; }

/* ── 필터 ── */
.filter-area { display:flex; flex-direction:column; align-items:center; gap:12px; }
.filter-group { display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:center; }
.filter-label { font-size:0.8rem; color:rgba(255,255,255,0.45); font-weight:600; min-width:42px; text-align:right; }
.filter-btns  { display:flex; gap:6px; flex-wrap:wrap; }

.filter-btn {
  padding:6px 16px; border-radius:50px;
  border:1px solid rgba(255,255,255,0.15);
  background:rgba(255,255,255,0.05);
  color:rgba(255,255,255,0.6);
  font-size:0.83rem; font-weight:600;
  cursor:pointer; transition:all 0.2s;
}
.filter-btn:hover { border-color:rgba(255,255,255,0.35); color:#fff; }

.filter-btn.btn-all.active    { background:rgba(255,255,255,0.15); border-color:rgba(255,255,255,0.5); color:#fff; }
.filter-btn.btn-dps.active    { background:rgba(255,107,53,0.25);  border-color:#ff8c5a; color:#ff8c5a; }
.filter-btn.btn-tank.active   { background:rgba(91,133,232,0.25);  border-color:#7da0f0; color:#7da0f0; }
.filter-btn.btn-healer.active { background:rgba(76,175,130,0.25);  border-color:#5dcf9e; color:#5dcf9e; }
.filter-btn.btn-mid.active    { background:rgba(100,200,220,0.2);  border-color:#64c8dc; color:#64c8dc; }
.filter-btn.btn-high.active   { background:rgba(249,158,26,0.2);   border-color:#f99e1a; color:#f99e1a; }
.filter-btn.btn-tbd.active    { background:rgba(255,255,255,0.08); border-color:rgba(255,255,255,0.35); color:rgba(255,255,255,0.7); }

.filter-result { font-size:0.8rem; color:rgba(255,255,255,0.3); }

/* ── 테이블 레이아웃 ── */
.col-name      { width: 110px; flex-shrink: 0; }
.col-grade     { width: 64px;  flex-shrink: 0; }
.col-pos-group { flex: 1; min-width: 130px; display: flex; flex-direction: column; gap: 6px; align-items: center; }
.col-note      { width: 160px; flex-shrink: 0; }

/* 헤더 */
.list-header {
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
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.list-header .col-pos-group { justify-content: center; }

.sortable {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}
.sortable:hover { color: rgba(255,255,255,0.7); }
.sort-icon { font-size: 0.75rem; opacity: 0.6; }

/* 리스트 컨테이너 */
.streamer-list { display:flex; flex-direction:column; gap:8px; }

/* 각 행 */
.streamer-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 12px;
  background: linear-gradient(145deg, #1a1f2e, #151b2a);
  border: 1px solid rgba(255,255,255,0.06);
  transition: all 0.2s;
}

.streamer-row:hover {
  border-color: rgba(249,158,26,0.35);
  background: linear-gradient(145deg, #1e2438, #181e2e);
  transform: translateX(4px);
}

.row-name {
  font-size: 0.95rem; font-weight: 700; color: #fff;
}

/* ── 포지션 헤더 (포지션 태그 + 티어 배지) ── */
.pos-header {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

/* ── 티어 배지 ── */
.tier-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 800;
}

.g-tbd { background:rgba(255,255,255,0.07); color:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.15); }
.g-jh1 { background:rgba(100,149,237,0.25); color:#6495ed; border:1px solid rgba(100,149,237,0.4); }
.g-jh2 { background:rgba(100,200,220,0.25); color:#64c8dc; border:1px solid rgba(100,200,220,0.4); }
.g-jh3 { background:rgba(80,200,160,0.25);  color:#50c8a0; border:1px solid rgba(80,200,160,0.4); }
.g-hs1 { background:rgba(255,193,7,0.2);    color:#ffc107; border:1px solid rgba(255,193,7,0.4); }
.g-hs2 { background:rgba(249,158,26,0.25);  color:#f99e1a; border:1px solid rgba(249,158,26,0.5); }
.g-hs3 { background:rgba(255,100,60,0.25);  color:#ff643c; border:1px solid rgba(255,100,60,0.5); }

/* ── 포지션 태그 ── */
.pos-tag {
  display:inline-flex; align-items:center; gap:4px;
  padding:3px 10px; border-radius:20px; font-size:0.8rem; font-weight:600;
  width: fit-content;
}
.pos-tag.dps    { background:rgba(255,107,53,0.2); color:#ff8c5a; border:1px solid rgba(255,107,53,0.35); }
.pos-tag.tank   { background:rgba(91,133,232,0.2); color:#7da0f0; border:1px solid rgba(91,133,232,0.35); }
.pos-tag.healer { background:rgba(76,175,130,0.2); color:#5dcf9e; border:1px solid rgba(76,175,130,0.35); }
.pos-sub { opacity: 0.7; }

/* ── 비고 ── */
.note-text {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.45);
  line-height: 1.5;
  word-break: keep-all;
}

/* ── 모스트 챔피언 ── */
.most-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.most-chip {
  font-size: 0.72rem;
  color: rgba(255,255,255,0.45);
  padding: 1px 0;
  white-space: nowrap;
}

/* ── 트랜지션 ── */
.row-fade-enter-active,
.row-fade-leave-active { transition: opacity 0.2s, transform 0.2s; }
.row-fade-enter-from,
.row-fade-leave-to     { opacity:0; transform:translateX(-8px); }

/* ── 빈 상태 ── */
.empty-state { text-align:center; padding:60px 0; }
.empty-icon  { font-size:3rem; margin-bottom:1rem; }
.empty-text  { color:rgba(255,255,255,0.35); font-size:1rem; }

/* ── 스태프 추가 버튼 ── */
.btn-add-streamer {
  padding: 7px 18px;
  border-radius: 50px;
  border: 1px solid rgba(249,158,26,0.5);
  background: rgba(249,158,26,0.12);
  color: #f99e1a;
  font-size: 0.83rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-add-streamer:hover {
  background: rgba(249,158,26,0.25);
  border-color: #f99e1a;
}

/* ── 관리 버튼 열 ── */
.col-actions {
  width: 68px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.btn-edit, .btn-delete {
  width: 28px; height: 28px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
  opacity: 0.6;
}
.btn-edit   { background: rgba(91,133,232,0.15); }
.btn-delete { background: rgba(255,80,80,0.12); }
.btn-edit:hover   { background: rgba(91,133,232,0.3); opacity: 1; }
.btn-delete:hover { background: rgba(255,80,80,0.25); opacity: 1; }

/* ── 모달 오버레이 ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-box {
  background: #1a1f2e;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.modal-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
}
.modal-close {
  background: none;
  border: none;
  color: rgba(255,255,255,0.4);
  font-size: 1rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: color 0.15s;
}
.modal-close:hover { color: #fff; }

.modal-body {
  padding: 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.72rem;
  font-weight: 700;
  color: rgba(255,255,255,0.35);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-top: 4px;
  border-top: 1px solid rgba(255,255,255,0.07);
  padding-top: 14px;
}
.sub-toggle {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  font-weight: 600;
  color: rgba(255,255,255,0.5);
  cursor: pointer;
  text-transform: none;
  letter-spacing: 0;
}
.sub-toggle input[type="checkbox"] { cursor: pointer; accent-color: #f99e1a; }

/* 그리드 레이아웃 */
.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.form-grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}

/* 개별 필드 */
.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255,255,255,0.45);
  letter-spacing: 0.3px;
}
.required { color: #f99e1a; }

.form-input {
  width: 100%;
  padding: 9px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  color: #fff;
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.15s, background 0.15s;
  box-sizing: border-box;
}
.form-input::placeholder { color: rgba(255,255,255,0.2); }
.form-input:focus {
  border-color: rgba(249,158,26,0.6);
  background: rgba(249,158,26,0.04);
}

.form-select {
  width: 100%;
  padding: 9px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.2);
  background: #1e2538;
  color: #fff;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  appearance: auto;
  transition: border-color 0.15s;
  box-sizing: border-box;
}
.form-select:focus { border-color: rgba(249,158,26,0.6); }
.form-select option { background: #1e2538; color: #fff; }

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 14px 24px 18px;
  border-top: 1px solid rgba(255,255,255,0.07);
}

.btn-cancel {
  padding: 8px 20px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.12);
  background: transparent;
  color: rgba(255,255,255,0.5);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-cancel:hover { border-color: rgba(255,255,255,0.3); color: #fff; }

.btn-save {
  padding: 8px 24px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #f99e1a, #e07b00);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s;
}
.btn-save:hover { opacity: 0.85; }

/* ── 모바일 ── */
@media (max-width: 768px) {
  .col-pos-group { min-width: 100px; }
  .col-name { width: 90px; }
}

@media (max-width: 560px) {
  .most-list { display: none; }
  .col-pos-group { min-width: 80px; }
}
</style>
