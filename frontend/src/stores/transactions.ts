import { defineStore } from 'pinia';
import { addTransaction, getTransactions } from 'src/api';
import { computed, ref } from 'vue';
import { useWallets } from './wallets';
import { ITransaction } from 'src/types';

export const useTransaction = defineStore('transaction', () => {
  const currentMode = ref<'expenses' | 'income'>('expenses');
  const walletsStore = useWallets();

  const incomeTransactionsList = ref<ITransaction>();
  const outcomeTransactionsList = ref<ITransaction>();

  async function loadTransactions() {
    if (!walletsStore.currentWallet?.id) return;
    await getTransactions(walletsStore.currentWallet.id).then((response) => {
      incomeTransactionsList.value = response.data.income;
      outcomeTransactionsList.value = response.data.outcome;
    });
  }

  async function newTransaciton(
    payload: Omit<ITransaction, 'id' | 'user' | 'type'>
  ) {
    await addTransaction({
      ...payload,
      type: currentMode.value === 'expenses' ? 'outcome' : 'income',
    });
    await loadTransactions();
  }

  const transactionsList = computed(() => {
    if (currentMode.value === 'expenses') {
      return outcomeTransactionsList.value;
    }
    return incomeTransactionsList.value;
  });

  return {
    currentMode,
    loadTransactions,
    transactionsList,
    newTransaciton,
  };
});
