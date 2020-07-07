<template>
  <div>
    <!-- Main sign up modal -->
    <b-modal
        v-if="showSignUpModal"
        id="modal-sign-up"
        scrollable
        title="Sign Up Form"
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
            This is a required field and must be at least
            {{ $v.form.username.$params.minLength.min }} characters.
          </b-form-invalid-feedback>
        </b-form-group>

        <!-- Email input -->
        <b-form-group
            id="input-group-2"
            label="Email:"
            label-for="input-2"
            description="We'll never share your email with anyone else."
        >
          <b-form-input
              id="input-2"
              v-model="$v.form.email.$model"
              :state="validateState('email')"
              aria-describedby="input-live-feedback"
              type="email"
              placeholder="Enter email"
              trim
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            Please enter valid email address.
          </b-form-invalid-feedback>
        </b-form-group>

        <!-- Password input -->
        <b-form-group
            id="input-group-3"
            label="Password:"
            label-for="input-3"
            description="Your password must be 8-20 characters long, contain only letters and numbers."
        >
          <b-form-input
              id="input-3"
              v-model="$v.form.password.$model"
              :state="validateState('password')"
              type="password"
              placeholder="Enter password"
          ></b-form-input>
        </b-form-group>

        <!-- Re_password input -->
        <b-form-group
            id="input-group-4"
            label="Repeat password:"
            label-for="input-4"
        >
          <b-form-input
              id="input-4"
              v-model="$v.form.re_password.$model"
              :state="validateState('re_password')"
              aria-describedby="input-live-feedback"
              type="password"
              placeholder="Enter password one more time"
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            Passwords must be the same.
          </b-form-invalid-feedback>
        </b-form-group>

      </b-form>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok, cancel }">
        <b-button @click="cancel()">
          Cancel
        </b-button>

        <b-button v-if="!isSignUpApiStatusLoading" variant="success" @click="ok()">
          Sign Up
        </b-button>

        <b-button v-if="isSignUpApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Sign Up...
        </b-button>
      </template>

    </b-modal>

    <!-- Activation message modal -->
    <b-modal
        v-model="isSignUpApiStatusLoaded"
        id="modal-sign-up-activate"
        title='Activate your account'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        @ok="onActivateOkBtn"
    >
      <p class="my-4">
        Please check your email.
      </p>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok }">
      <b-button size="sm" variant="secondary" @click="ok()">
        Close
      </b-button>
    </template>

    </b-modal>

    <!-- Error modal -->
    <b-modal
        v-model="isSignUpApiStatusError"
        id="modal-sign-up-error"
        title='Sign up error'
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
        Please retry to sign up. Error: {{ authErrorMsg }}
      </p>
    </b-modal>

  </div>
</template>

<script>
  import { validationMixin } from "vuelidate";
  import {
    required, minLength, maxLength, email, sameAs, alphaNum
  } from "vuelidate/lib/validators";
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";

  export default {
    name: "SignUpModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          re_password: '',
        },
      }
    },
    validations: {
      form: {
        username: {
          required,
          minLength: minLength(3),
        },
        email: {
          required,
          email,
        },
        password: {
          required,
          minLength: minLength(8),
          maxLength: maxLength(20),
          alphaNum,
        },
        re_password: {
          required,
          sameAsPassword: sameAs('password'),
        },
      },
    },
    computed: {
      ...mapGetters(['signUpApiStatus', 'authErrorMsg', 'showSignUpModal']),

      isSignUpApiStatusLoading() {
        return +this.signUpApiStatus === apiStatusList.LOADING;
      },

      isSignUpApiStatusLoaded() {
        return +this.signUpApiStatus === apiStatusList.LOADED;
      },

      isSignUpApiStatusError() {
        return +this.signUpApiStatus === apiStatusList.ERROR;
      },
    },
    methods: {
      ...mapActions(['signUp']),

      onOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },

      handleSubmit() {
        this.$v.$touch();

        if (!this.isFieldsInvalid()) {
          this.signUp(this.form);
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

      onActivateOkBtn() {
        this.resetFormValues();
        this.$store.commit('updateSignUpApiStatus', apiStatusList.INIT);
      },

      onErrorRetryBtn() {
        this.resetFormValues();
        this.$store.commit('updateSignUpApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-sign-up-error');
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-sign-up-error');
        this.$bvModal.hide('modal-sign-up');
      },
    },
  }
</script>

<style scoped>

</style>