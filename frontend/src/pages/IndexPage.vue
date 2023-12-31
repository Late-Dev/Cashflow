<template>
  <q-page class="column overflow-hidden">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div class="row justify-between q-ma-sm">
      <div class="column">
        <div class="row text-bold total" v-if="transactionStore.loaded">
          {{ transactionStore.monthTransactionsList?.length ? monthSum + ' $' : 'no data' }}
        </div>
        <q-skeleton v-else type="rect" width="100px" />
        <div class="row hint month" v-if="transactionStore.loaded">
          <div v-if="transactionStore.selectedMonth !== undefined">
            {{ transactionStore.currentMode === 'outcome' ? 'Spent' : 'Earned'
            }} in {{ getMonthName(transactionStore.selectedMonth) }}
          </div>
        </div>
        <q-skeleton v-else type="text" width="80px" />
      </div>
      <div class="column">
        <q-checkbox class="checkbox" color="dark" v-model="barchart" :checked-icon="ionPieChartOutline"
          :unchecked-icon="ionPodiumOutline" />
      </div>
    </div>
    <div v-if="!barchart" class="row justify-between items-center" v-touch-swipe.mouse.horizontal="handleSwipe">
      <q-icon size="sm" @click="transactionStore.selectMonth(transactionStore.selectedMonth - 1)"
        class="q-pl-md cursor-pointer" :name="ionChevronBack" />
      <div v-if="transactionStore.loaded && categorieStore.loaded">

        <CategoryChart :chart-data="categoriesChartData" v-if="transactionStore.selectedMonth" :colors="colorsChartData"
          :month="getMonthName(transactionStore.selectedMonth)">
        </CategoryChart>
        <h5 style="width: 180px; text-align: center;" v-else>
          Add your first transaction
        </h5>
      </div>
      <q-skeleton v-else type="circle" width="180px" height="180px" />
      <q-icon @click="transactionStore.selectMonth(transactionStore.selectedMonth + 1)" size="sm"
        class="q-pr-md cursor-pointer" :name="ionChevronForward" />
    </div>
    <div v-else>
      <MonthBarChart :chart-data="monthChartData" @choose-month="chooseMonth" v-if="transactionStore.loaded" />

      <q-scroll-area v-else style="height: 180px; max-width: 100vw;">
        <div class="row no-wrap items-end" style="height: 180px; padding: 10px 20px;">
          <q-skeleton type="rect" style="margin: 0 10px;" width="60px" :height="`${(n * n * 15 % (123 - n)) % 100}%`"
            v-for="n in 12" :key="n" />
        </div>
      </q-scroll-area>
    </div>
    <div class="row justify-center  q-mt-md">
      <q-btn :disable="!transactionStore.loaded" @click="router.push({ name: 'new' })" :icon="ionAdd" :align="`center`"
        no-caps unelevated class="link-button button__new">New {{ transactionStore.currentMode === 'outcome' ? 'expense' :
          'income'
        }}</q-btn>
    </div>
    <div class="column q-mt-md" v-if="transactionStore.loaded">
      <div class="transactions__item q-mt-md" v-for="(transaction, index) in transactionStore.monthTransactionsList"
        :key="transaction.id">
        <div v-if="isFirstToday(index)" class="row transactions__date">{{ (new
          Date(transaction.date)).toLocaleDateString('en-US', { month: 'long', day: 'numeric' }) }}</div>
        <TransactionBar :transaction="transaction" @delete="deleteTransaction" @edit="editTransaction"
          @open="router.push({ name: 'explore', params: { id: $event } })" />
      </div>
    </div>
    <div v-else>
      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>

        <q-item-section>
          <q-item-label>
            <q-skeleton type="text" />
          </q-item-label>
          <q-item-label caption>
            <q-skeleton type="text" width="65%" />
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>

        <q-item-section>
          <q-item-label>
            <q-skeleton type="text" />
          </q-item-label>
          <q-item-label caption>
            <q-skeleton type="text" width="90%" />
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>

        <q-item-section>
          <q-item-label>
            <q-skeleton type="text" width="35%" />
          </q-item-label>
          <q-item-label caption>
            <q-skeleton type="text" />
          </q-item-label>
        </q-item-section>
      </q-item>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import CategoryChart from 'components/CategoryChart.vue';
import { computed, ref } from 'vue';
import { ionPodiumOutline, ionPieChartOutline, ionAdd, ionChevronBack, ionChevronForward } from '@quasar/extras/ionicons-v7'
import { useRouter } from 'vue-router';
import ModeToggle from 'src/components/ModeToggle.vue';
import TransactionBar from 'src/components/TransactionBar.vue';
import { useTransaction } from 'src/stores/transactions';
import { useCategories } from 'src/stores/category';
import MonthBarChart from 'src/components/MonthBarChart.vue';
import { useWebApp } from 'src/stores/webapp';
import { ITransaction } from 'src/types';

const webAppStore = useWebApp()
const transactionStore = useTransaction()
const router = useRouter()

const barchart = ref(false)

function getMonthName(monthNumber: number) {
  const date = new Date();
  date.setMonth(monthNumber);

  return date.toLocaleString('en-US', { month: 'long' });
}

const monthSum = computed(() => {
  return transactionStore.monthTransactionsList?.reduce((accumulator, val) => accumulator + val.value, 0)
})

const aggregatedTransactions = computed(() => {
  return transactionStore.monthTransactionsList?.reduce((accumulator, val) => {

    const category = accumulator.find(el => el.category === val.category)
    if (accumulator.length && category) {
      category.value += val.value
    } else if (val.category) {
      accumulator.push({ category: val.category as number, value: val.value })

    }
    return accumulator
  }, [{ category: 0, value: 0 }])
})

const categoriesChartData = computed(() => {
  return aggregatedTransactions.value?.map(el => el.value) || [0]
})

const categorieStore = useCategories()

const colorsChartData = computed(() => {
  return aggregatedTransactions.value?.map(el => categorieStore.categoriesList?.find((element) => el.category === element.id)?.color) || [0]
})

const monthChartData = computed(() => {
  const monthArray = new Array(12).fill(0);
  transactionStore.transactionsList?.forEach((element) => {
    const index = new Date(element.date).getMonth()
    monthArray[index] += element.value
  })
  return monthArray
})


function handleSwipe({ ...newInfo }) {
  if (newInfo.direction === 'left') {

    console.log('change up')
    transactionStore.selectMonth(transactionStore.selectedMonth + 1)
  }
  if (newInfo.direction === 'right') {
    transactionStore.selectMonth(transactionStore.selectedMonth - 1)
    console.log('change down')
  }
}

function isFirstToday(index: number) {
  if (index === 0) {
    return true
  }

  if (transactionStore.transactionsList && transactionStore.transactionsList[index] && transactionStore.transactionsList[index - 1]) {
    const prevDate = new Date(transactionStore.transactionsList[index - 1].date)
    const currentDate = new Date(transactionStore.transactionsList[index].date)
    if (prevDate.getDate() !== currentDate.getDate()) {
      return true
    }
  }
  return false
}

function chooseMonth(event: number) {
  barchart.value = false
  transactionStore.selectMonth(event)
}

function deleteTransaction(id: number) {
  webAppStore.confirm(() => {
    transactionStore.delTransaction(id)
  })
}

function editTransaction(transaction: ITransaction) {
  transactionStore.editTransactionData = { ...transaction , category: categorieStore.categoriesList?.find((element) => element.id === transaction.category) };
  router.push({ name: 'editTransaction' })
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
