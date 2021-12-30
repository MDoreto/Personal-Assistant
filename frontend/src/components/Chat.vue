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
    <div class="divchat">
      <v-row
        v-for="message in messages"
        :key="message.id"
        class="pa-2 ma-2 d-flex "
        :class="message.sender == 'User' ? 'flex-row-reverse' : 'flex-row'"
        width="100"
        ><v-card
          max-width="75%"
          rounded
          :class="
            message.sender == 'User' ? 'teal lighten-3' : 'blue lighten-3'
          "
          :id="message.id"
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
.divchat {
  max-height: 450px;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;
}
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
      this.messages.unshift({
        text: this.text,
        sender: "User",
        id: this.messages.length,
      });

      var temp = this.text;
      this.text = "";
      var message = { text: "...", sender: "Jarvis", id: this.messages.length };
      this.messages.unshift(message);
      axios
        .post(process.env.VUE_APP_ROOT_API, { text: temp })
        .then((response) => {
          message.text = response.data;
        });
    },
  },
};
</script>