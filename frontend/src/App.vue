<template>
  -{{walletsStore.walletList }}-
  <router-view />
</template>

<script setup lang="ts">
import { useWebApp } from 'src/stores/webapp'
import { onMounted, ref } from 'vue';
import { useWallets } from 'src/stores/wallets'
const walletsStore = useWallets()

const webAppStore = useWebApp()
const data = ref()
onMounted(async () => {
  data.value = await webAppStore.auth()
})

</script>
