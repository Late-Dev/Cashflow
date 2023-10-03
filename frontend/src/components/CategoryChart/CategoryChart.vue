<template>
    <div>
        <Doughnut :data="data"></Doughnut>
    </div>
</template>

<script setup lang='ts'>
import { ref } from 'vue';
import { Doughnut } from 'vue-chartjs'
import {
    Chart as ChartJS,
    ArcElement,
    ChartData,
    Colors
} from 'chart.js'



ChartJS.register(ArcElement, Colors)

const data = ref<ChartData<"doughnut">>({ datasets: [{ data: [1, 2, 3, 4, 5] }] })

</script>

<style scoped lang='scss'></style>