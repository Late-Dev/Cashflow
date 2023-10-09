import { defineStore } from 'pinia';
import { ICategory } from 'src/types';
import { ref } from 'vue';
import { useWallets } from './wallets';
import { getCategories } from 'src/api';

export const useCategories = defineStore('category', () => {
  const categoriesList = ref<ICategory>();
  const walletsStore = useWallets();

  async function loadCategories() {
    if (!walletsStore.currentWallet?.id) return;
    await getCategories(walletsStore.currentWallet.id).then((response) => {
      categoriesList.value = response.data;
    });
  }

  return {
    categoriesList,
    loadCategories,
  };
});
