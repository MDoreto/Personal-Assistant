<template>
  <v-card color="grey lighten-4" height="600" class="d-flex flex-column">
    <div>
      <v-toolbar color="blue white--text" @click="close()">
        <v-toolbar-title>Jarvis</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="audio = !audio" dark>
          <v-icon v-if="audio">mdi-volume-high</v-icon>
          <v-icon v-else>mdi-volume-off</v-icon>
        </v-btn>
      </v-toolbar>
    </div>
    <div class="divchat">
      <v-row
        v-for="message in messages"
        :key="message.id"
        class="pa-2 ma-2 d-flex"
        :class="message.sender == 'User' ? 'flex-row-reverse' : 'flex-row'"
        width="100"
        ><v-card
          max-width="75%"
          rounded
          :class="
            message.sender == 'User' ? 'teal lighten-3' : 'blue lighten-3'
          "
          @click="printData(message.data)"
        >
          <v-card-text
            ><span class="font-weight-bold">{{ message.sender }}</span
            ><br />
            <p class="text--primary">
              {{
                message.data
                  ? message.sender == "User"
                    ? message.data.queryText
                    : message.data.fulfillmentText
                  : "..."
              }}
            </p>
          </v-card-text></v-card
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
        @keyup.enter="sendMessage"
      >
        <template slot="prepend"
          ><v-icon
            :color="recording ? 'red' : 'blue'"
            class="pt-1"
            @click="record"
            >mdi-microphone</v-icon
          ></template
        ><template slot="append-outer"
          ><v-icon color="blue" class="pt-1" @click="sendMessage"
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
    audio: true,
    recording: false,
    chunks: [],
    mediaRecorder: null,
  }),
  created() {},
  methods: {
    close() {
      this.$emit("update:dialog", false);
    },
    printData(item) {
      console.log(item);
    },
    record() {
      if (this.recording) {
        this.mediaRecorder.stop();
        this.recording = false;
      } else {
        navigator.mediaDevices
          .getUserMedia({
            audio: true,
          })
          .then((stream) => {
            this.mediaRecorder = new MediaRecorder(stream);
            this.mediaRecorder.start();
            this.messages.unshift({
              data: null,
              sender: "User",
              id: this.messages.length,
            });
            this.mediaRecorder.ondataavailable =
              this.mediaRecorderDataAvailable;
            this.mediaRecorder.onstop = this.mediaRecorderStop;
          })
          .catch((err) => {
            alert(`The following error occurred: ${err}`);
          });
        this.recording = true;
      }
    },
    mediaRecorderDataAvailable(e) {
      this.chunks.push(e.data);
    },
    mediaRecorderStop() {
      var audioBlob = new Blob(this.chunks, { type: "audio/webm;codecs=opus" });

      this.mediaRecorder = null;
      this.chunks = [];
      var file = new File([audioBlob], "teste");
      let formData = new FormData();
      formData.append("audio", file);

      axios
        .post(process.env.VUE_APP_ROOT_API + "audio", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })

        .then((response) => {
          this.messages[0].data = response.data.queryResult;
          this.messages.unshift({
            data: {
              fulfillmentText: response.data.queryResult.fulfillmentText,
            },
            sender: "Jarvis",
            id: this.messages.length,
          });
          if (this.audio)
            axios
              .get(process.env.VUE_APP_ROOT_API + "audio_file", {
                responseType: "blob",
              })
              .then((res) => {
                let blob = new Blob([res.data], { type: "audio/wav" });
                var url = URL.createObjectURL(blob);
                var audio = new Audio();
                audio.src = url;
                audio.play();
                const promise = audio.play();
                if (promise !== undefined) {
                  // On older browsers play() does not return anything, so the value would be undefined.
                  promise
                    .then(() => {
                      // Audio is playing.
                    })
                    .catch((error) => {
                      console.log(error);
                    });
                }
              });
          this.audioBlob = null;
        })
        .catch((err) => {
          this.audioBlob = null;
        });
    },

    sendMessage() {
      if (this.text) {
        this.messages.unshift({
          data: { queryText: this.text },
          sender: "User",
          id: this.messages.length,
        });
        var temp = this.text;
        this.text = "";
        var message = {
          data: null,
          sender: "Jarvis",
          id: this.messages.length,
        };
        this.messages.unshift(message);
        axios
          .post(process.env.VUE_APP_ROOT_API + "message", { text: temp })
          .then((response) => {
            (message.data = {
              fulfillmentText: response.data.queryResult.fulfillmentText,
            }),
              (this.messages[1].data = response.data.queryResult);
          });
      }
    },
  },
};
</script>