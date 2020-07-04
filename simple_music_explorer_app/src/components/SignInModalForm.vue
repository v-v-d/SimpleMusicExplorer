<template>
  <div>
    <b-modal
        id="modal-sign-in"
        scrollable
        title="Sign In Form"
        @hidden="resetFormValues"
    >
      <b-form @submit.stop.prevent="onSubmit" @reset.stop.prevent="onReset" v-if="show">
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

        <b-form-group
            id="input-group-3"
            label="Password:"
            label-for="input-3"
        >
          <b-form-input
              id="input-3"
              v-model="$v.form.password.$model"
              :state="validateState('password')"
              type="password"
              placeholder="Enter password"
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>

      <template v-slot:modal-footer>
        <p> </p>
      </template>

    </b-modal>
  </div>
</template>

<script>
  import { validationMixin } from "vuelidate";
  import { required, minLength } from "vuelidate/lib/validators";
  import { mapActions } from 'vuex';

  export default {
    name: "SignInModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          username: '',
          password: '',
        },
        show: true,
      }
    },
    validations: {
      form: {
        username: {
          required,
          minLength: minLength(3),
        },
        password: {
          required,
        },
      },
    },
    methods: {
      ...mapActions(['getToken']),

      onSubmit() {
        if (this.isFieldsValid()) {
          const payload = {
            data: this.form,
            url: '/api/auth/login/',
          }
          this.getToken(payload);
          this.closeModal();
        }
      },

      isFieldsValid() {
        return Object.keys(this.form).some(key => !this.$v.form[key].$invalid)
      },

      closeModal() {
        if (Object.values(this.form).every(value => value)) {
          this.resetFormValues();
          this.$bvModal.hide('modal-sign-in');
        }
      },

      onReset() {
        this.resetFormValues();
      },

      resetFormValues() {
        Object.keys(this.form).forEach(key => {
          this.form[key] = null;
        });
        this.$nextTick(() => {
          this.$v.$reset();
        });
      },

      validateState(key) {
        const { $dirty, $error } = this.$v.form[key];
        return $dirty ? !$error : null;
      },
    },
  }
</script>

<style scoped>
  .btn {
    margin-right: 10px !important;
  }
</style>