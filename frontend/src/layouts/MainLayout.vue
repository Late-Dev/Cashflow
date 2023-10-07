<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="tg-primary" v-if="false">
      <q-toolbar>
        <div>
          Cancel
        </div>

        <q-toolbar-title class="text-center">
          Vova's wallet
        </q-toolbar-title>

        <q-btn flat dense round icon="menu" aria-label="Menu" />
      </q-toolbar>
    </q-header>



    <q-page-container class="tg-primary">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">


</script>
