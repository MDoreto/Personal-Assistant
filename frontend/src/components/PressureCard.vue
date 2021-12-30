<template>
  <v-card class="deep-purple darken-2"
    ><v-card-text class="white--text">
      <p>Pressure</p>
      <v-row align="center" class="flex-nowrap pa-2">
        <span class="display-3">{{ value.toFixed(2) }} </span>hPA<v-spacer
        ></v-spacer><v-icon size="50" dark>mdi-gauge</v-icon></v-row
      >
    </v-card-text></v-card
  >
</template>
    <script>
export default {
  props: {
    value: { required: true, default: "" },
  },
};
</script>