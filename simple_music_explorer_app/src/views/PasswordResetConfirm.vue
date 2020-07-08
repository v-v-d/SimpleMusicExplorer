<template>
  <div>

    <!-- Main password reset confirm modal -->
    <b-modal
        v-model="isPasswordResetConfirmApiStatusInit"
        id="modal-password-reset-confirm"
        scrollable
        title="Password Reset Confirm Form"
        @show="resetFormValues"
        @hidden="resetFormValues"
        @cancel="resetFormValues"
        @ok="onOk"
    >
      <b-form @submit.stop.prevent="handleSubmit">

        <!-- new_password input -->
        <b-form-group
            id="input-group-1"
            label="New password:"
            label-for="input-1"
            description="Your password must be 8-20 characters long, contain only letters and numbers."
        >
          <b-form-input
              id="input-1"
              v-model="$v.form.new_password.$model"
              :state="validateState('new_password')"
              placeholder="Enter new password"
              type="password"
          ></b-form-input>
        </b-form-group>

        <!-- re_new_password input -->
        <b-form-group
            id="input-group-4"
            label="Repeat new password:"
            label-for="input-4"
        >
          <b-form-input
              id="input-4"
              v-model="$v.form.re_new_password.$model"
              :state="validateState('re_new_password')"
              aria-describedby="input-live-feedback"
              placeholder="Enter new password one more time"
              type="password"
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

        <b-button v-if="!isPasswordResetConfirmApiStatusLoading" variant="success" @click="ok()">
          Reset
        </b-button>

        <b-button v-if="isPasswordResetConfirmApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Reset...
        </b-button>
      </template>

    </b-modal>

    <!-- Success message modal -->
    <b-modal
        v-model="isPasswordResetConfirmApiStatusLoaded"
        title='Success'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        @ok="redirect"
    >
      <p class="my-4">
        Password resetting succeeded!
      </p>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok }">
        <b-button variant="success" @click="ok()">
          Close
        </b-button>
      </template>

    </b-modal>

    <!-- Error modal -->
    <b-modal
        v-model="isPasswordResetConfirmApiStatusError"
        id="modal-password-reset-confirm-error"
        title='Password resetting error'
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
        Please retry to reset password. Error: {{ userErrorMsg }}
      </p>
    </b-modal>

  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";
  import router from "@/router";
  import {alphaNum, maxLength, minLength, required, sameAs} from "vuelidate/lib/validators";
  import { validationMixin } from "vuelidate";

  export default {
    name: "PasswordResetConfirm",
    mixins: [validationMixin],
    props: ['uid', 'token'],
    data() {
      return {
        form: {
          new_password: '',
          re_new_password: '',
        },
      };
    },
    validations: {
      form: {
        new_password: {
          required,
          minLength: minLength(8),
          maxLength: maxLength(20),
          alphaNum,
        },
        re_new_password: {
          required,
          sameAsPassword: sameAs('new_password'),
        },
      },
    },
    computed: {
      ...mapGetters(['resetPasswordConfirmApiStatus', 'userErrorMsg']),

      isPasswordResetConfirmApiStatusInit() {
        return +this.resetPasswordConfirmApiStatus === apiStatusList.INIT;
      },

      isPasswordResetConfirmApiStatusLoading() {
        return +this.resetPasswordConfirmApiStatus === apiStatusList.LOADING;
      },

      isPasswordResetConfirmApiStatusLoaded() {
        return +this.resetPasswordConfirmApiStatus === apiStatusList.LOADED;
      },

      isPasswordResetConfirmApiStatusError() {
        return +this.resetPasswordConfirmApiStatus === apiStatusList.ERROR;
      },
    },
    methods: {
      ...mapActions(['resetPasswordConfirm']),

      redirect() {
        router.push({ name: 'Index' });
      },

      onOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },

      handleSubmit() {
        this.$v.$touch();

        if (!this.isFieldsInvalid()) {
          const data = {
            uid: this.uid,
            token: this.token,
            ...this.form,
          };
          this.resetPasswordConfirm(data);
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
        this.$store.commit('updateResetPasswordConfirmApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-password-reset-confirm-error');
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-password-reset-confirm-error');
        this.$bvModal.hide('modal-password-reset-confirm');
        this.redirect();
      },
    },
    created() {
      this.$bvModal.show('modal-password-reset-confirm');
    },
    watch: {
      $route: 'resetPasswordConfirm',
    },
  }
</script>

<style scoped>

</style>