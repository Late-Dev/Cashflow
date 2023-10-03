
<template>
  <div class="app">
    <div class="app_navbar">

    </div>
    <div class="card app__card">


      <CategoryChart />
      <button class="app__new-btn">Add new</button>
    </div>
  </div>
</template>


<script setup lang="ts">
import CategoryChart from './components/CategoryChart/CategoryChart.vue'


</script>

<style scoped lang="scss">
.app{

  &__card {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  &__new-btn{
    margin-top: 1em;
  }
}

</style>
