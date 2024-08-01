<template>
  <q-page class="column overflow-hidden ">

    <div class="row q-ma-sm title">
      {{ currentWallet.name }}
    </div>

    <div class="row q-ma-sm title">
      Members
    </div>
    <div v-if="usersLoaded" class="column full-width">
      <q-list bordered separator>
        <q-item clickable v-ripple v-for="user in walletUsers" :key="user.id">
          <q-item-section avatar>
            <q-avatar color="teal" text-color="white" :icon="ionPersonOutline">
              <img :src="user.photo_url" v-if="user.photo_url">
            </q-avatar>
          </q-item-section>

          <q-item-section class="wallet-settings__username">@{{ user.username }}</q-item-section>
          <q-item-section side v-if="user.user_type === 'owner'">Admin</q-item-section>
          <q-item-section side class="text-negative" v-if="user.user_type !== 'owner'">Delete</q-item-section>
        </q-item>
      </q-list>
    </div>
    <div v-else>
      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>
        <q-item-section>
          <q-item-label>
            <q-skeleton type="rect" />
          </q-item-label>
        </q-item-section>
      </q-item>
    </div>

    <div v-if="invite_link" class="column full-width q-ma-sm q-pa-sm">
      <div class="invite__group row invite__row">
        <q-field full-width @focus="copy(invite_link)" class="col  invite__button overflow-hidden" dense filled square
          outlined bg-color="secondary" label-color="dark" color="dark" v-model="invite_link" label="Category">
          <template v-slot:control>
            <div class="self-center no-outline tg-primary-text invite__input" tabindex="0">
              {{ invite_link }}
            </div>
          </template>
          <template v-slot:append>
            <q-icon class="tg-primary-text" :name="ionLinkOutline"></q-icon>
          </template>
        </q-field>
        <q-btn class="tg-secondary invite__button q-ml-sm" @click="webAppStore.shareWallet(currentWallet.name)" square
          flat :icon="ionArrowRedoSharp"> </q-btn>
        <q-btn class="tg-secondary invite__button q-ml-sm" @click="QRDialog = true" square flat :icon="ionQrCodeSharp">
        </q-btn>
      </div>

      <q-dialog @show="openQRDialog" v-model="QRDialog">
        <q-card class="tg-secondary">
          <div  ref="QRElement" class="q-ma-lg"></div>
        </q-card>
      </q-dialog>
    </div>

    <div class="row q-ma-sm title">
      Categories
    </div>
    <div v-if="loaded" style="padding-bottom: 60px;">
      <p class="q-ma-sm">

        Income catagories:
      </p>
      <list-item :color="category.color" @delete="deleteCategory" @edit="editCategory" :item="category"
        v-for="category in incomeWalletCategories" :key="category.id">
        <template #icon>
          {{ category.icon }}
        </template>

        <template #name>{{ category.name }}</template>
      </list-item>
      <p class="q-ma-sm">

        Expenses:
      </p>
      <list-item :color="category.color" @delete="deleteCategory" @edit="editCategory" :item="category"
        v-for="category in outcomeWalletCategories" :key="category.id">
        <template #icon>
          {{ category.icon }}
        </template>

        <template #name>{{ category.name }}</template>
      </list-item>
    </div>
    <div v-else>
      <q-item v-for="n in 10" :key="n">
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>
        <q-item-section>
          <q-item-label>
            <q-skeleton type="rect" />
          </q-item-label>
        </q-item-section>
      </q-item>
    </div>

  </q-page>
</template>

<script setup lang='ts'>
import ListItem from 'src/components/ListItem.vue';
import { useRouter, useRoute } from 'vue-router';
import { useWebApp } from 'src/stores/webapp';
import { computed, onMounted, ref } from 'vue';
import copy from 'copy-text-to-clipboard';
import { IAccount, ICategory, Wallet } from 'src/types';
import { deleteCategoryRequest, getAllUsersInWallet, getCategories, generateWalletLink, getWallets } from 'src/api';
import { ionPersonOutline, ionLinkOutline, ionArrowRedoSharp, ionQrCodeSharp } from '@quasar/extras/ionicons-v7';
import QrCreator from 'qr-creator';



const QRElement = ref()
const QRDialog = ref(false)

function openQRDialog() {
  QrCreator.render({
    text: invite_link.value,
    radius: 0.4, // 0.0 to 0.5
    ecLevel: 'L', // L, M, Q, H
    fill: '#007AFF', // foreground color
    background: null, // color or null for transparent
    size: 256 // in pixels
  }, QRElement.value);
}


const webAppStore = useWebApp()
const router = useRouter()
// const categorieStore = useCategories()
const route = useRoute()
const walletCategories = ref<ICategory[]>()
const loaded = ref(false)

interface IAccountWithOwner extends IAccount {
  user_type: 'owner'
}

const walletUsers = ref<IAccountWithOwner[]>()
const usersLoaded = ref(false)

const walletId = computed(() => {
  return parseInt(route.params.id as string)
})

const invite_link = ref()
const currentWallet = ref({ name: '' })

onMounted(() => {
  webAppStore.showMainButton('Add', () => { router.push({ name: 'newCategory', params: { wallet_id: route.params.id as string } }) })
  loadWalletCategories()
  getWallets().then((response) => {
    currentWallet.value = response.data.find((el: Wallet) => el.id === walletId.value)
  })
  getAllUsersInWallet(walletId.value).then((response) => {
    walletUsers.value = response.data
    usersLoaded.value = true
  })
  generateWalletLink(walletId.value).then((response) => {
    invite_link.value = process.env.WEBAPP_TG_URL + '?startapp=' + response.data.replaceAll('.', '__')
  })
})

const incomeWalletCategories = computed(() => {
  return walletCategories.value?.filter(el => el.transaction_type === 'income')
})

const outcomeWalletCategories = computed(() => {
  return walletCategories.value?.filter(el => el.transaction_type === 'outcome')
})


async function loadWalletCategories() {
  await getCategories(walletId.value).then((response) => {
    walletCategories.value = response.data
    loaded.value = true
  })
}

function deleteCategory(id: number) {
  webAppStore.confirm(async () => {
    await deleteCategoryRequest(id)
    await loadWalletCategories()
  })
}

function editCategory(category: ICategory) {
  router.push({ name: 'editCategory', params: { category_id: category.id, wallet_id: route.params.id } })
}

</script>

<style scoped lang='scss'>
@import '../css/mixins.scss';

.wallet-settings {
  &__username {
    font-size: 17px;
    font-weight: 500;
  }
}

.invite {
  @include input-group;

  &__input {
    white-space: nowrap;
    overflow: hidden;
  }

  &__row {
    max-width: 100%;
  }

  &__button {
    border-radius: 12px;
  }
}
</style>
