import { defineStore } from 'pinia';
import { ICategory } from 'src/types';
import { computed, ref } from 'vue';
import { useWallets } from './wallets';
import { useTransaction } from './transactions';

import { deleteCategoryRequest, getCategories } from 'src/api';

export const useCategories = defineStore('category', () => {
  const allCategoriesList = ref<ICategory[]>();
  const walletsStore = useWallets();
  const transactionStore = useTransaction();

  const loaded = ref(false);

  async function loadCategories() {
    if (!walletsStore.currentWallet?.id) return;
    loaded.value = false;
    allCategoriesList.value = undefined;

    await getCategories(walletsStore.currentWallet.id).then((response) => {
      allCategoriesList.value = response.data;
      loaded.value = true;
    });
  }

  const categoriesList = computed(() => {
    return allCategoriesList.value?.filter(
      (el) => el.transaction_type === transactionStore.currentMode
    );
  });

  async function deleteCategory(id: number) {
    await deleteCategoryRequest(id);
    await loadCategories();
  }

  return {
    categoriesList,
    loadCategories,
    loaded,
    allCategoriesList,
    deleteCategory,
  };
});
