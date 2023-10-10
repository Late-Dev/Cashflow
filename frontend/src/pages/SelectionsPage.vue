<template>
  <q-page class="column">
    <q-list bordered separator>
      <q-item @click="selectItem(category)" clickable v-ripple v-for="category in categoriesStore.categoriesList"
        :key="category.id">
        <q-item-section avatar>
          <q-avatar :style="{ background: `hsl(${category.color}, 64%, 61%)` }"> {{ category.icon }} </q-avatar>
        </q-item-section>
        <q-item-section class="category__text">{{ category.name }}</q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script setup lang='ts'>
import { useRoute, useRouter } from 'vue-router';
import { useCategories } from 'src/stores/category';
import { useTransaction } from 'src/stores/transactions';

const transactionStore = useTransaction()
const categoriesStore = useCategories()
const route = useRoute()
const router = useRouter()

function selectItem(item: any) {
  if (route.query.mode === 'edit') {
    transactionStore.editTransactionData.category = item
  }
  else {

    transactionStore.newTransacitonData.category = item;
  }
  router.go(-1);
}

</script>

<style scoped lang='scss'>
.category__text {
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
}
</style>
