import { defineStore } from 'pinia';
import { getWallets } from 'src/api';
import { Wallet } from 'src/types';
import { ref } from 'vue';

export const useWallets = defineStore('wallets', () => {
  const walletList = ref<Wallet>();

  async function loadWallets() {
    await getWallets().then((response) => {
      walletList.value = response.data;
    });
  }

  return {
    loadWallets,
    walletList
  };
});
