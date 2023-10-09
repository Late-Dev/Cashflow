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
        <q-checkbox class="checkbox" color="dark" v-model="barchart" :checked-icon="ionPieChartOutline"
          :unchecked-icon="ionPodiumOutline" />
      </div>
    </div>
    <div class="row justify-between items-center" v-touch-swipe.mouse.horizontal="handleSwipe">
      <q-icon size="sm" class="q-pa-md cursor-pointer" :name="ionChevronBack" />
      <CategoryChart></CategoryChart>
      <q-icon size="sm" class="q-pa-md cursor-pointer" :name="ionChevronForward" />
    </div>
    <div class="row justify-center  q-mt-md">
      <q-btn @click="router.push({ name: 'new' })" :icon="ionAdd" :align="`center`" no-caps unelevated
        class="link-button button__new">New {{ transactionStore.currentMode === 'expenses' ? 'expense' : 'income'
        }}</q-btn>
    </div>
    <div class="column q-mt-md">
      <div class="transactions__item">
        <div class="row transactions__date">August 20 </div>
        <TransactionBar @open="router.push({ name: 'explore', params: { id: 1 } })" />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import CategoryChart from 'components/CategoryChart.vue';
import { ref } from 'vue';
import { ionPodiumOutline, ionPieChartOutline, ionAdd, ionChevronBack, ionChevronForward } from '@quasar/extras/ionicons-v7'
import { useRouter } from 'vue-router';
import ModeToggle from 'src/components/ModeToggle.vue';
import TransactionBar from 'src/components/TransactionBar.vue';
import { useTransaction } from 'src/stores/transactions';

const transactionStore = useTransaction()
const router = useRouter()

const barchart = ref(false)


function handleSwipe({ ...newInfo }) {
  if (newInfo.direction === 'left') {

    console.log('change up')
  }
  if (newInfo.direction === 'right') {

    console.log('change down')
  }
}

</script>

<style lang="scss" scoped>
.checkbox {
  background: $theme-secondary-bg;
  border-radius: 6px;


  :deep(.q-checkbox__inner) {
    color: $theme-primary-text;

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

.transactions {
  &__item {
    overflow: hidden;
    // padding-left: 10px;
  }

  &__date {
    font-size: 17px;
    font-weight: 600;
    padding-left: 15px;
  }
}
</style>
