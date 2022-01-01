<template>
  <div id="history" :style="{ height: height }"></div>
</template>

<script>
// @ is an alias to /src
import * as echarts from "echarts";
export default {
  data: () => ({
    myChart: null,
  }),
  props: {
    items: { required: true },
    width: {
      type: String,
      default: "725px",
    },
    height: {
      type: String,
      default: "350px",
    },
  },
  mounted() {
    var chartDom = document.getElementById("history");
    this.myChart = echarts.init(chartDom);
    let date = this.items.map((o) =>
      new Date(o.timestamp).toLocaleString("pt-BR")
    );
    var option = {
      tooltip: {
        trigger: "axis",
        position: function (pt) {
          return [pt[0], "10%"];
        },
      },
      title: {
        left: "center",
        top: 15,
        text: "History Weather Chart",
      },
      toolbox: {
        feature: {
          saveAsImage: {},
        },
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: date,
      },
      yAxis: [
        {
          type: "value",
          boundaryGap: [0, "100%"],
          min: 0,
          max: 50,
          axisLabel: {
           formatter: '{value} °C'
          },
        },
        {
          type: "value",
          boundaryGap: [0, "100%"],
          min: 0,
          max: 100,
          axisLabel: {
           formatter: '{value} %',
           align: 'right',
           margin: 50
          },
        },
      ],
      dataZoom: [
        {
          type: "inside",
          start: 0,
          end: 100,
        },
        {
          start: 0,
          end: 100,
        },
      ],
    };
    this.myChart.setOption(option);
    this.updateChart();
  },
  watch: {
    items() {
      this.updateChart();
    },
  },
  methods: {
    updateChart() {
      let date = this.items.map((o) =>
        new Date(o.timestamp).toLocaleString("pt-BR")
      );
      let t = this.items.map((o) => o.temperature);
      let h = this.items.map((o) => o.humidity.toFixed(2));
      var option = {
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: date,
        },

        series: [
          {
            name: "Temperature",

            type: "line",
            symbol: "none",
            sampling: "lttb",
            itemStyle: {
              color: "rgb(255, 70, 131)",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: "rgb(255, 158, 68)",
                },
                {
                  offset: 1,
                  color: "rgb(255, 70, 131)",
                },
              ]),
            },
            data: t,
          },
          {
            name: "Humidity",
            yAxisIndex: 1,
            min: 0,
            max: 100,
            type: "line",
            symbol: "none",
            sampling: "lttb",
            itemStyle: {
              color: "rgba(58,77,233)",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: "rgba(58,77,233,0.8)",
                },
                {
                  offset: 1,
                  color: "rgba(58,77,233,0.3)",
                },
              ]),
            },
            data: h,
          },
        ],
      };
      this.myChart.setOption(option);
    },
  },
};
</script>
