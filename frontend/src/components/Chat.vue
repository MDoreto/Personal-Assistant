<template>
  <v-card color="grey lighten-4" height="600" class="d-flex flex-column">
    <div>
      <v-toolbar color="blue white--text">
        <v-toolbar-title>Jarvis</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="audio = !audio" dark>
          <v-icon v-if="audio">mdi-volume-off</v-icon>
          <v-icon v-else>mdi-volume-high</v-icon>
        </v-btn>
      </v-toolbar>
    </div>
    <div>
      <v-row
        v-for="message in messages"
        :key="message"
        class="pa-2 ma-2 d-flex"
        :class="message.sender == 'User' ? 'flex-row-reverse' : 'flex-row'"
        width="100"
        ><v-card
          max-width="75%"
          rounded
          :class="
            message.sender == 'User' ? 'teal lighten-3' : 'blue lighten-3'
          "
          class=""
        >
          <v-card-text
            ><span class="font-weight-bold">{{ message.sender }}</span
            ><br />
            <p class="text--primary">{{ message.text }}</p></v-card-text
          ></v-card
        ></v-row
      >
    </div>
    <v-spacer></v-spacer>
    <v-card-actions>
      <v-text-field
        label="Type here"
        solo
        rounded
        v-model="text"
        @keyup.enter="sendMessage()"
      >
        <template slot="prepend"
          ><v-icon color="blue" class="pr-2 pt-1"
            >mdi-microphone</v-icon
          ></template
        ><template slot="append-outer"
          ><v-icon color="blue" class="pl-2 pt-1" @click="sendMessage()"
            >mdi-send</v-icon
          ></template
        >
      </v-text-field>
    </v-card-actions>
  </v-card>
</template>
<style scoped>
</style>
<script>
import axios from "axios";
export default {
  name: "Chat",
  data: () => ({
    messages: [],
    text: "",
    audio: false,
  }),
  created() {},
  methods: {
    closeDialog() {
      this.$emit("update:dialog", false);
    },
    sendMessage() {
      this.messages.push({ text: this.text, sender: "User" });
      var temp = this.text;
      this.text = "";
      axios
        .post("http://127.0.0.1:5000/dialogflow", { text: temp })
        .then((response) => {
          this.messages.push({ text: response.data, sender: "Jarvis" });
          console.log(this.messages);
        });
    },
  },
};
</script>