<template>
  <div>
    <b-modal
        id="modal-delete-user"
        scrollable
        title="Enter password for delete confirmation."
        @hidden="resetFormValues"
        @cancel="resetFormValues"
        @ok="onOk"
    >
      <b-form @submit.stop.prevent="handleSubmit">

        <!-- Password input -->
        <b-form-group
            id="input-group-2"
            label="Password:"
            label-for="input-2"
        >
          <b-form-input
              id="input-2"
              v-model="$v.form.current_password.$model"
              :state="validateState('current_password')"
              type="password"
              placeholder="Enter current password"
          ></b-form-input>
        </b-form-group>

      </b-form>

      <!-- Customized modal buttons -->
      <template v-slot:modal-footer="{ ok, cancel }">
        <!-- Emulate built in modal footer ok and cancel button actions -->
        <b-button @click="cancel()">
          Cancel
        </b-button>

        <b-button v-if="!isDeleteUserApiStatusLoading" variant="danger" @click="ok()">
          Delete
        </b-button>

        <b-button v-if="isDeleteUserApiStatusLoading" variant="secondary" disabled>
          <b-spinner small/>
          Delete...
        </b-button>
      </template>

    </b-modal>

    <!-- Success message modal -->
    <b-modal
        v-model="isDeleteUserApiStatusLoaded"
        id="modal-delete-user-success"
        title='Success'
        size='sm'
        centered
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        @ok="onSuccessOkBtn"
    >
      <p class="my-4">
        Success.
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
        v-model="isDeleteUserApiStatusError"
        id="modal-delete-user-error"
        title='Change user info error'
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
  import { required } from "vuelidate/lib/validators";
  import { mapGetters, mapActions } from 'vuex';
  import apiStatusList from "@/store/apiStatusList";

  export default {
    name: "PatchUserModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          current_password: '',
        },
      }
    },
    validations: {
      form: {
        current_password: {
          required,
        },
      },
    },
    computed: {
      ...mapGetters(['deleteUserApiStatus', 'userErrorMsg']),

      isDeleteUserApiStatusLoading() {
        return +this.deleteUserApiStatus === apiStatusList.LOADING;
      },

      isDeleteUserApiStatusLoaded() {
        return +this.deleteUserApiStatus === apiStatusList.LOADED;
      },

      isDeleteUserApiStatusError() {
        return +this.deleteUserApiStatus === apiStatusList.ERROR;
      },
    },
    methods: {
      ...mapActions(['deleteUser']),

      onOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },

      handleSubmit() {
        this.$v.$touch();

        if (!this.isFieldsInvalid()) {
          this.deleteUser(this.form);
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

      onSuccessOkBtn() {
        this.resetFormValues();
        this.$store.commit('updateDeleteUserApiStatus', apiStatusList.INIT);
        this.$bvModal.hide('modal-delete-user');
      },

      onErrorRetryBtn() {
        this.resetFormValues();
        this.$store.commit('updateDeleteUserApiStatus', apiStatusList.INIT);
      },

      onErrorCancelBtn() {
        this.$bvModal.hide('modal-delete-user');
      },
    },
  }
</script>

<style scoped>

</style>