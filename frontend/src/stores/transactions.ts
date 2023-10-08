import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTransaction = defineStore('transaction', () => {
  const currentMode = ref<'expenses' | 'income'>('expenses');

  return {
    currentMode,
  };
});
