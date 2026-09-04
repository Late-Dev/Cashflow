<template>
  <q-btn-toggle :disable="disabled" spread no-caps rounded class="toggle" v-model="useTransactionStore.currentMode"
    unelevated toggle-text-color="dark" text-color="dark" toggle-color="primary" :options="modeOptions"></q-btn-toggle>
</template>

<script setup lang='ts'>
import { useTransaction } from 'src/stores/transactions';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const useTransactionStore = useTransaction()
const { t } = useI18n()
const modeOptions = computed(() => [
  { label: t('mode.expenses'), value: 'outcome' },
  { label: t('mode.income'), value: 'income' },
])

defineProps(['disabled'])

</script>

<style scoped lang='scss'>
.toggle {
  padding: 3px;
  background-color: $theme-secondary-bg;

  border-radius: 7px;

  height: 32px;

  :deep(button) {
    padding: 5px;
    line-height: 1em;

    min-height: auto;
    font-weight: 400;
    border-radius: 7px;
  }

  :deep(.bg-primary) {
    border-radius: 7px !important;
    box-shadow: 0px 3px 1px 0px rgba(0, 0, 0, 0.04), 0px 3px 8px 0px rgba(0, 0, 0, 0.12);
    font-weight: 500;
  }
}
</style>
