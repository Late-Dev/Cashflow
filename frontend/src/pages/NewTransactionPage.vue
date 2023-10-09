<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div class="q-pa-sm">

      <q-form @submit="onSubmit" ref="formElement">
        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model.number="transactionStore.newTransacitonData.value" label="The amount" />
          <!-- <q-field @focus="router.push({ name: 'select', params: { type: 'currency' } })" dense filled square outlined
            bg-color="secondary" label-color="dark" color="dark" v-model="currency" label="Currency">

            <template v-slot:append>
              <div class="text-body2 flex flex-center">
                All <q-icon :name="ionChevronForward" class="cursor-pointer" />
              </div>
            </template>
          </q-field> -->
        </div>

        <div class="new-transaction__group">
          <q-field @focus="router.push({ name: 'select', params: { type: 'category' } })" dense filled square outlined
            bg-color="secondary" label-color="dark" color="dark" v-model="transactionStore.newTransacitonData.category"
            label="Category">
            <template v-slot:control>
              <div class="self-center full-width no-outline" tabindex="0">
                {{ transactionStore.newTransacitonData.category?.name }}
              </div>
            </template>
            <template v-slot:append>
              <div class="text-body2 flex flex-center">
                All <q-icon :name="ionChevronForward" class="cursor-pointer" />
              </div>
            </template>
          </q-field>
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model="transactionStore.newTransacitonData.source" label="Source" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model="transactionStore.newTransacitonData.description" label="Comment" />
        </div>

        <div class="new-transaction__group">
          <q-field dense filled square borderless bg-color="secondary" label-color="dark" color="dark" label="Date"
            v-model="transactionStore.newTransacitonData.date">
            <template v-slot:control>
              <div class="self-center full-width no-outline" tabindex="0">{{ (new
                Date(transactionStore.newTransacitonData.date)).toLocaleDateString() }}
              </div>
            </template>
          </q-field>
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script setup lang='ts'>
import ModeToggle from 'src/components/ModeToggle.vue';
import { onMounted, ref } from 'vue';
import { useWebApp } from 'src/stores/webapp';
import { useRouter } from 'vue-router';
import { useTransaction } from 'src/stores/transactions';
import { ionChevronForward } from '@quasar/extras/ionicons-v7';

const transactionStore = useTransaction()
const router = useRouter()
const formElement = ref()


async function onSubmit() {


  await transactionStore.newTransaciton().then(() => {
    router.go(-1)

  })



  return
}
const webAppStore = useWebApp()

onMounted(() => {
  webAppStore.showMainButton('Save', formElement.value.submit)
})

</script>

<style scoped lang='scss'>
.new-transaction {
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
