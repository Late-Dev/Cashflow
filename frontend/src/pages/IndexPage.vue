<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <ModeToggle />
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
      <div class="transactions__list">
        <div class="row">August 20 </div>
        <TransactionBar />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import CategoryChart from 'components/CategoryChart.vue';
import { ref } from 'vue';
import { ionPodiumOutline, ionPieChartOutline, ionAdd } from '@quasar/extras/ionicons-v7'
import { useRouter } from 'vue-router';
import ModeToggle from 'src/components/ModeToggle.vue';
import TransactionBar from 'src/components/TransactionBar.vue';
import { useWebApp } from 'src/stores/webapp'

const router = useRouter()
const webAppStore = useWebApp()

const barchart = ref(false)
</script>

<style lang="scss" scoped>
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

.transactions__list {
  overflow: hidden;
}
</style>
