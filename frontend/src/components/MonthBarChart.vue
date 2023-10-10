<template>
  <div class="month-bar-chart">

    <q-scroll-area style="height: 180px; max-width: 100vw;">
      <div class="row no-wrap">
        <Bar id="my-chart-id" style="width: 200vw; padding: 0 20px;" :options="chartOptions" :data="data" />
      </div>
    </q-scroll-area>
  </div>
</template>

<script setup lang='ts'>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed, ref, watch } from 'vue';

ChartJS.register(Title, BarElement, CategoryScale, LinearScale)


const props = defineProps(['chartData'])


const data = computed(() => {
  return {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    datasets: [{ data: props.chartData, borderRadius: 5, borderSkipped: false, }]
  }
})

const emit = defineEmits(['chooseMonth'])

const chartOptions = {
  responsive: false,
  aspectRatio: 5,
  scales: {
    x: {
      border: {
        display: false
      },
      grid: {
        display: false
      },
    },
    y: {
      border: {
        display: false
      },
      grid: {
        display: false
      },
      ticks: {
        display: false
      }
    }
  },
  onClick: (_: any, b: any) => {
    const clickIndex = b[0].index;
    emit('chooseMonth', clickIndex)
  },
}
</script>

<style scoped lang='scss'>
.month-bar-chart {

  height: 180px;

}
</style>
