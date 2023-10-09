import { defineStore } from 'pinia';
import { ICategory } from 'src/types';
import { computed, ref } from 'vue';
import { useWallets } from './wallets';
import { useTransaction } from './transactions';

import { getCategories } from 'src/api';

export const useCategories = defineStore('category', () => {
  const allCategoriesList = ref<ICategory[]>();
  const walletsStore = useWallets();
  const transactionStore = useTransaction();

  async function loadCategories() {
    if (!walletsStore.currentWallet?.id) return;
    await getCategories(walletsStore.currentWallet.id).then((response) => {
      allCategoriesList.value = response.data;
    });
  }

  const categoriesList = computed(() => {
    return allCategoriesList.value?.filter(
      (el) => el.transaction_type === transactionStore.currentMode
    );
  });

  return {
    categoriesList,
    loadCategories,
  };
});