<template>
    <div class="category-chart">
        <div class="category-chart__sum">$100500</div>
        <Doughnut :data="data" :options="options"></Doughnut>
    </div>
</template>

<script setup lang='ts'>
import { onMounted, ref } from 'vue';
import { Doughnut } from 'vue-chartjs'
import {
    Chart as ChartJS,
    ArcElement,
    ChartData,
    Colors,

} from 'chart.js'



ChartJS.register(ArcElement, Colors)

const data = ref<ChartData<"doughnut">>({ datasets: [{ data: [1, 2, 3, 4, 5] }] })

const options = ref({

})

function generateRandomArray(num = 5, min = 0, max = 10) {
    const localMin = Math.ceil(min);
    const localMax = Math.floor(max);
    const result = []
    for (let n = 0; n < num; n++) {
        result.push(Math.floor(Math.random() * (localMax - localMin + 1)))
    }
    return result;
}

onMounted(() => {
    data.value = { datasets: [{ data: [5, 4, 3, 1, 1] }] }

    setInterval(() => {
        data.value = { datasets: [{ data: generateRandomArray(5, 0, 10) }] }
    }, 3000)
})

</script>

<style scoped lang='scss'>
.category-chart {
    position: relative;

    &__sum {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
}
</style>