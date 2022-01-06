<template>
  <div id="light" :style="{ height: height, width: width }"></div>
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
      default: "300px",
    },
    width: {
      type: String,
      default: "150px",
    },
  },
  mounted() {
    var chartDom = document.getElementById("light");
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
        top: 15,
        text: "Light",
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
        data: ["LDR"],
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
              color: "#fac420",
            },
            symbolRepeat: true, // Demand
            symbolSize: [25, 6], // Dimensions of graphic elements
            data: [
              {
                value: (this.value / 1024 - 1) * -100,
                name: "LDR",
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
