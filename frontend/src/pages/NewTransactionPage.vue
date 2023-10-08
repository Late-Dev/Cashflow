<template>
  <q-page class="column">
    <div class="q-ma-sm">
      <ModeToggle />
    </div>
    <div class="q-pa-sm">

      <q-form @submit="onSubmit" @reset="onReset">
        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="The amount" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="Currency" />
        </div>

        <div class="new-transaction__group">

          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="Category" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="Source" />
          <q-input dense filled square outlined bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="Comment" />
        </div>

        <div class="new-transaction__group">

          <q-input dense filled square borderless bg-color="secondary" label-color="dark" color="dark" v-model="text"
            label="Date" />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script setup lang='ts'>
import ModeToggle from 'src/components/ModeToggle.vue';


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
