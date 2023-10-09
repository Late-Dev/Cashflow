import { defineStore } from 'pinia';
import { addTransaction, getTransactions } from 'src/api';
import { computed, ref } from 'vue';
import { useWallets } from './wallets';
import { ITransaction } from 'src/types';

export const useTransaction = defineStore('transaction', () => {
  const currentMode = ref<'outcome' | 'income'>('outcome');
  const walletsStore = useWallets();

  const incomeTransactionsList = ref<ITransaction[]>();
  const outcomeTransactionsList = ref<ITransaction[]>();

  const newTransacitonData = ref<Omit<ITransaction, 'id' | 'user' | 'type'>>({
    value: 0,
    description: '',
    category: undefined,
    source: '',
    date: new Date().toUTCString(),
  });

  async function loadTransactions() {
    if (!walletsStore.currentWallet?.id) return;
    await getTransactions(walletsStore.currentWallet.id).then((response) => {
      incomeTransactionsList.value = response.data.income;
      outcomeTransactionsList.value = response.data.outcome;
    });
  }

  async function newTransaciton() {

    await addTransaction({
      ...newTransacitonData.value,
      type: currentMode.value ,
      wallet: walletsStore.currentWallet?.id,
    });
    await loadTransactions();
  }

  const transactionsList = computed(() => {
    if (currentMode.value === 'outcome') {
      return outcomeTransactionsList.value;
    }
    return incomeTransactionsList.value;
  });

  return {
    currentMode,
    loadTransactions,
    transactionsList,
    newTransaciton,
    newTransacitonData,
  };
});
