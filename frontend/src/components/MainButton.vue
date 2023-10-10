<template>
  <q-btn flat square :disable="disable" class="main-button">{{ text }}</q-btn>
</template>

<script setup lang='ts'>

defineProps(['text', 'disable'])

</script>

<style scoped lang='scss'>
.main-button{
  position: fixed;
  width: 100vw;
  top: calc(100vh - 50px);
  background: $theme-button-bg;
  color: $theme-button-text;
  height: 50px;
}

</style>
