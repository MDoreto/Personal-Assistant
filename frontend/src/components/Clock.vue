<template>
  <v-card class="purple white--text pa-6"
    ><v-row
      ><v-col cols="1 padding-top"
        ><div class="verticaltext">LAST UPDATE</div></v-col
      ><v-col
        ><v-row justify="center" class="display-1 black--text nomargin pl-4">{{
          splitDate[4]
        }}</v-row>
        <v-row class="white--text flex-nowrap nomargin"
          ><v-col
            ><v-row justify="center" align="center" class="display-2 pt-1 pl-7">{{
              splitDate[2]
            }}</v-row></v-col
          ><v-col class="nomargin"
            ><v-row justify="center">{{ splitDate[1] }}</v-row
            ><v-row justify="center" class="headline">{{
              splitDate[3]
            }}</v-row></v-col
          ></v-row
        ></v-col
      ></v-row
    ></v-card
  >
</template>
<style scoped>
.verticaltext {
  display: block;
  transform: rotate(270deg);
  font-size: 12px !important;
  white-space: pre;
}
.padding-top {
  padding-top: 67px;
  padding-right: 0;
  padding-bottom: 0;
  padding-left: 0;
  margin-left: 0;
  color: #E1BEE7;
}
.nomargin{
    margin-left:-40px;
}
</style>
<script>
export default {
  props: {
    date: { required: true },
  },
  computed: {
    splitDate() {
      return this.date.toString().split(" ");
    },
  },
};
</script>