<template>
  <div
    id="pressure"
    :style="{ height: height, width: width }"
    
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
      default: "300px",
    },
    height: {
      type: String,
      default: "300px",
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
            min: 900,
            max: 950,
            axisLabel: {
              fontSize: 9,
            },
            detail: {
              valueAnimation: true,
              formatter: "{value} hPA",
              fontSize: 15,
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
