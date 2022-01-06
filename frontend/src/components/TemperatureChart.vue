<template>
  <div
    id="temperature"
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
      default: "350px",
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
    var chartDom = document.getElementById("temperature");
    this.myChart = echarts.init(chartDom);
    this.updateChart();
  },
  methods: {
    updateChart() {
      var option = {
        series: [
          {
            type: "gauge",
            center: ["50%", "60%"],
            startAngle: 200,
            endAngle: -20,
            min: 0,
            max: 50,
            splitNumber: 10,
            itemStyle: {
              color: "#FFAB91",
            },
            progress: {
              show: true,
              width: 30,
            },
            pointer: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                width: 30,
              },
            },
            axisTick: {
              distance: -45,
              splitNumber: 5,
              lineStyle: {
                width: 1,
                color: "#999",
              },
            },
            splitLine: {
              distance: -52,
              length: 14,
              lineStyle: {
                width: 2,
                color: "#999",
              },
            },
            axisLabel: {
              distance: -10,
              color: "#999",
              fontSize: 15,
            },
            anchor: {
              show: false,
            },
            title: {
              show: false,
            },
            detail: {
              valueAnimation: true,
              width: "60%",
              lineHeight: 20,
              borderRadius: 8,
              offsetCenter: [0, "-5%"],
              fontSize: 30,
              fontWeight: "bolder",
              formatter: "{value} °C",
              color: "inherit",
            },
            data: [this.value],
          },
          {
            type: "gauge",
            center: ["50%", "60%"],
            startAngle: 200,
            endAngle: -20,
            min: 0,
            max: 50,
            itemStyle: {
              color: "#FD7347",
            },
            progress: {
              show: true,
              width: 8,
            },
            pointer: {
              show: false,
            },
            axisLine: {
              show: false,
            },
            axisTick: {
              show: false,
            },
            splitLine: {
              show: false,
            },
            axisLabel: {
              show: false,
            },
            detail: {
              show: false,
            },
            data: [
              {
                value: this.value,
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
