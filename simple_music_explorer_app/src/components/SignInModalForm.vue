<template>
  <div>
    <!-- Main sign in modal -->
    <b-modal
        v-if="showSignInModal"
        id="modal-sign-in"
        scrollable
        title="Sign In Form"
        @show="resetFormValues"
        @hidden="resetFormValues"
        @cancel="resetFormValues"
        @ok="onOk"
    >
      <b-form @submit.stop.prevent="handleSubmit">

        <!-- Username input -->
        <b-form-group
            id="input-group-1"
            label="Username:"
            label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="$v.form.username.$model"
            :state="validateState('username')"
            aria-describedby="input-live-feedback"
            placeholder="Enter username"
            trim
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            This filed is a required.
          </b-form-invalid-feedback>
        </b-form-group>

        <!-- Password input -->
        <b-form-group
            id="input-group-2"
            label="Password:"
            label-for="input-2"
        >
          <b-form-input
              id="input-2"
              v-model="$v.form.password.$model"
              :state="validateState('password')"
              type="password"
              placeholder="Enter password"
          ></b-form-input>
        </b-form-group>

      </b-form>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok, cancel }">
        <b-button @click="cancel()">
          Cancel
        </b-button>

        <b-button v-if="!isSignInApiStatusLoading" variant="success" @click="ok()">
          Sign In
        </b-button>

        <b-button v-if="isSignInApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Sign In...
        </b-button>
      </template>
    </b-modal>

    <!-- Error modal -->
    <b-modal
        v-model="isSignInApiStatusError"
        title='Sign in error'
        size='sm'
        buttonSize='sm'
        okVariant='success'
        okTitle='Retry'
        centered
        no-close-on-backdrop
        no-close-on-esc
        body-bg-variant="danger"
        body-text-variant="white"
        hide-header-close
        @ok="onErrorRetryBtn"
        @cancel="onErrorCancelBtn"
    >
      <p class="my-4">
        Please retry to sign in. Can't get data from server.
        Error: {{ authErrorMsg }}
      </p>
    </b-modal>

  </div>
</template>

<script>
  import { validationMixin } from "vuelidate";
  import { required } from "vuelidate/lib/validators";
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";

  export default {
    name: "SignInModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          username: '',
          password: '',
        },
      }
    },
    validations: {
      form: {
        username: {
          required,
        },
        password: {
          required,
        },
      },
    },
      computed: {
      ...mapGetters(['signInApiStatus', 'authErrorMsg', 'showSignInModal']),

      isSignInApiStatusLoading() {
        return +this.signInApiStatus === apiStatusList.LOADING;
      },

      isSignInApiStatusError: {
        get() {
          return +this.signInApiStatus === apiStatusList.ERROR;
        },
        set() {
          this.$store.commit('updateSignInApiStatus', apiStatusList.INIT);
        },
      },
    },
    methods: {
      ...mapActions(['signIn']),

      onOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },

      handleSubmit() {
        this.$v.$touch();

        if (!this.isFieldsInvalid()) {
          this.signIn(this.form);
        }
      },

      isFieldsInvalid() {
        return Object.keys(this.form).some(key => this.$v.form[key].$invalid)
      },

      resetFormValues() {
        Object.keys(this.form).forEach(key => {
          if (this.form[key]) {
            this.form[key] = '';
          }

          this.$nextTick(() => {
            this.$v.$reset();
          });
        });
      },

      validateState(key) {
        const { $dirty, $error } = this.$v.form[key];
        return $dirty ? !$error : null;
      },

      onErrorRetryBtn() {
        this.resetFormValues();
        this.$store.commit('updateSignInApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-sign-in-error');
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-sign-in-error');
        this.$bvModal.hide('modal-sign-in');
      },
    },
  }
</script>

<style scoped>

</style>