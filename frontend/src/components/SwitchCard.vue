<template>
  <v-card class="pa-8" :class="color">
    
    <v-row justify="center" align="center">
      <v-switch :color="color.split(' ')[0] + ' darken-4'" class="compact-form mr-12 pt-3" inset :value="value"></v-switch
      ><v-icon size="80" class="ml-4">{{ icon }}</v-icon></v-row
    >
  </v-card>
</template>
<style scoped>
.compact-form {
  transform: scale(2);
  transform-origin: left;
}
</style>
<script>
export default {
  props: {
    icon: { required: true },
    value: { required: true },
    color: { default: "" },
  },
};
</script>