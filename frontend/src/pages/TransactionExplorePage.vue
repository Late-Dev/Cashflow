<template>
  <q-page class="column q-pa-md overflow-hidden">
    <div class="column flex-center">
      <q-avatar size="60px" :style="{ background: `hsl(${category?.color}, 64%, 61%)` }"> {{ category?.icon }} </q-avatar>
      <div class="transaction__category q-mt-sm">

        {{ category?.name }}
      </div>
    </div>
    <div class="row transaction__title">
      The amount
    </div>
    <div class="row transaction__value">
      {{ category?.transaction_type === 'outcome' ? '-' : '+' }}{{ transationInfo?.value }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.source">
      Source
    </div>
    <div class="row transaction__value" v-if="transationInfo?.source">
      {{ transationInfo?.source }}
    </div>
    <div class="row transaction__title" v-if="transationInfo?.description">
      Comment
    </div>
    <div class="row transaction__value" v-if="transationInfo?.description">
      {{ transationInfo?.description }}
    </div>
    <div class="row transaction__title">
      Date
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

const categorieStore = useCategories()

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
