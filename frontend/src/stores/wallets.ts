import { defineStore } from 'pinia';
import { addWallet, deleteWalletRequest, editWalletRequest, getCurrencies, getWallets, setDefaultWalletRequest } from 'src/api';
import { Currency, Wallet } from 'src/types';
import { ref } from 'vue';
import { useTransaction } from './transactions';
import { useCategories } from './category';

export const useWallets = defineStore('wallets', () => {
  const walletList = ref<Wallet[]>();

  const currentWallet = ref<Wallet>();

  const loaded = ref(false);
  const currencies = ref<Currency[]>([]);

  const transactionStore = useTransaction();
  const categoriesStore = useCategories();

  async function loadWallets() {
    if (!currencies.value.length) {
      await loadCurrencies();
    }
    await getWallets().then((response) => {
      walletList.value = response.data;
      currentWallet.value = response.data.find((wallet: Wallet) => wallet.is_default) || response.data[0];
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
    await addWallet(name, 'USD');
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

  async function updateWallet(id: number, name?: string, defaultCurrency?: string) {
    await editWalletRequest(id, name, defaultCurrency);
    await loadWallets();
  }

  async function renameWallet(id: number, name?: string) {
    if (!name) return;
    await updateWallet(id, name);
  }

  async function loadCurrencies() {
    await getCurrencies().then((response) => {
      currencies.value = response.data;
    });
  }

  async function setDefaultWallet(id: number) {
    await setDefaultWalletRequest(id);
    await loadWallets();
  }

  return {
    loadWallets,
    walletList,
    currentWallet,
    loaded,
    currencies,
    chooseWallet,
    createWallet,
    deleteWallet,
    renameWallet,
    updateWallet,
    setDefaultWallet,
    loadCurrencies,
  };
});
