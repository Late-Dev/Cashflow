<template>
  <q-page class="column overflow-hidden">
    <div class="row q-ma-sm title">
      All wallets
    </div>
    <div>

      <list-item color="secondary" @delete="deleteWallet" @open="openWallet" @edit="editWallet" :item="wallet"
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
import {  onMounted } from 'vue';
import { Wallet } from 'src/types';

const webAppStore = useWebApp()
const walletStore = useWallets()
const router = useRouter()

function openWallet(id: number) {
  walletStore.chooseWallet(id)
  router.push({ name: 'index' })
}

onMounted(() => {
  webAppStore.showMainButton('Add', () => { router.push({ name: 'addWallet' }) })
})


function deleteWallet(id: number) {
  webAppStore.confirm(() => {
    walletStore.deleteWallet(id)
  })
}

function editWallet(wallet: Wallet) {
  router.push({ name: 'editWallet', params: { id: wallet.id } })
}

</script>

<style scoped lang='scss'></style>
