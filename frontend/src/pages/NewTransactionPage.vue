<template>
  <q-page class="column overflow-hidden">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div class="q-pa-sm">

      <q-form @submit="onSubmit" ref="formElement">
        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model.number="transactionStore.newTransacitonData.value" :label="t('transaction.amount')" />
          <q-select class="currency-select" popup-content-class="currency-select-popup" dense filled square outlined
            behavior="dialog" bg-color="secondary" label-color="dark" color="dark"
            v-model="transactionStore.newTransacitonData.currency" :options="currencyOptions" emit-value map-options
            :label="t('transaction.currency')" />
        </div>

        <div class="new-transaction__group">
          <q-field @focus="router.push({ name: 'select', params: { type: 'category' } })" dense filled square outlined
            bg-color="secondary" label-color="dark" color="dark" v-model="transactionStore.newTransacitonData.category"
            :label="t('transaction.category')">
            <template v-slot:control>
              <div class="self-center full-width no-outline tg-primary-text " tabindex="0">
                {{ (transactionStore.newTransacitonData.category as ICategory)?.name }}
              </div>
            </template>
            <template v-slot:append>
              <div class="text-body2 flex flex-center tg-primary-text">
                {{ t('common.all') }} <q-icon :name="ionChevronForward" class="cursor-pointer" />
              </div>
            </template>
          </q-field>
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model="transactionStore.newTransacitonData.source" :label="t('transaction.source')" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model="transactionStore.newTransacitonData.description" :label="t('transaction.comment')" />
        </div>
        <div class="new-transaction__group" @click="chosingDate = true">
          <q-field dense filled square borderless bg-color="secondary" label-color="dark" color="dark" :label="t('transaction.date')"
            v-model="transactionStore.newTransacitonData.date">
            <template v-slot:control>
              <div class="self-center full-width no-outline tg-primary-text" tabindex="0">{{ (new
                Date(transactionStore.newTransacitonData.date)).toLocaleDateString() }}
              </div>
            </template>
          </q-field>
        </div>
      </q-form>
    </div>
    <q-dialog v-model="chosingDate">
      <q-date class="tg-card" v-model="transactionStore.newTransacitonData.date" minimal />
    </q-dialog>
  </q-page>
</template>

<script setup lang='ts'>
import ModeToggle from 'src/components/ModeToggle.vue';
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useWebApp } from 'src/stores/webapp';
import { useRouter } from 'vue-router';
import { useTransaction } from 'src/stores/transactions';
import { ionChevronForward } from '@quasar/extras/ionicons-v7';
import { ICategory } from 'src/types';
import { useWallets } from 'src/stores/wallets';
import { logClientError } from 'src/api';
import { useI18n } from 'vue-i18n';

const transactionStore = useTransaction()
const walletStore = useWallets()
const router = useRouter()
const { t } = useI18n()
const formElement = ref()

const chosingDate = ref(false)

const currencyOptions = computed(() => walletStore.currencies.map((currency) => ({
  label: `${currency.code} — ${currency.name}`,
  value: currency.code,
})))

async function onSubmit() {
  webAppStore.disableMainButton()
  if (!transactionStore.newTransacitonData.category) {
    webAppStore.showAlert(t('transaction.categoryRequired'))
    webAppStore.enableMainButton()
    return
  }

  try {
    await transactionStore.newTransaciton()
    router.go(-1)
    webAppStore.disableCloseConfirm()
  } catch (error) {
    console.error(error)
    const axiosError = error as { response?: { data?: unknown; status?: number } }
    await logClientError('Could not save transaction', {
      page: 'NewTransactionPage',
      error: String(error),
      response: axiosError.response ? { status: axiosError.response.status, data: axiosError.response.data } : undefined,
      payload: transactionStore.newTransacitonData,
    })
    webAppStore.showAlert(t('transaction.saveError'))
  } finally {
    webAppStore.enableMainButton()
  }
}
const webAppStore = useWebApp()

onMounted(() => {
  walletStore.loadCurrencies()
  transactionStore.newTransacitonData.currency = walletStore.currentWallet?.default_currency || 'USD'
  webAppStore.showMainButton(t('common.save'), formElement.value.submit)
  webAppStore.enableCloseConfirm()
})

onBeforeUnmount(() => {
  webAppStore.disableCloseConfirm()
})

</script>

<style scoped lang='scss'>
@import '../css/mixins.scss';
.new-transaction {
  @include input-group;
}
</style>
