<template>
  <div>
    <b-spinner v-if="loading" variant="primary" label="Spinning"></b-spinner>

    <b-alert v-model="authErrorStatus" variant="danger">
      Can't get data from server. Error: {{ authErrorMsg }}
    </b-alert>

    <b-alert v-model="isUserActive" variant="success">
      Account activation succeeded! Now sign in please.
    </b-alert>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';

  export default {
    name: "UserActivation",
    props: ['uid', 'token'],
    data() {
      return {
        loading: false,
      }
    },
    computed: mapGetters(['isUserActive', 'authErrorStatus', 'authErrorMsg']),
    methods: mapActions(['activate']),
    created() {
      this.loading = true;

      const data = {
        uid: this.uid,
        token: this.token,
      };
      this.activate(data)
        // .then(data => {
        //   console.log(data);
        .then(() => {
          this.loading = false;
        });
    },
    watch: {
      $route: 'activate'
    },
  }
</script>

<style scoped>

</style>