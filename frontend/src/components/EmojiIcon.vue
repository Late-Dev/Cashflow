<template>
  <div :style="{ background: `hsl(${color}, 64%, 61%)` }" class="flex-center emoji-icon">
    <slot></slot>
  </div>
</template>

<script setup lang='ts'>
defineProps(['color'])

</script>

<style scoped lang='scss'>
.emoji-icon {
  height: 40px;
  width: 40px;
  margin: 5px;
  font-size: 24px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;

}
</style>
