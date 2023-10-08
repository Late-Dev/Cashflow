<template>
  -{{ data }}-
  <router-view />
</template>

<script setup lang="ts">
import { useWebApp } from 'src/stores/webapp'
import { onMounted, ref } from 'vue';

const webAppStore = useWebApp()
const data = ref()
onMounted(async () => {
  data.value = await webAppStore.auth()
})

</script>
