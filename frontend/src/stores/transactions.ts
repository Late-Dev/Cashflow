import { defineStore } from 'pinia';
import {
  addTransaction,
  deleteTransaction,
  editTransactionRequest,
  getTransactions,
} from 'src/api';
import { computed, ref, watch } from 'vue';
import { useWallets } from './wallets';
import { ITransaction } from 'src/types';

export const useTransaction = defineStore('transaction', () => {
  const currentMode = ref<'outcome' | 'income'>('outcome');
  const walletsStore = useWallets();

  const incomeTransactionsList = ref<ITransaction[]>();
  const outcomeTransactionsList = ref<ITransaction[]>();

  const loaded = ref(false);

  const newTransacitonData = ref<Omit<ITransaction, 'id' | 'user' | 'type'>>({
    value: 0,
    currency: 'USD',
    description: '',
    category: undefined,
    source: '',
    date: new Date().toUTCString(),
  });

  const editTransactionData = ref<Omit<ITransaction, 'user'>>({
    id: 0,
    type: 'income',
    value: 0,
    currency: 'USD',
    description: '',
    category: undefined,
    source: '',
    date: new Date().toUTCString(),
  });

  async function loadTransactions() {
    if (!walletsStore.currentWallet?.id) return;
    loaded.value = false;
    incomeTransactionsList.value = undefined;
    outcomeTransactionsList.value = undefined;
    await getTransactions(walletsStore.currentWallet.id).then((response) => {
      incomeTransactionsList.value = sortTransactions(response.data.income || []);
      outcomeTransactionsList.value = sortTransactions(response.data.outcome || []);

      loaded.value = true;

      selectedMonth.value = new Date(
        transactionsList.value?.[0]?.date || new Date()
      ).getMonth();
    });
  }

  function sortTransactions(transactions: ITransaction[]) {
    return [...transactions].sort((a, b) => {
      const dateDiff = new Date(b.date).getTime() - new Date(a.date).getTime();
      if (dateDiff !== 0) return dateDiff;
      return (b.id || 0) - (a.id || 0);
    });
  }

  async function newTransaciton() {
    await addTransaction({
      ...newTransacitonData.value,
      currency: newTransacitonData.value.currency || walletsStore.currentWallet?.default_currency || 'USD',
      type: currentMode.value,
      wallet: walletsStore.currentWallet?.id,
    }).then(() => {
      newTransacitonData.value = {
        value: 0,
        currency: walletsStore.currentWallet?.default_currency || 'USD',
        description: '',
        category: undefined,
        source: '',
        date: new Date().toUTCString(),
      };
    });
    await loadTransactions();
  }

  const transactionsList = computed(() => {
    if (currentMode.value === 'outcome') {
      return outcomeTransactionsList.value;
    }
    return incomeTransactionsList.value;
  });

  function selectMonth(num: number) {
    selectedMonth.value = num;
  }

  const selectedMonth = ref();
  const monthTransactionsList = computed(() => {
    return sortTransactions(transactionsList.value || []).filter(
      (el) => new Date(el.date).getMonth() === selectedMonth.value
    );
  });

  watch(currentMode, () => {
    newTransacitonData.value.category = undefined;
    newTransacitonData.value.currency = walletsStore.currentWallet?.default_currency || 'USD';
  });

  watch(() => walletsStore.currentWallet?.default_currency, (currency) => {
    newTransacitonData.value.currency = currency || 'USD';
  });

  async function delTransaction(id: number) {
    await deleteTransaction(id);
    await loadTransactions();
  }

  async function editTransaction() {
    await editTransactionRequest(editTransactionData.value);

    editTransactionData.value = {
      id: 0,
      type: 'income',
      value: 0,
      currency: walletsStore.currentWallet?.default_currency || 'USD',
      description: '',
      category: undefined,
      source: '',
      date: new Date().toUTCString(),
    };
    await loadTransactions();
  }

  return {
    currentMode,
    loadTransactions,
    transactionsList,
    newTransaciton,
    newTransacitonData,
    monthTransactionsList,
    selectedMonth,
    selectMonth,
    loaded,
    delTransaction,
    editTransactionData,
    editTransaction,
  };
});
