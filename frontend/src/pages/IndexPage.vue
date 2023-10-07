<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <q-btn-toggle spread no-caps rounded class="toggle" v-model="mode" unelevated toggle-text-color="black" text-color="black"
        toggle-color="primary" :options="[
          { label: 'Expenses', value: 'expenses' },
          { label: 'Income', value: 'income' },

        ]"></q-btn-toggle>
    </div>
    <div class="row justify-center">
      <CategoryChart></CategoryChart>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import CategoryChart from 'components/CategoryChart.vue';
import { ref } from 'vue';

const mode = ref<'expenses' | 'income'>('expenses')

</script>

<style lang="scss">
.toggle {
  padding: 3px;
  background-color: $theme-secondary-bg;

  border-radius: 7px;

  height: 32px;

  button {
    padding: 5px;
    line-height: 1em;

    min-height: auto;
    font-weight: 400;
    border-radius: 7px;
  }

  .bg-primary{
    border-radius: 7px !important;
    box-shadow: 0px 3px 1px 0px rgba(0, 0, 0, 0.04), 0px 3px 8px 0px rgba(0, 0, 0, 0.12);
    font-weight: 500;
  }
}
</style>
