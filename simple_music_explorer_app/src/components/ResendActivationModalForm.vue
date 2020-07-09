<template>
  <div>
    <b-modal
        id="modal-resend-activation"
        scrollable
        title="Resend Activation Form"
        @hidden="resetFormValues"
        @cancel="resetFormValues"
        @ok="onOk"
    >
      <b-form @submit.stop.prevent="handleSubmit">

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

      </b-form>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok, cancel }">
        <!-- Emulate built in modal footer ok and cancel button actions -->
        <b-button @click="cancel()">
          Cancel
        </b-button>

        <b-button v-if="!isResendActivationApiStatusLoading" variant="success" @click="ok()">
          Resend
        </b-button>

        <b-button v-if="isResendActivationApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Resend...
        </b-button>
      </template>

    </b-modal>

    <!-- Confirm message modal -->
    <b-modal
        v-model="isResendActivationApiStatusLoaded"
        id="modal-resend-activation-confirm"
        title='Confirm'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        @ok="onConfirmOkBtn"
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
        v-model="isResendActivationApiStatusError"
        id="modal-resend-activation-error"
        title='Resend activation error'
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
        Error: {{ userErrorMsg }}
      </p>
    </b-modal>

  </div>
</template>

<script>
  import { validationMixin } from "vuelidate";
  import { required, email } from "vuelidate/lib/validators";
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";

  export default {
    name: "ResendActivationModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          email: '',
        },
      }
    },
    validations: {
      form: {
        email: {
          required,
          email,
        },
      },
    },
    computed: {
      ...mapGetters(['resendActivationApiStatus', 'userErrorMsg']),

      isResendActivationApiStatusLoading() {
        return +this.resendActivationApiStatus === apiStatusList.LOADING;
      },

      isResendActivationApiStatusLoaded() {
        return +this.resendActivationApiStatus === apiStatusList.LOADED;
      },

      isResendActivationApiStatusError() {
        return +this.resendActivationApiStatus === apiStatusList.ERROR;
      },
    },
    methods: {
      ...mapActions(['resendActivation']),

      onOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },

      handleSubmit() {
        this.$v.$touch();

        if (!this.isFieldsInvalid()) {
          this.resendActivation(this.form);
        }
      },

      isFieldsInvalid() {
        return Object.keys(this.form).some(key => this.$v.form[key].$invalid);
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

      onConfirmOkBtn() {
        this.resetFormValues();
        this.$store.commit('updateResendActivationApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-resend-activation');
      },

      onErrorRetryBtn() {
        this.resetFormValues();
        this.$store.commit('updateResendActivationApiStatus', apiStatusList.INIT);
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-resend-activation');
      },
    },
  }
</script>

<style scoped>

</style>