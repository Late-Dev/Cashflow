<template>
  <q-page class="column">
    settings
    {{ categoriesStore.categoriesList }}
  </q-page>
</template>

<script setup lang='ts'>
import { useCategories } from 'src/stores/category';

const categoriesStore = useCategories()
</script>

<style scoped lang='scss'></style>
