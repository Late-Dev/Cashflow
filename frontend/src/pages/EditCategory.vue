<template>
  <q-page class="column overflow-hidden">
    <div class="q-ma-sm">
      <ModeToggle :readonly="!!route.params.id" />
    </div>
    <div class="row justify-around items-center">
      <q-avatar :style="{ background: `hsl(${category.color}, 64%, 61%)` }">
        {{ category.icon }}
      </q-avatar>
      <div class="edit-category__group">
        <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="category.icon"
          label="Icon" />
      </div>
    </div>
    <div class="row">
      <q-slider :min="0" :max="360" selection-color="secondary" track-color="rainbow" class="q-ma-md"
        v-model="category.color" color="secondary" :step="1" />
    </div>
    <div class="edit-category__group">
      <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="category.name"
        label="Category name" />


    </div>
  </q-page>
</template>

<script setup lang='ts'>
import { ICategory } from 'src/types';
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useTransaction } from 'src/stores/transactions'
import { useRoute, useRouter } from 'vue-router';
import { useCategories } from 'src/stores/category';
import { useWebApp } from 'src/stores/webapp';
import ModeToggle from 'src/components/ModeToggle.vue';

const router = useRouter()
const categoryStore = useCategories()
const transactionStore = useTransaction()
const route = useRoute()
const webAppStore = useWebApp()

const category = ref<ICategory>({
  id: -1,
  name: '',
  icon: '',
  color: 0,
  transaction_type: 'outcome'
})

onMounted(() => {
  webAppStore.showMainButton('Save', () => {

    if (category.value.id !== -1) {
      categoryStore.createCategory(category.value)
    }
    else {
      categoryStore.editCategory(category.value)
    }

    router.go(-1)
  })
  if (route.params.id) {
    const foundCat = categoryStore.allCategoriesList?.find((el) => el.id === parseInt(route.params.id as string))
    if (foundCat) {
      category.value = foundCat
    }
  }
})

onBeforeUnmount(() => {
  webAppStore.hideMainButton(() => {

    if (category.value.id !== -1) {
      categoryStore.createCategory(category.value)
    }
    else {
      categoryStore.editCategory(category.value)
    }

    router.go(-1)
  })
})



watch(() => transactionStore.currentMode, (value) => {
  category.value.transaction_type = value
}, { immediate: true })


</script>

<style scoped lang='scss'>
.edit-category {
  &__group {


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
