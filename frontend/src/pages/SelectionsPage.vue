<template>
  <q-page class="column">
    select
    {{ route.params.type }}
  </q-page>
</template>

<script setup lang='ts'>
import { useRoute } from 'vue-router';

const route = useRoute()
</script>

<style scoped lang='scss'></style>
