<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  authStore.fetchUser()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #0d0d1a;
  color: #e0e0e0;
  font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
