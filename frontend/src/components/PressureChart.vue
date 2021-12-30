<template>
  <div
    id="pressure"
    :style="{ height: height, width: width }"
    class="grey lighten-4 pa-1"
  ></div>
</template>

<script>
// @ is an alias to /src
import * as echarts from "echarts";
export default {
  data: () => ({
    myChart: null,
  }),
  props: {
    value: { required: true },
    width: {
      type: String,
      default: "350px",
    },
    height: {
      type: String,
      default: "350px",
    },
  },
  watch: {
    value() {
      this.updateChart();
    },
  },
  mounted() {
    var chartDom = document.getElementById("pressure");
    this.myChart = echarts.init(chartDom);
    this.updateChart();
  },
  methods: {
    updateChart() {
      var option = {
        series: [
          {
            name: "Pressure",
            type: "gauge",
            progress: {
              show: true,
            },
            min: 0,
            max: 2000,
            axisLabel: {
              fontSize: 9,
            },
            detail: {
              valueAnimation: true,
              formatter: "{value}",
              fontSize: 20,
            },
            data: [
              {
                value: this.value.toFixed(2),
                name: "PRESSURE",
                fontSize: 10,
              },
            ],
          },
        ],
      };

      this.myChart.setOption(option);
    },
  },
};
</script>
