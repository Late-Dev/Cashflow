<template>
  <q-page class="column overflow-hidden">
    <div class="row q-ma-sm title">
      {{ t('wallet.allWallets') }}
    </div>
    <div class="q-ma-sm">
      <q-select class="currency-select" popup-content-class="currency-select-popup" dense filled square outlined
        behavior="dialog" bg-color="secondary" label-color="dark" color="dark"
        v-model="language" :options="languageOptions" emit-value map-options :label="t('language.label')" />
    </div>
    <div style="padding-bottom: 60px;">

      <list-item color="secondary" show-actions @delete="deleteWallet" @open="openWallet" @edit="editWallet" :item="wallet"
        v-for="wallet in walletStore.walletList" :key="wallet.id">
        <template #icon>
          <q-icon :name="ionWalletOutline"></q-icon>
        </template>

        <template #name>{{ wallet.name }}</template>
      </list-item>


    </div>

  </q-page>
</template>

<script setup lang='ts'>
import { useWallets } from 'src/stores/wallets';
import { ionWalletOutline } from '@quasar/extras/ionicons-v7';
import ListItem from 'src/components/ListItem.vue';
import { useRouter } from 'vue-router';
import { useWebApp } from 'src/stores/webapp';
import { computed, onMounted } from 'vue';
import { Wallet } from 'src/types';
import { useI18n } from 'vue-i18n';
import { MessageLanguages } from 'src/boot/i18n';

const webAppStore = useWebApp()
const walletStore = useWallets()
const router = useRouter()
const { t } = useI18n()

const languageOptions = computed(() => [
  { label: t('language.en'), value: 'en-US' },
  { label: t('language.ru'), value: 'ru' },
  { label: t('language.zh'), value: 'zh-CN' },
])

const language = computed({
  get: () => webAppStore.language,
  set: (value: MessageLanguages) => webAppStore.setLanguage(value),
})

function openWallet(id: number) {
  walletStore.chooseWallet(id)
  router.push({ name: 'index' })
}

onMounted(() => {
  webAppStore.showMainButton(t('common.add'), () => { router.push({ name: 'addWallet' }) })
})


function deleteWallet(id: number) {
  webAppStore.confirm(async () => {
    await walletStore.deleteWallet(id)
  })
}

function editWallet(wallet: Wallet) {
  router.push({ name: 'editWallet', params: { id: wallet.id } })
}

</script>

<style scoped lang='scss'></style>
