<template>
  <v-card max-width="600" class="mx-auto">
    <v-toolbar color="light-blue" dark>

      <v-toolbar-title>My Events</v-toolbar-title>


    </v-toolbar>

    <v-list subheader two-line>
      <v-list-item v-for="s in events">

        <v-list-item-content>
          <v-list-item-title v-text="s.event_title"></v-list-item-title>
          <v-list-item-subtitle>Date: {{ s.event_date.replace("T", " Time: ").replace("Z", "")  }}</v-list-item-subtitle>
          <v-list-item-subtitle>Status: {{ s.event_status }}</v-list-item-subtitle>
          <v-list-item-subtitle>Location: {{ s.event_location }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn icon>
            <!-- <button @click="deleteStdFct(s.sid)"><v-icon color="grey lighten-1">mdi-delete</v-icon></button>  -->
            <v-row>
              <v-dialog v-model="removeDialogs[s.event_id]" persistent max-width="590">


                <template v-slot:activator="{ on, attrs }">
                  <v-btn class="mr-1" color="blue darken-2" dark v-bind="attrs" v-on="on" @click="getsettime(s.event_date);deleteStd = false">
                    <v-icon color="white lighten-1">mdi-pen</v-icon>
                  </v-btn>
                  <v-btn class="mr-16" color="red darken-2" dark v-bind="attrs" v-on="on" @click="deleteStd = true">
                    <v-icon color="white lighten-1">mdi-delete</v-icon>
                  </v-btn>
                </template>


                <v-card v-if="deleteStd">
                  <v-card-title class="text-h5">
                    Delete
                  </v-card-title>
                  <v-card-text>Do you want to delete <b>{{ s.event_title }}</b> from the database?</v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="removeDialogs[s.event_id] = false">
                      Cancel
                    </v-btn>
                    <v-btn color="red darken-1" text @click="deleteEvent(s.event_id)">
                      Delete
                    </v-btn>
                  </v-card-actions>
                </v-card>


                <v-card v-else>
                  <v-card-title>
                    <span class="text-h5">User Profile</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>

                        <v-col cols="12">
                          <v-text-field label="Title" v-model="s.event_title"></v-text-field>
                        </v-col>

                        <v-row justify="center">
                          <v-date-picker class="mr-1" v-model="s.event_date.split('T')[0]"></v-date-picker>
                          <v-time-picker ampm-in-title format="ampm" v-model="eventTime"></v-time-picker>
                        </v-row>


                        <v-col cols="12">
                          <v-select :items="itemsStatus" :menu-props="{ top: true, offsetY: true }" label="Status"
                            v-model="s.event_status"></v-select>
                        </v-col>

                        <v-col cols="12">
                          <v-text-field label="Location" v-model="s.event_location"></v-text-field>
                        </v-col>

                      </v-row>
                    </v-container>
                    <small>*indicates required field</small>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue-darken-1" variant="text" @click="removeDialogs[s.event_id] = false">
                      Close
                    </v-btn>
                    <v-btn color="blue-darken-1" variant="text"
                      @click="editEvent(s.event_id, s.event_title, s.event_date, s.event_status, s.event_location)">
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
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
      eventTime: '12:00',
    }
  },

  methods: {
    getsettime(dt){
      console.log("test")
      this.eventTime=dt.split('T')[1].replace('Z','')
      return this.eventTime
    },
    async getData() {
      try {
        let formData = new FormData();
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/myevents', formData);
        this.events.push(response.data[0])
        this.events=this.events[0]
      } catch (error) {
        console.log(error);
      }
    },
    async deleteEvent(id) {
      try {
        let formData = new FormData();
        formData.append("eventId", id);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/deleteevent', formData);
        this.status = response.data
        this.hasSaved = true
        this.removeDialogs[id] = false
        this.$router.go()
      } catch (error) {
        console.log(error);
      }
    },
    async editEvent(id, title, date, status, location) {
      try {
        let formData = new FormData();
        formData.append("eventTitle", title);
        formData.append("eventDate", date.split("T")[0]+":"+this.eventTime);
        formData.append("eventLocation", location);
        formData.append("eventStatus", status);
        formData.append("eventId", id);
        const response = await this.$http.post('http://127.0.0.1:9000/editevent', formData);
        this.status = response.data
        this.hasSaved = true
        this.removeDialogs[id] = false
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