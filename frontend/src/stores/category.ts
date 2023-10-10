import { defineStore } from 'pinia';
import { ICategory } from 'src/types';
import { computed, ref } from 'vue';
import { useWallets } from './wallets';
import { useTransaction } from './transactions';

import { deleteCategoryRequest, getCategories, addCategory, editCategoryRequest } from 'src/api';

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

  async function createCategory(category: ICategory) {
    if (!walletsStore.currentWallet?.id) return;
    await addCategory(
      category.name,
      walletsStore.currentWallet.id,
      category.transaction_type,
      category.icon,
      category.color
    );
    await loadCategories();
  }

  async function editCategory(category: ICategory) {
    await editCategoryRequest(category.id, category.name, category.icon, category.color);
    await loadCategories();
  }

  return {
    categoriesList,
    loadCategories,
    loaded,
    allCategoriesList,
    deleteCategory,
    createCategory,
    editCategory,
  };
});
