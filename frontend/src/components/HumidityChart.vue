<template>
  <div
    id="humidity"
    :style="{ height: height, width: width }"
  ></div>
</template>

<script>
// @ is an alias to /src
import * as echarts from "echarts";
import "echarts-liquidfill";
export default {
  data: () => ({
    myChart: null,
  }),
  props: {
    value: { required: true },
    height: {
      type: String,
      default: "300px",
    },
    width: {
      type: String,
      default: "300px",
    },
  },
  mounted() {
    var chartDom = document.getElementById("humidity");
    this.myChart = echarts.init(chartDom);
    this.updateChart();
  },
  watch: {
    value() {
      this.updateChart();
    },
  },
  methods: {
    updateChart() {
      var option = {
        grid:{
          left:50
        },
        title: {
          left: "center",
          top: 20,
          text: "Humidity",
          textStyle: {
            fontSize: 25,
          },
        },
        series: [
          {
            type: "liquidFill",
            data: [this.value.toFixed(2) / 100],
          },
        ],
      };
      this.myChart.setOption(option);
    },
  },
};
</script>
