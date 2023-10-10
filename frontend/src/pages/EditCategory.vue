<template>
  <q-page class="column overflow-hidden">
    <div class="q-ma-sm">
      <ModeToggle :readonly="!!route.params.category_id" />
    </div>
    <div v-if="loaded" class="row justify-around items-center">
      <q-avatar :style="{ background: `hsl(${category.color}, 64%, 61%)` }">
        {{ category.icon }}
      </q-avatar>
      <div class="edit-category__group">
        <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="category.icon"
          label="Icon" />
      </div>
    </div>
    <div v-if="loaded" class="row">
      <q-slider :min="0" :max="360" selection-color="secondary" track-color="rainbow" class="q-ma-md"
        v-model="category.color" color="secondary" :step="1" />
    </div>
    <div v-if="loaded" class="edit-category__group">
      <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="category.name"
        label="Category name" />


    </div>
  </q-page>
</template>

<script setup lang='ts'>
import { ICategory } from 'src/types';
import { onMounted, ref, watch } from 'vue';
import { useTransaction } from 'src/stores/transactions'
import { useRoute, useRouter } from 'vue-router';
import { useWebApp } from 'src/stores/webapp';
import ModeToggle from 'src/components/ModeToggle.vue';
import { getCategories, addCategory, editCategoryRequest } from 'src/api';

const router = useRouter()
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


const walletCategories = ref<ICategory[]>()
const loaded = ref(false)

async function loadWalletCategories() {
  await getCategories(parseInt(route.params.category_id as string)).then((response) => {
    walletCategories.value = response.data
    loaded.value = true
  })
}


onMounted(async () => {

  webAppStore.showMainButton('Save', async () => {

    if (category.value.id !== -1) {
      await addCategory(
        category.value.name,
        parseInt(route.params.wallet_id as string),
        transactionStore.currentMode,
        category.value.icon,
        category.value.color)
    }
    else {
      await editCategoryRequest(category.value.id, category.value.name, category.value.icon, category.value.color)

    }

    router.go(-1)
  })
  if (route.params.category_id) {
    await loadWalletCategories()
    const foundCat = walletCategories.value?.find((el) => el.id === parseInt(route.params.category_id as string))
    if (foundCat) {
      category.value = foundCat
    }
  }
  else {
    loaded.value = true
  }
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
