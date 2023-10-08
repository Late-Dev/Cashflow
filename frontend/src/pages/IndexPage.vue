<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <q-btn-toggle spread no-caps rounded class="toggle" v-model="mode" unelevated toggle-text-color="black"
        text-color="black" toggle-color="primary" :options="[
          { label: 'Expenses', value: 'expenses' },
          { label: 'Income', value: 'income' },

        ]"></q-btn-toggle>
    </div>
    <div class="row justify-between q-ma-sm">
      <div class="column">
        <div class="row text-bold total">
          20 000 $
        </div>
        <div class="row hint month">
          Spent in August
        </div>
      </div>
      <div class="column">
        <q-checkbox class="checkbox" color="accent" v-model="barchart" :checked-icon="ionPieChartOutline"
          :unchecked-icon="ionPodiumOutline" indeterminate-icon="help" />
      </div>
    </div>
    <div class="row justify-center">
      <CategoryChart></CategoryChart>
    </div>
    <div class="row justify-center q-mt-md">
      <q-btn @click="router.push({ name: 'new' })" :icon="ionAdd" :align="`center`" no-caps unelevated
        class="link-button button__new">New expense</q-btn>
    </div>
    <div class="column">
      <div>
        <div class="row">August 20 </div>
        <div class="row">Clothing and shoes</div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import CategoryChart from 'components/CategoryChart.vue';
import { ref } from 'vue';
import { ionPodiumOutline, ionPieChartOutline, ionAdd } from '@quasar/extras/ionicons-v7'
import { useRouter } from 'vue-router';

const router = useRouter()
const mode = ref<'expenses' | 'income'>('expenses')

const barchart = ref(false)
</script>

<style lang="scss" scoped>
.toggle {
  padding: 3px;
  background-color: $theme-secondary-bg;

  border-radius: 7px;

  height: 32px;

  :deep(button) {
    padding: 5px;
    line-height: 1em;

    min-height: auto;
    font-weight: 400;
    border-radius: 7px;
  }

  :deep(.bg-primary) {
    border-radius: 7px !important;
    box-shadow: 0px 3px 1px 0px rgba(0, 0, 0, 0.04), 0px 3px 8px 0px rgba(0, 0, 0, 0.12);
    font-weight: 500;
  }
}

.checkbox {
  background: #F4F4F5;
  border-radius: 6px;

  :deep(.q-checkbox__inner) {


    &::before {
      border-radius: 6px !important;

    }
  }

}

.button__new {
  line-height: 2em;
  font-size: 13px;
  border-radius: 12px;

  padding: 10px 24px;
  width: 212px;

}

.total {
  font-size: 17px;
}

.month {
  font-size: 14px;
}
</style>
