<template>
  <div class="category-chart">
    <div class="category-chart__sum">{{ month }}</div>
    <Doughnut :data="data" :options="options"></Doughnut>
  </div>
</template>

<script setup lang="ts">
import {  ref, watch } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, ChartData, Colors } from 'chart.js';

ChartJS.register(ArcElement, Colors);

interface PropsType {
  chartData: number[];
  colors: number[];
  month?: string;
}

const props = defineProps<PropsType>()

const data = ref<ChartData<'doughnut'>>({
  datasets: [
    {
      data: [0],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
    },
  ],
});

const options = ref({
  options: {
    // This chart will not respond to mousemove, etc
    events: ['click'],
    interaction: {
      mode: 'dataset',
    },

  },
  cutout: '85%',
  borderRadius: 20,
  offset: 20,
  borderWidth: 0,
  onClick: (_: any, b: any) => {
    const clickIndex = b[0].index;

    console.log(data.value.datasets[0].data[clickIndex]);
  },
});


watch(() => props.chartData, () => {
  data.value = {
    datasets: [{
      data: props.chartData, backgroundColor: props.colors.map(num => `hsl(${num}, 64%, 61%)`),
    }]
  };

})

</script>

<style scoped lang="scss">
.category-chart {
  position: relative;

  &__sum {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 17px;
  }
}
</style>
