<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="tg-primary">
      <q-toolbar>


        <q-toolbar-title>
          {{ walletsStore.currentWallet?.name }}
        </q-toolbar-title>

        <q-btn flat dense round :icon="ionChevronForward" aria-label="Menu" />
      </q-toolbar>
    </q-header>



    <q-page-container class="tg-primary">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useWallets } from 'src/stores/wallets'
import { ionChevronForward } from '@quasar/extras/ionicons-v7'
const walletsStore = useWallets()

</script>
