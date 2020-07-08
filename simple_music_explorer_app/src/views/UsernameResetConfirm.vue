<template>
  <div>

    <!-- Main username reset confirm modal -->
    <b-modal
        v-model="isUsernameResetConfirmApiStatusInit"
        id="modal-username-reset-confirm"
        scrollable
        title="Username Reset Confirm Form"
        @show="resetFormValues"
        @hidden="resetFormValues"
        @cancel="resetFormValues"
        @ok="onOk"
    >
      <b-form @submit.stop.prevent="handleSubmit">

        <!-- new_username input -->
        <b-form-group
            id="input-group-1"
            label="New username:"
            label-for="input-1"
        >
          <b-form-input
              id="input-1"
              v-model="$v.form.new_username.$model"
              :state="validateState('new_username')"
              aria-describedby="input-live-feedback"
              placeholder="Enter new username"
              trim
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            This is a required field and must be at least
            {{ $v.form.new_username.$params.minLength.min }} characters.
          </b-form-invalid-feedback>
        </b-form-group>

        <!-- re_new_password input -->
        <b-form-group
            id="input-group-4"
            label="Repeat new username:"
            label-for="input-4"
        >
          <b-form-input
              id="input-4"
              v-model="$v.form.re_new_username.$model"
              :state="validateState('re_new_username')"
              aria-describedby="input-live-feedback"
              placeholder="Enter new username one more time"
              trim
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            Usernames must be the same.
          </b-form-invalid-feedback>
        </b-form-group>

      </b-form>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok, cancel }">
        <b-button @click="cancel()">
          Cancel
        </b-button>

        <b-button v-if="!isUsernameResetConfirmApiStatusLoading" variant="success" @click="ok()">
          Reset
        </b-button>

        <b-button v-if="isUsernameResetConfirmApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Reset...
        </b-button>
      </template>

    </b-modal>

    <!-- Success message modal -->
    <b-modal
        v-model="isUsernameResetConfirmApiStatusLoaded"
        title='Success'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        @ok="redirect"
    >
      <p class="my-4">
        Username resetting succeeded!
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
        v-model="isUsernameResetConfirmApiStatusError"
        id="modal-username-reset-confirm-error"
        title='Username resetting error'
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
        Please retry to reset username. Error: {{ userErrorMsg }}
      </p>
    </b-modal>

  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";
  import router from "@/router";
  import { minLength, required, sameAs } from "vuelidate/lib/validators";
  import { validationMixin } from "vuelidate";

  export default {
    name: "UsernameResetConfirm",
    mixins: [validationMixin],
    props: ['uid', 'token'],
    data() {
      return {
        form: {
          new_username: '',
          re_new_username: '',
        },
      };
    },
    validations: {
      form: {
        new_username: {
          required,
          minLength: minLength(3),
        },
        re_new_username: {
          sameAsPassword: sameAs('new_username'),
        },
      },
    },
    computed: {
      ...mapGetters(['resetUsernameConfirmApiStatus', 'userErrorMsg']),

      isUsernameResetConfirmApiStatusInit() {
        return +this.resetUsernameConfirmApiStatus === apiStatusList.INIT;
      },

      isUsernameResetConfirmApiStatusLoading() {
        return +this.resetUsernameConfirmApiStatus === apiStatusList.LOADING;
      },

      isUsernameResetConfirmApiStatusLoaded() {
        return +this.resetUsernameConfirmApiStatus === apiStatusList.LOADED;
      },

      isUsernameResetConfirmApiStatusError() {
        return +this.resetUsernameConfirmApiStatus === apiStatusList.ERROR;
      },
    },
    methods: {
      ...mapActions(['resetUsernameConfirm']),

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
          this.resetUsernameConfirm(data);
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
        this.$store.commit('updateResetUsernameConfirmApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-username-reset-confirm-error');
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-username-reset-confirm-error');
        this.$bvModal.hide('modal-username-reset-confirm');
        this.redirect();
      },
    },
    created() {
      this.$bvModal.show('modal-username-reset-confirm');
    },
    watch: {
      $route: 'activate',
    },
  }
</script>

<style scoped>

</style>