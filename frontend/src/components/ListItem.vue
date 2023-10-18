<template>
  <q-item @click="emit('open', item.id)" clickable dense class="row items-center transaction-bar"
    :class="{ 'transaction-bar--settings': isSettingsOpened }" v-touch-swipe.mouse.horizontal="handleSwipe">
    <q-avatar :color="typeof color === 'string' ? color : ''" :style="{ background: `hsl(${color}, 64%, 61%)` }"
      class="q-mr-sm">
      <slot name="icon">

        {{ icon }}
      </slot>
    </q-avatar>
    <div class="col col-grow transaction-bar__info">
      <div>
        <div class="transaction-bar__name">
          <slot name="name">

          </slot>
        </div>
        <div class="transaction-bar__source">
          <slot name="source"></slot>
        </div>
      </div>
      <div class="transaction-bar__value">
        <slot name="right"></slot>
      </div>
    </div>
    <div class="transaction-bar__options">
      <q-btn flat @click.stop="emit('edit', item)" class="transaction-bar__edit"> <q-icon size="md"
          :name="ionCreate"></q-icon>
        edit</q-btn>
      <q-btn flat @click.stop="emit('delete', item.id)" class="transaction-bar__delete"> <q-icon size="md"
          :name="ionTrash"></q-icon>delete</q-btn>
    </div>
  </q-item>
</template>

<script setup lang='ts'>
import { ref } from 'vue';
import { ionCreate, ionTrash } from '@quasar/extras/ionicons-v7';


const emit = defineEmits(['open', 'edit', 'delete'])

interface PropsType {
  item: {
    id: number
  },
  color?: string | number,
  icon?: string
}

defineProps<PropsType>()

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
    height: 62px;
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
