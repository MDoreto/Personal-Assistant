<template>
  <div class="pa-10 maindiv" v-if="nodeMcu && devices">
    <v-row justify="center">{{
      this.measures
        ? new Date(lastMeasure.timestamp).toLocaleString("pt-BR")
        : ""
    }}</v-row>
    <v-row justify="center" align="center" class=""
      ><v-col cols="12" xl="2" lg="3" md="2" sm="12" xs="12" class="ma-1"
        ><AltitudeCard :value.sync="nodeMcu.altitude" /></v-col
      ><v-col cols="12" xl="2" lg="2" md="2" sm="12" xs="12" class="ma-1"
        ><SwitchCard
          :value.sync="devices.tv_bedroom"
          icon="mdi-television"
          color="red lighten-2" /></v-col
      ><v-col cols="12" xl="2" lg="2" md="2" sm="12" xs="12" class="ma-1"
        ><SwitchCard
          :value.sync="devices.desktop_bedroom"
          icon="mdi-desktop-classic"
          color="brown lighten-3" /></v-col
      ><v-col cols="12" xl="2" lg="2" md="2" sm="12" xs="12" class="ma-1"
        ><SwitchCard
          :value.sync="devices.nodemcu_bedroom"
          icon="mdi-car-esp"
          color="yellow lighten-3" /></v-col
      ><v-col cols="12" xl="2" lg="2" md="2" sm="12" xs="12" class="ma-1"
        ><LightCard
          :value="true"
          icon="mdi-lightbulb-on-outline"
          color="orange lighten-3" /></v-col
      ><v-col
        cols="12"
        xl="auto"
        lg="3"
        md="12"
        xs="12"
        sm="12"
        class="grey lighten-4 ma-1"
      >
        <TemperatureChart :value.sync="lastMeasure.temperature" /></v-col
      ><v-col cols="5" lg="1" xs="1" sm="1" class="grey lighten-4 ma-1">
        <SignalChart :value.sync="nodeMcu.rssi" /></v-col
      ><v-col cols="5" lg="1" xs="1" sm="1" class="grey lighten-4 ma-1">
        <LightChart :value.sync="nodeMcu.light" /></v-col
      ><v-col cols="12" lg="auto" xs="12" sm="12" class="grey lighten-4 ma-1">
        <HumidityChart :value.sync="lastMeasure.humidity" /></v-col
      ><v-col cols="12" lg="2" xs="12" sm="12" class="grey lighten-4 ma-1"><PressureChart :value.sync="lastMeasure.pressure" /></v-col
      ><v-col
        cols="12"
        xl="12"
        lg="12"
        md="12"
        sm="12"
        xs="12"
        class="grey lighten-4 ma-1"
        ><HistoryChart :items.sync="measures"
      /></v-col>
    </v-row>

    <v-btn
      color="blue darken-2"
      dark
      fab
      bottom
      right
      fixed
      @click="chat = !chat"
    >
      <v-icon v-if="chat"> mdi-close </v-icon>
      <v-icon v-else> mdi-message-outline </v-icon>
    </v-btn>
    <v-dialog
      v-model="chat"
      content-class="chat-dialog"
      hide-overlay
      width="350"
      transition="dialog-bottom-transition"
    >
      <Chat
    /></v-dialog>
  </div>
</template>
<style scoped>
>>> .chat-dialog {
  position: fixed;
  bottom: 60px;
  right: 10px;
}
</style>
<script>
// @ is an alias to /src
import { db } from "../firebaseDatabase.js";
export default {
  data: () => ({
    nodeMcu: null,
    chat: false,
    devices: null,
  }),
  components: {
    PressureChart: () => import("@/components/PressureChart.vue"),
    SignalChart: () => import("@/components/SignalChart.vue"),
    LightChart: () => import("@/components/LightChart.vue"),
    TemperatureChart: () => import("@/components/TemperatureChart.vue"),
    HumidityChart: () => import("@/components/HumidityChart.vue"),
    HistoryChart: () => import("@/components/HistoryChart.vue"),
    AltitudeCard: () => import("@/components/AltitudeCard.vue"),
    PressureCard: () => import("@/components/PressureCard.vue"),
    Chat: () => import("@/components/Chat.vue"),
    SwitchCard: () => import("@/components/SwitchCard.vue"),
    LightCard: () => import("@/components/LightCard.vue"),
  },
  firebase: {
    nodeMcu: db.ref("NodeMcu"),
    devices: db.ref("Devices"),
  },
  computed: {
    measures() {
      return Object.values(this.nodeMcu.bme280);
    },
    lastMeasure() {
      return this.measures.at(-1);
    },
  },
};
</script>
