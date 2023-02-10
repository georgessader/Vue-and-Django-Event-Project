<template>
  <v-card max-width="600" class="mx-auto">
    <v-toolbar color="light-blue" dark>

      <v-toolbar-title>My Events</v-toolbar-title>


    </v-toolbar>

    <v-list subheader two-line>
      <v-list-item v-for="(s, i) in events[0]">

        <v-list-item-content>
          <v-list-item-title>{{ s.first_name }} {{ s.last_name }}</v-list-item-title>
          <v-list-item-subtitle>Username: {{ s.username }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn icon>
            <!-- <button @click="deleteStdFct(s.sid)"><v-icon color="grey lighten-1">mdi-delete</v-icon></button>  -->
            <v-row>
              <template>
                <v-btn v-if="checkExists(s.username)" class="mr-1" color="red darken-2" dark
                  @click="clearSU(s.username)">
                  <v-icon color="white lighten-1" style="font-size: 12px;">Remove SU</v-icon>
                </v-btn>
                <v-btn v-else class="mr-1" color="blue darken-2" dark @click="makeSU(s.username)">
                  <v-icon color="white lighten-1" style="font-size: 9px;">Make SU</v-icon>
                </v-btn>
              </template>
            </v-row>
          </v-btn>
        </v-list-item-action>
      </v-list-item>

      <v-snackbar v-model="hasSaved" :timeout="2000" absolute bottom left>
        {{ status }}
      </v-snackbar>
    </v-list>
  </v-card>
</template>



<script>
export default {
  data() {
    return {
      events: [],
      status: '',
      hasSaved: false,
      deleteStd: false,
      removeDialogs: {},
      eventTitle: '',
      eventDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      eventLocation: '',
      itemsStatus: ['Draft', 'Private', 'Public'],
      eventStatus: '',
      suUsers: []
    }
  },

  methods: {
    checkExists(username) {
      return this.suUsers.includes(username)
    },
    async getData() {
      try {
        let formData = new FormData();
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/getusers', formData);
        this.events.push(response.data[0])
        for (var i = 0; i < response.data[1].length; i++)
          this.suUsers.push(response.data[1][i].username)
      } catch (error) {
        console.log(error);
      }
    },
    async clearSU(username) {
      try {
        let formData = new FormData();
        formData.append("user", username);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/clearsuperuser', formData);
        this.$router.go()
      } catch (error) {
        console.log(error);
      }
    },
    async makeSU(username) {
      try {
        let formData = new FormData();
        formData.append("user", username);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/makesuperuser', formData);
        this.$router.go()
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    // Fetch tasks on page load
    this.getData();
    if (!sessionStorage.getItem('username')) {
      this.$router.push({ path: '/login' })
    }


  }
}
</script>
