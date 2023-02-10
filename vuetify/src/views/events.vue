<template>
  <v-card max-width="600" class="mx-auto">

    <template>
      <v-row justify="center">
        <v-dialog v-model="searchDialog" persistent max-width="400">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" class="mt-10 mb-10" dark v-bind="attrs" v-on="on">
              Search
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h5">
              Search Filter
            </v-card-title>


            <v-card-text>
              <v-container>
                <v-row>

                  <v-col cols="12">
                    <v-text-field label="Title" v-model="searchTitle"></v-text-field>
                  </v-col>

                  <v-checkbox v-model="checkDateSearch"
                    :label="`Search using date: ${checkDateSearch.toString()}`"></v-checkbox>
                  <v-row justify="center" v-if="checkDateSearch">
                    <v-date-picker v-model="searchDate"></v-date-picker>
                  </v-row>

                  <v-col cols="12">
                    <v-combobox v-model="searchStatusSelect" :items="searchStatus" label="Status" multiple outlined
                      dense></v-combobox>
                  </v-col>

                  <v-col cols="12">
                    <v-text-field label="Location" v-model="searchLocation"></v-text-field>
                  </v-col>

                </v-row>
              </v-container>
            </v-card-text>


            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="clearSearch()">
                Clear Search
              </v-btn>
              <v-btn color="green darken-1" text @click="searchDialog = false">
                Cancel
              </v-btn>
              <v-btn color="green darken-1" text
                @click="getDataBySearch(searchTitle, searchDate, searchStatusSelect, searchLocation)">
                Search
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </template>



    <v-toolbar color="light-blue" dark>

      <v-toolbar-title>Events</v-toolbar-title>

    </v-toolbar>


    <v-list subheader two-line>
      <v-list-item v-for="s in events">

        <v-list-item-content>
          <v-list-item-title>{{ subUsers[s.event_id][0].first_name }} {{ subUsers[s.event_id][0].last_name
          }}</v-list-item-title>
          <v-list-item-title v-text="s.event_title"></v-list-item-title>
          <v-list-item-subtitle>Date: {{ s.event_date.replace("T", " Time: ").replace("Z", "") }}</v-list-item-subtitle>
          <v-list-item-subtitle>Status: {{ s.event_status }}</v-list-item-subtitle>
          <v-list-item-subtitle>Location: {{ s.event_location }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action style="margin-right: 110px;">
          <v-btn icon>
            <v-row>
              <v-dialog v-model="removeDialogs[s.event_id]" max-width="700">


                <template justify="left" v-slot:activator="{ on, attrs }">
                  <template v-if="isLogged">
                    <template v-if="s.event_status != 'Draft'">
                      <v-btn v-if="checkExists(s.event_id)" class="mr-1" color="red darken-2" dark
                        @click="unsubscribeEvent(s.event_id)">
                        <v-icon color="white lighten-1" style="font-size: 9px;">unsubscribe</v-icon>
                      </v-btn>
                      <v-btn v-else class="mr-1" color="blue darken-2" dark @click="subscribeEvent(s.event_id)">
                        <v-icon color="white lighten-1" style="font-size: 12px;">subscribe</v-icon>
                      </v-btn>
                    </template>


                    <template v-if="canEdit > 0 || subUsers[s.event_id][0].username == getUsername()">
                      <v-btn class="mr-1" color="blue darken-2" dark v-bind="attrs" v-on="on" @click="modeBtn = 1; getsettime(s.event_date)">
                        <v-icon color="white lighten-1">mdi-pen</v-icon>
                      </v-btn>
                      <v-btn class="mr-1" color="red darken-2" dark v-bind="attrs" v-on="on" @click="modeBtn = 2">
                        <v-icon color="white lighten-1">mdi-delete</v-icon>
                      </v-btn>
                    </template>

                  </template>


                  <v-btn class="mr-1" max-width="25" color="blue darken-1" dark v-bind="attrs" v-on="on"
                    @click="getSubscribers(s.event_id)">
                    <v-icon color="white lighten-1">{{ subCounts[s.event_id] }}</v-icon>
                  </v-btn>

                </template>


                <v-card v-if="modeBtn == 0">
                  <v-card-title class="text-h5">
                    Subscribers
                  </v-card-title>
                  <v-card-text v-for="sub in subscribers[0]">
                    <b>{{ sub.first_name }} {{ sub.last_name }}</b>, Username: <b>{{ sub.username }}</b>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="removeDialogs[s.event_id] = false">
                      Close
                    </v-btn>
                  </v-card-actions>
                </v-card>



                <v-card v-else-if="modeBtn == 2">
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
                    <span class="text-h5">Edit Event</span>
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
      modeBtn: 0,
      removeDialogs: {},
      itemsStatus: ['Draft', 'Private', 'Public'],
      Subscribed: [],
      idSubscribed: [],
      subscribers: [],
      isLogged: false,
      searchDialog: false,
      searchTitle: '',
      searchDate: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      searchStatus: ['Draft', 'Private', 'Public'],
      searchStatusSelect: [],
      searchLocation: '',
      checkDateSearch: false,
      canEdit: 0,
      subUsers: [],
      subCounts: new FormData(),
      eventTime: '12:00',
    }
  },
  methods: {
    getsettime(dt){
      this.eventTime=dt.split('T')[1].replace('Z','')
      return this.eventTime
    },
    clearSearch() {
      this.searchTitle = ''
      this.searchStatusSelect = []
      this.searchLocation = ''
      this.checkDateSearch = false
      this.$router.go()
    },
    getUsername() {
      return sessionStorage.getItem("username")
    },
    async getSubscribers(id) {
      try {
        this.subscribers = []
        let formData = new FormData();
        formData.append("username", sessionStorage.getItem("username"));
        formData.append("eventId", id);
        const response = await this.$http.post('http://127.0.0.1:9000/getsubscribers', formData);
        this.subscribers.push(response.data)
        this.modeBtn = 0
      } catch (error) {
        console.log(error);
      }
    },
    checkExists(id) {
      return this.idSubscribed.includes(id)
    },
    async getData() {
      try {
        this.events = []
        this.subUsers = []
        this.canEdit = 0
        this.subCounts = 0
        this.Subscribed = []
        this.isLogged = sessionStorage.getItem('username')
        let formData = new FormData();
        formData.append("username", sessionStorage.getItem("username"));
        formData.append("isSearch", false);
        const response = await this.$http.post('http://127.0.0.1:9000/events', formData);
        this.events.push(response.data[0])
        this.canEdit = response.data[4]
        this.subCounts = response.data[3]
        this.subUsers.push(response.data[1])
        this.subUsers = this.subUsers[0]
        this.events = this.events[0]
        this.Subscribed.push(response.data[2])
        for (var j = 0; j < this.Subscribed[0].length; j++)
          this.idSubscribed.push(this.Subscribed[0][j].event_id)


      } catch (error) {
        console.log(error);
      }
    },
    async getDataBySearch(titleVal, dateVal, statusVal, locationVal) {
      try {
        this.events = []
        this.subUsers = []
        this.canEdit = 0
        this.subCounts = 0
        this.Subscribed = []
        let formData = new FormData();
        formData.append("username", sessionStorage.getItem("username"));
        formData.append("eventTitle", titleVal);
        if (this.checkDateSearch)
          formData.append("eventDate", dateVal);
        else
          formData.append("eventDate", "");
        formData.append("eventStatus", statusVal);
        formData.append("eventLocation", locationVal);
        formData.append("isSearch", true);
        const response = await this.$http.post('http://127.0.0.1:9000/events', formData);
        this.events.push(response.data[0])
        this.canEdit = response.data[4]
        this.subCounts = response.data[3]
        this.subUsers.push(response.data[1])
        this.subUsers = this.subUsers[0]
        this.events = this.events[0]
        this.Subscribed.push(response.data[2])
        for (var j = 0; j < this.Subscribed[0].length; j++)
          this.idSubscribed.push(this.Subscribed[0][j].event_id)
        this.searchDialog = false
      } catch (error) {
        console.log(error);
      }
    },
    async subscribeEvent(id) {
      try {
        let formData = new FormData();
        formData.append("eventId", id);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/subscribeevent', formData);
        this.status = response.data
        this.hasSaved = true
        this.$router.go()
      } catch (error) {
        console.log(error);
      }
    },
    async unsubscribeEvent(id) {
      try {
        let formData = new FormData();
        formData.append("eventId", id);
        formData.append("username", sessionStorage.getItem("username"));
        const response = await this.$http.post('http://127.0.0.1:9000/unsubscribeevent', formData);
        this.status = response.data
        this.hasSaved = true
        this.$router.go()
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
    }
  },
  created() {
    this.getData();
  }
}
</script>