<template>
  <v-card class="pa-8" :class="color">
    
    <v-row justify="center" align="center">
      <v-btn readonly :color="color.split(' ')[0] + ' darken-4'" class="compact-form mr-6 elevation-4 white--text" fab  outlined @click="switchLight"><v-icon large color="">mdi-light-switch</v-icon></v-btn
      ><v-icon size="80" class="ml-4">{{ icon }}</v-icon></v-row
    >
  </v-card>
</template>
<style scoped>
.compact-form {
  transform: scale(1.3);
  transform-origin: left;
}
</style>
<script>
import axios from 'axios';
export default {
  props: {
    icon: { required: true },
    value: { required: true },
    color: { default: "" },
  },
  methods:{
    switchLight(){
      axios.post(process.env.VUE_APP_ROOT_API_RASP,{device:'light_bedroom', action:'switch'})
    }
  }
};
</script>