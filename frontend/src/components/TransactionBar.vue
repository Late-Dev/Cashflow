<template>
  <q-item @click="emit('open', 1)" clickable dense class="row items-center transaction-bar"
    :class="{ 'transaction-bar--settings': isSettingsOpened }" v-touch-swipe.mouse.horizontal="handleSwipe">
    <EmojiIcon />
    <div class="col transaction-bar__info">
      <div>
        <div class="transaction-bar__name">
          Clothing and shoes
        </div>
        <div class="transaction-bar__source">
          ZARA
        </div>
      </div>
      <div class="transaction-bar__value">-2,000 $</div>
    </div>
    <div class="transaction-bar__options">
      <q-btn flat @click="emit('edit')" class="transaction-bar__edit"> <q-icon size="md" :name="ionCreate"></q-icon>
        edit</q-btn>
      <q-btn flat @click="emit('delete')" class="transaction-bar__delete"> <q-icon size="md"
          :name="ionTrash"></q-icon>delete</q-btn>
    </div>
  </q-item>
</template>

<script setup lang='ts'>
import { ref } from 'vue';
import EmojiIcon from './EmojiIcon.vue';
import { ionCreate, ionTrash } from '@quasar/extras/ionicons-v7';

const emit = defineEmits(['open', 'edit', 'delete'])

const isSettingsOpened = ref(false)

function handleSwipe({ ...newInfo }) {
  if (newInfo.direction === 'left') {
    isSettingsOpened.value = true
  }
  if (newInfo.direction === 'right') {
    isSettingsOpened.value = false
  }
}
</script>

<style scoped lang='scss'>
.transaction-bar {

  min-height: 60px;
  position: relative;

  transition: transform .2s ease-in-out;
  transform: translateX(0);

  padding: 0;
  padding-left: 10px;

  -moz-user-select: none;
  -khtml-user-select: none;
  user-select: none;

  &--settings {
    transform: translateX(-120px);

  }

  &__info {
    padding: 10px 0;
    padding-right: 16px;
    border-bottom: 1px solid var(--wallet-separator-color, #C8C7CB);
    height: 100%;
    display: flex;

    justify-content: space-between;
    align-items: center;
  }

  &__options {
    position: absolute;
    right: -120px;

    width: 120px;

    display: flex;
  }

  &__delete,
  &__edit {
    width: 60px;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 11px;
    padding: 6px;
    border-radius: 0;
  }

  &__edit {
    background: #0098EA;

  }

  &__delete {
    background: $negative;
  }

  &__value {
    font-size: 17px;
  }

  &__name {
    font-size: 17px;
    line-height: 22px;
  }

  &__source {
    color: $theme-hint;
    font-size: 14px;
    line-height: 18px;
  }
}
</style>
