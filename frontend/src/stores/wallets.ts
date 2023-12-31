import { defineStore } from 'pinia';
import { addWallet, deleteWalletRequest, getWallets } from 'src/api';
import { Wallet } from 'src/types';
import { ref } from 'vue';
import { useTransaction } from './transactions';
import { useCategories } from './category';

export const useWallets = defineStore('wallets', () => {
  const walletList = ref<Wallet[]>();

  const currentWallet = ref<Wallet>();

  const loaded = ref(false);

  const transactionStore = useTransaction();
  const categoriesStore = useCategories();

  async function loadWallets() {
    await getWallets().then((response) => {
      walletList.value = response.data;
      currentWallet.value = response.data[0];
      loaded.value = true;
    });

    transactionStore.loadTransactions();
    categoriesStore.loadCategories();
  }

  async function chooseWallet(id: number) {
    if (!loaded.value) return;
    loaded.value = false;
    currentWallet.value = walletList.value?.find((el) => el.id === id);

    await transactionStore.loadTransactions();
    await categoriesStore.loadCategories();
    loaded.value = true;
  }

  async function createWallet( name?: string) {
    if ( !name) return;
    if (!loaded.value) return;
    loaded.value = false;
    await addWallet(name);
    await getWallets().then((response) => {
      walletList.value = response.data;
      currentWallet.value = response.data.at(-1);
    });

    await transactionStore.loadTransactions();
    await categoriesStore.loadCategories();
    loaded.value = true;
  }

  async function deleteWallet(id: number) {
    await deleteWalletRequest(id);
    await loadWallets()
  }

  return {
    loadWallets,
    walletList,
    currentWallet,
    loaded,
    chooseWallet,
    createWallet,
    deleteWallet,
  };
});
