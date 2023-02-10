<script>
export default {
  methods: {
    logOut() {
      sessionStorage.removeItem("username")
      this.$root.$emit('loadApp')
      this.$router.push({ path: '/login' })
    }
  },
  created() {
    this.logOut();
  }
}
</script>