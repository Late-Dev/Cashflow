<template>
  <q-page class="column overflow-hidden ">
    <div class="row q-ma-sm title"> New wallet</div>
    <div class="add-wallet__group q-ma-sm">

      <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
        v-model.number="newWalletName" label="Name" />

    </div>
  </q-page>
</template>

<script setup lang='ts'>
import {  onMounted, ref } from 'vue';
import { useWallets } from 'src/stores/wallets';
import { useWebApp } from 'src/stores/webapp';
import { useRouter } from 'vue-router';
const router = useRouter()


const webAppStore = useWebApp()

const walletStore = useWallets()

const newWalletName = ref()


onMounted(() => {
  webAppStore.showMainButton('Add', async () => {
    webAppStore.disableMainButton()
    await walletStore.createWallet(newWalletName.value);
    router.push({ name: 'index' })
  })
})




</script>

<style scoped lang='scss'>
@import '../css/mixins.scss';

.add-wallet {
  @include input-group;
}
</style>
