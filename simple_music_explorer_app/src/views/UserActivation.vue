<template>
  <div>
    <div class="d-flex justify-content-center mb-3">
      <b-spinner
          v-if="isActivationApiStatusLoading"
          variant="primary"
          label="Loading..."
      />
    </div>

    <!-- Activation message modal -->
    <b-modal
        v-model="isActivationApiStatusLoaded"
        title='Success'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
    >
      <p class="my-4">
        Account activation succeeded! Now sign in please.
      </p>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ cancel, ok }">
        <b-button variant="secondary" @click="cancel()">
          Cancel
        </b-button>

        <b-button v-b-modal.modal-sign-in variant="success" @click="ok()">
          Sign In
        </b-button>
      </template>

    </b-modal>

    <!-- Error modal -->
    <b-modal
        v-model="isActivationApiStatusError"
        title='Account activation error'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        body-bg-variant="danger"
        body-text-variant="white"
        hide-header-close
        @ok="redirect"
    >
      <p class="my-4">
        Error: {{ authErrorMsg }}
      </p>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok }">
        <b-button size="sm" variant="secondary" @click="ok()">
          Close
        </b-button>
      </template>
    </b-modal>

  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";
  import router from "@/router";

  export default {
    name: "UserActivation",
    props: ['uid', 'token'],
    computed: {
      ...mapGetters(['activateApiStatus', 'authErrorMsg']),

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
    methods: {
      ...mapActions(['activate']),

      redirect() {
        router.push({ name: 'Index' });
      },
    },
    created() {
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