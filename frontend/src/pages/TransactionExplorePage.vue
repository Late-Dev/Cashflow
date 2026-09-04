<template>
  <q-page class="column q-pa-md overflow-hidden">
    <div class="column flex-center">
      <q-avatar size="60px" :style="{ background: `hsl(${category?.color}, 64%, 61%)` }"> {{ category?.icon }} </q-avatar>
      <div class="transaction__category q-mt-sm">

        {{ category?.name }}
      </div>
    </div>
    <div class="row transaction__title">
      {{ t('transaction.amount') }}
    </div>
    <div class="row transaction__value">
      {{ category?.transaction_type === 'outcome' ? '-' : '+' }}{{ transationInfo?.value }} {{ transationInfo?.currency }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.display_currency && transationInfo?.display_currency !== transationInfo?.currency">
      {{ t('transaction.inWalletCurrency') }}
    </div>
    <div class="row transaction__value" v-if="transationInfo?.display_currency && transationInfo?.display_currency !== transationInfo?.currency">
      {{ category?.transaction_type === 'outcome' ? '-' : '+' }}{{ Number(transationInfo?.display_value || 0).toFixed(2) }} {{ transationInfo?.display_currency }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.usd_to_currency_rate">
      {{ t('transaction.usdRateAtPurchase') }}
    </div>
    <div class="row transaction__value" v-if="transationInfo?.usd_to_currency_rate">
      1 USD = {{ transationInfo?.usd_to_currency_rate }} {{ transationInfo?.currency }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.source">
      {{ t('transaction.source') }}
    </div>
    <div class="row transaction__value" v-if="transationInfo?.source">
      {{ transationInfo?.source }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.description">
      {{ t('transaction.comment') }}
    </div>
    <div class="row transaction__value" v-if="transationInfo?.description">
      {{ transationInfo?.description }}
    </div>
    <div class="row transaction__title">
      {{ t('transaction.date') }}
    </div>
    <div class="row transaction__value">
      {{ (new Date(transationInfo?.date as string)).toLocaleDateString() }}
    </div>
    <!-- <div class="row transaction__title">
      Name
    </div>
    <div class="row transaction__value">
      {{ (new Date(transationInfo?.date as string)).toLocaleDateString() }}
    </div> -->
  </q-page>
</template>

<script setup lang='ts'>
import { useRoute } from 'vue-router';
import { useTransaction } from 'src/stores/transactions';
import { computed } from 'vue';
import { useCategories } from 'src/stores/category';
import { useI18n } from 'vue-i18n';

const categorieStore = useCategories()
const { t } = useI18n()

const transactionStore = useTransaction()
const route = useRoute()

const transationInfo = computed(() => {
  return transactionStore.transactionsList?.find((item) => item.id == parseInt(route.params.id as string))
})


const category = computed(() => {
  return categorieStore.categoriesList?.find((el) => el.id === transationInfo.value?.category as number)
})

</script>

<style scoped lang='scss'>
.transaction {
  &__title {
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    color: $theme-hint;
  }

  &__category {
    font-size: 21px;
    font-style: normal;
    font-weight: 500;
  }

  &__value {
    font-size: 17px;
    font-style: normal;
    font-weight: 400;
  }
}
</style>
