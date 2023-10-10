<template>
  <q-page class="column overflow-hidden ">
    <div class="row q-ma-sm title">
      Categories
    </div>
    <div v-if="loaded" style="padding-bottom: 60px;">
      <list-item :color="category.color" @delete="deleteCategory" @edit="editCategory" :item="category"
        v-for="category in walletCategories" :key="category.id">
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
import { onMounted, ref } from 'vue';
// import { useCategories } from 'src/stores/category';
import { ICategory } from 'src/types';
import { deleteCategoryRequest, getCategories } from 'src/api';

const webAppStore = useWebApp()
const router = useRouter()
// const categorieStore = useCategories()
const route = useRoute()
const walletCategories = ref<ICategory[]>()
const loaded = ref(false)

onMounted(async () => {
  webAppStore.showMainButton('Add', () => { router.push({ name: 'newCategory', params: { wallet_id: route.params.id as string } }) })
  await loadWalletCategories()
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

<style scoped lang='scss'></style>
