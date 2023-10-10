<template>
  <q-page class="column">
    <div class="row q-ma-sm title">
      Categories
    </div>
    <div>

      <list-item :color="category.color" @delete="deleteCategory" @edit="editCategory" :item="category"
        v-for="category in categorieStore.allCategoriesList" :key="category.id">
        <template #icon>
          {{ category.icon }}
        </template>

        <template #name>{{ category.name }}</template>
      </list-item>


    </div>

  </q-page>
</template>

<script setup lang='ts'>
import ListItem from 'src/components/ListItem.vue';
import { useRouter } from 'vue-router';
import { useWebApp } from 'src/stores/webapp';
import { onMounted } from 'vue';
import { useCategories } from 'src/stores/category';
import { ICategory } from 'src/types';

const webAppStore = useWebApp()
const router = useRouter()
const categorieStore = useCategories()

onMounted(() => {
  webAppStore.showMainButton('Add', () => { router.push({ name: 'addCategory' }) })
})

function deleteCategory(id: number) {
  webAppStore.confirm(() => {
    categorieStore.deleteCategory(id)
  })
}

function editCategory(category: ICategory) {
  router.push({ name: 'editCategory' })
}

</script>

<style scoped lang='scss'></style>
