<template>
  <router-view />
  <MainButton :disable="webAppStore.mainButton.disabled" v-if="webAppStore.mainButton.isVisible" @click="webAppStore.mainButton.onClick" :text="webAppStore.mainButton.text" />
</template>

<script setup lang="ts">
import { useWebApp } from 'src/stores/webapp'
import { onMounted, ref } from 'vue';
import MainButton from './components/MainButton.vue';

const webAppStore = useWebApp()
const data = ref()
onMounted(async () => {
  data.value = await webAppStore.auth()
})

</script>
