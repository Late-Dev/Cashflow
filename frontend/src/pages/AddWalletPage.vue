<template>
  <q-page class="column overflow-hidden">
    <div class="row q-ma-sm title"> New wallet</div>
    <div class="add-wallet__group">

      <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
        v-model.number="newWalletName" label="Name" />

    </div>
  </q-page>
</template>

<script setup lang='ts'>
import { onBeforeMount, onBeforeUnmount, onMounted, ref } from 'vue';
import { useWallets } from 'src/stores/wallets';
import { useWebApp } from 'src/stores/webapp';
import { useRouter } from 'vue-router';
const router = useRouter()


const webAppStore = useWebApp()

const walletStore = useWallets()

const newWalletName = ref()


onMounted(() => {
  webAppStore.showMainButton('Add', () => {
    walletStore.createWallet(newWalletName.value);
    router.push({ name: 'index' })
  })
})




</script>

<style scoped lang='scss'>
.add-wallet {
  &__group {
    margin-bottom: 14px;

    border-radius: 12px;
    overflow: hidden;

    :deep(input) {
      color: $theme-primary-text;
    }

    :deep(.q-field__label) {
      opacity: 0.7;
    }

    :deep(.q-field__control::after) {

      display: none;

    }

    :deep(.q-field__control::before) {
      border: none;
    }

  }
}
</style>
