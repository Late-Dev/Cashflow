import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUser = defineStore('user', () => {
  const id = ref(0);

  return {
    id,
  };
});
