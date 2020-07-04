<template>
  <div>
    <div class="d-flex justify-content-center mb-3">
      <b-spinner
          v-if="isActivationApiStatusLoading"
          variant="primary"
          label="Loading..."
      />
    </div>

    <b-alert v-model="isActivationApiStatusError" variant="danger" dismissible>
      Can't get data from server. Error: {{ authErrorMsg }}
    </b-alert>

    <b-alert v-model="isActivationApiStatusLoaded" variant="success" dismissible>
      Account activation succeeded! Now sign in please.
    </b-alert>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";

  export default {
    name: "UserActivation",
    props: ['uid', 'token'],
    data() {
      return {
        loading: false,
      }
    },
    computed: {
      ...mapGetters(['activateApiStatus', 'isUserActive', 'authErrorMsg']),

      isActivationApiStatusLoading() {
        return +this.activateApiStatus === apiStatusList.LOADING;
      },

      isActivationApiStatusLoaded() {
        return +this.activateApiStatus === apiStatusList.LOADED;
      },

      isActivationApiStatusError() {
        return +this.activateApiStatus === apiStatusList.ERROR;
      },
    },
    methods: mapActions(['activate']),
    created() {
      this.loading = true;

      const data = {
        uid: this.uid,
        token: this.token,
      };
      this.activate(data);
    },
    watch: {
      $route: 'activate'
    },
  }
</script>

<style scoped>

</style>