import { defineStore } from 'pinia';
import { getWallets } from 'src/api';
import { Wallet } from 'src/types';
import { ref } from 'vue';
import { useTransaction } from './transactions';

export const useWallets = defineStore('wallets', () => {
  const walletList = ref<Wallet[]>();

  const currentWallet = ref<Wallet>();

  const transactionStore = useTransaction();

  async function loadWallets() {
    await getWallets().then((response) => {
      walletList.value = response.data;
      currentWallet.value = response.data[0];
    });

    transactionStore.loadTransactions();
  }

  return {
    loadWallets,
    walletList,
    currentWallet,
  };
});
