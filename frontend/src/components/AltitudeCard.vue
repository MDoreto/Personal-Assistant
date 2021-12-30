<template>
  <v-card class="light-blue darken-2"
    ><v-card-text class="white--text">
      <p>Altitude</p>
      <v-row align="center" class="flex-nowrap pa-2">
        <span class="display-3">{{ value.toFixed(2) }} </span>m<v-spacer
        ></v-spacer><v-icon size="60" dark>mdi-image-filter-hdr</v-icon></v-row
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