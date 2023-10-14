<template>
  <q-page class="column overflow-hidden ">
    <div class="row q-ma-sm title">
      Team
    </div>
    <div v-if="usersLoaded">

      <!-- {{ walletUsers }} -->
      <q-list bordered>
        <q-item clickable v-ripple v-for="user in walletUsers" :key="user.id">
          <q-item-section avatar>
            <q-avatar color="teal" text-color="white" :icon="ionPersonOutline">
              <img :src="user.photo_url" v-if="user.photo_url">
            </q-avatar>
          </q-item-section>

          <q-item-section class="wallet-settings__username">@{{ user.username }}</q-item-section>
          <q-item-section side>Admin</q-item-section>
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
// import { useCategories } from 'src/stores/category';
import { IAccount, ICategory } from 'src/types';
import { deleteCategoryRequest, getAllUsersInWallet, getCategories } from 'src/api';
import { ionPersonOutline } from '@quasar/extras/ionicons-v7';

const webAppStore = useWebApp()
const router = useRouter()
// const categorieStore = useCategories()
const route = useRoute()
const walletCategories = ref<ICategory[]>()
const loaded = ref(false)

const walletUsers = ref<IAccount[]>()
const usersLoaded = ref(false)

onMounted(async () => {
  webAppStore.showMainButton('Add', () => { router.push({ name: 'newCategory', params: { wallet_id: route.params.id as string } }) })
  await loadWalletCategories()
  await getAllUsersInWallet(parseInt(route.params.id as string)).then((response) => {
    walletUsers.value = response.data
    usersLoaded.value = true
  })
})

const incomeWalletCategories = computed(() => {
  return walletCategories.value?.filter(el => el.transaction_type === 'income')
})

const outcomeWalletCategories = computed(() => {
  return walletCategories.value?.filter(el => el.transaction_type === 'outcome')
})


async function loadWalletCategories() {
  await getCategories(parseInt(route.params.id as string)).then((response) => {
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
.wallet-settings {
  &__username {
    font-size: 17px;
    font-weight: 500;
  }
}
</style>
