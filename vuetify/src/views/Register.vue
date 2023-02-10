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
  <v-app id="inspire">
    <v-card id="card" class="overflow-hidden p" color="purple lighten-1" dark>
      <v-toolbar flat color="purple">
        <v-icon>mdi-account</v-icon>
        <v-toolbar-title class="font-weight-light">
          Sign Up
        </v-toolbar-title>
        <v-spacer></v-spacer>

      </v-toolbar>


      <v-card-text>
        <v-text-field color="white" label="First Name" v-model="fname"></v-text-field>
        <v-text-field color="white" label="Last Name" v-model="lname"></v-text-field>
        <v-text-field color="white" label="Username" v-model="username"></v-text-field>
        <v-text-field color="white" label="Email" v-model="email"></v-text-field>
        <v-text-field color="white" label="Password" v-model="password1" type="password"></v-text-field>
        <v-text-field color="white" label="Confirm Password" v-model="password2" type="password"></v-text-field>
      </v-card-text>



      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" :to="this.tologin">
          Login
        </v-btn>
        <v-btn color="success" @click="save">
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
      fname: '',
      lname: '',
      username: '',
      email: '',
      password1: '',
      password2: '',
      status: 'Error',
      tologin: '/login'
    }
  },

  methods: {
    async save() {
      try {

        let formData = new FormData();
        formData.append("first_name", this.fname);
        formData.append("last_name", this.lname);
        formData.append("username", this.username);
        formData.append("email", this.email);
        formData.append("password1", this.password1);
        formData.append("password2", this.password2);
        const response = await this.$http.post('http://127.0.0.1:9000/', formData);
        this.status = response.data
      } catch (error) {
        console.log(error);
      }
      this.hasSent = true
    }
  },
  created() {
    this.$root.$emit('loadApp')
    if (sessionStorage.getItem('username')) {
      this.$router.push({ path: '/login' })
    }
  }
}
</script>