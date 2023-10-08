<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div>

      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <q-input filled v-model="text" label="Filled" />
      </q-form>
    </div>
  </q-page>
</template>

<script setup lang='ts'>
import ModeToggle from 'src/components/ModeToggle.vue';


</script>

<style scoped lang='scss'></style>
