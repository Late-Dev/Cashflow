<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div class="q-pa-sm">

      <q-form @submit="onSubmit" ref="formElement">
        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark"
            v-model.number="amount" label="The amount" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="currency"
            label="Currency" />
        </div>

        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="category"
            label="Category" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="source"
            label="Source" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="comment"
            label="Comment" />
        </div>

        <div class="new-transaction__group">

          <q-input dense filled square borderless bg-color="secondary" label-color="dark" color="dark" v-model="dateField"
            label="Date" />
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

const useTransactionStore = useTransaction()
const router = useRouter()
const formElement = ref()

const amount = ref(0);
const currency = ref<string>();
const category = ref()
const source = ref()
const comment = ref()
const dateField = ref()

async function onSubmit() {



  await useTransactionStore.newTransaciton({

    value: amount.value,
    category: category.value,
    source: source.value,
    description: comment.value,
    date: dateField.value,
  }).then(()=>{
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
