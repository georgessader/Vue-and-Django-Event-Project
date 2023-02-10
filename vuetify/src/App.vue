<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            Events Project
          </v-list-item-title>
          <v-list-item-subtitle>
            for My Network
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" :to="item.to" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Events Application</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <!--  -->
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: null,
      items: [],
      right: null,
    }
  },
  methods: {
    loadApp() {
      console.log("called")
      if (sessionStorage.getItem('username')) {
          this.items = [
            { title: 'My Events', icon: 'mdi-account', to: '/myevents' },
            { title: 'Events', icon: 'mdi-alpha-e-box', to: '/events' },
            { title: 'Create Event', icon: 'mdi-calendar-plus', to: '/home' },
            { title: 'Logout', icon: 'mdi-logout', to: '/logout' },
          ]
      }

      else
        this.items = [
          { title: 'Register', icon: 'mdi-account-plus', to: '/Register' },
          { title: 'Login', icon: 'mdi-login', to: '/Login' },
          { title: 'Events', icon: 'mdi-calendar', to: '/events' },
        ]
    },
  },
  created() {
    this.loadApp();
  },
  mounted() {
    const thisInstance = this
    this.$root.$on('loadApp', function () {
      thisInstance.loadApp()
    })
  }
}
</script>
