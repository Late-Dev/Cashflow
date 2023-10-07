<template>
  --{{ webAppStore.webapp.initData }}--
  <router-view />
</template>

<script setup lang="ts">
import { useWebApp } from 'src/stores/webapp'

const webAppStore = useWebApp()

</script>
