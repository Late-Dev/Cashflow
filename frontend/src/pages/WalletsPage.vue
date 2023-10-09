<template>
  <q-page class="column">
    <div class="row q-ml-sm settings__title">
      All wallets
    </div>
    <div>

      <list-item color="secondary" @open="openWallet" :item="wallet" v-for="wallet in walletStore.walletList"
        :key="wallet.id">
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

const walletStore = useWallets()
const router = useRouter()

function openWallet(id: number) {
  walletStore.chooseWallet(id)
  router.push({ name: 'index' })
}

</script>

<style scoped lang='scss'>
.settings {
  &__title {
    font-size: 17px;
    font-style: normal;
    font-weight: 600;
  }
}
</style>
