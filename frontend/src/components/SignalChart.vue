<template>
  <div id="signal" :style="{ height: height, width: width }"></div>
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
    height: {
      type: String,
      default: "350px",
    },
    width: {
      type: String,
      default: "150px",
    },
  },
  mounted() {
    var chartDom = document.getElementById("signal");
    this.myChart = echarts.init(chartDom);
    var option = {
      grid: [
        {
          // Set the margin

          bottom: 50,
          top: 70,
        },
      ],
      title: {
        left: "center",
        right: 10,
        right: "auto",
        top: 15,
        text: "Signal",
        textStyle: {
          fontSize: 20,
        },
      },
      yAxis: {
        // Y axis configuration
        show: true,
        min: 0,
        max: 100,
        offset: -40,
        axisLine: {
          show: false,
        },
        axisTick: {
          // Hidden Scale
          show: false,
        },
        splitLine: {
          // Hidden Scale
          show: false,
        },
        axisLabel: {
          // Y-axis text
          fontSize: 12,
        },
      },
      xAxis: {
        // x-axis configuration
        data: ["RSSI"],
        // x axis data
        show: true,
        axisLine: {
          show: false,
        },
      },
    };
    this.myChart.setOption(option);
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
        series: [
          {
            name: "signal",
            type: "pictorialBar", // Setting Types are like-column
            symbol: "roundRect", // graphics type, rectangle with rounded corners
            barWidth: "30% ", // Column width
            barMaxWidth: "50% ", // Maximum width
            symbolMargin: "3", // graphic vertical interval
            itemStyle: {
              color: "rgb(80, 214, 101)",
            },
            symbolRepeat: true, // Demand
            symbolSize: [25, 6], // Dimensions of graphic elements
            data: [
              {
                value: this.value + 100,
                name: "RSSI",
                fontSize: 10,
              },
            ], // y axial data
            animationEasing: "elasticOut", // animation effect
          },
        ],
      };
      this.myChart.setOption(option);
    },
  },
};
</script>
