<style>
#card {
  width: 50%;
  margin: auto;
  margin-top: 10px;
}

@media screen and (max-width:800px) {
  #card {
    width: 100%;
  }
}
</style>

<template>
  <v-app>
    <v-card id="card" class="overflow-hidden p" color="purple lighten-1" dark>
      <v-toolbar flat color="purple">
        <v-icon class="mr-1">mdi-calendar-plus</v-icon>
        <v-toolbar-title class="font-weight-light">
          Create Event
        </v-toolbar-title>
        <v-spacer></v-spacer>

      </v-toolbar>

      <v-card-text>
        <v-text-field color="white" label="Title" v-model="eventTitle"></v-text-field>
        <v-row justify="center">
          <v-date-picker class="mr-1" v-model="eventDate"></v-date-picker>
          <v-time-picker ampm-in-title format="ampm" v-model="eventTime"></v-time-picker>
        </v-row>
       
        <v-col cols="12">
          <v-select :items="itemsStatus" :menu-props="{ top: true, offsetY: true }" label="Status"
            v-model="eventStatus"></v-select>
        </v-col>
        <v-text-field color="white" label="Location" v-model="eventLocation"></v-text-field>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="login">
          Create Event
        </v-btn>
      </v-card-actions>
      <v-snackbar v-model="hasSent" :timeout="2000" absolute bottom left>
        {{ status }}
      </v-snackbar>
    </v-card>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      hasSent: false,
      eventTitle: '',
      eventDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      eventTime: '12:00',
      eventLocation: '',
      itemsStatus: ['Draft', 'Private', 'Public'],
      eventStatus: '',
      status: 'Error',
    }
  },

  methods: {
    async login() {
      try {
        let formData = new FormData();
        formData.append("eventTitle", this.eventTitle);
        formData.append("eventDate", this.eventDate+":"+this.eventTime);
        formData.append("eventLocation", this.eventLocation);
        formData.append("eventStatus", this.eventStatus);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/home', formData);
        this.status = response.data
      } catch (error) {
        console.log(error);
      }
      this.hasSent = true
    }
  },
  created() {
    this.$root.$emit('loadApp')
    if (!sessionStorage.getItem('username')) {
      this.$router.push({ path: '/login' })
    }
  }
}
</script>