import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios.js'

export const useStreamersStore = defineStore('streamers', () => {
  const streamers = ref([])
  const loading   = ref(false)

  const fetchStreamers = async () => {
    loading.value = true
    try {
      const res = await api.get('/overwatch/streamers/')
      streamers.value = res.data
    } finally {
      loading.value = false
    }
  }

  const addStreamer = async (data) => {
    const res = await api.post('/overwatch/streamers/', data)
    streamers.value.push(res.data)
  }

  const updateStreamer = async (id, data) => {
    const res = await api.put(`/overwatch/streamers/${id}/`, data)
    const idx = streamers.value.findIndex(s => s.id === id)
    if (idx !== -1) streamers.value[idx] = res.data
  }

  const deleteStreamer = async (id) => {
    await api.delete(`/overwatch/streamers/${id}/`)
    streamers.value = streamers.value.filter(s => s.id !== id)
  }

  return { streamers, loading, fetchStreamers, addStreamer, updateStreamer, deleteStreamer }
})
