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
        <v-icon>mdi-account</v-icon>
        <v-toolbar-title class="font-weight-light">
          Login
        </v-toolbar-title>
        <v-spacer></v-spacer>

      </v-toolbar>


      <v-card-text>
        <v-text-field color="white" label="Username" v-model="username"></v-text-field>
        <v-text-field color="white" label="Password" v-model="password" type="password"></v-text-field>
      </v-card-text>



      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="login">
          Login
        </v-btn>
        <v-btn color="success" :to="this.toregister">
          Register
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
      username: '',
      password: '',
      status: 'Error',
      toregister: '/register'
    }
  },

  methods: {
    async login() {
      try {
        let formData = new FormData();
        formData.append("username", this.username);
        formData.append("password", this.password);
        const response = await this.$http.post('http://127.0.0.1:9000/login', formData);
        this.status = response.data
        if (this.status == "Success") {
          sessionStorage.setItem("username", this.username);
          this.$router.push({ path: '/home' })
        }
      } catch (error) {
        console.log(error);
      }
      this.hasSent = true
    }
  },
  created() {
    if (sessionStorage.getItem('username')) {
      this.$router.push({ path: '/home' })
    }
  }
}
</script>