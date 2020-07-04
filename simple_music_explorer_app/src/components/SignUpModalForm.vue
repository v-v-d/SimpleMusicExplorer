<template>
  <div>
    <b-modal
        id="modal-sign-up"
        scrollable
        title="Sign Up Form"
        @hidden="onHidden"
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

        <b-form-group
            id="input-group-4"
            label="Repeat password:"
            label-for="input-4"
        >
          <b-form-input
              id="input-4"
              v-model="$v.form.password2.$model"
              :state="validateState('password2')"
              aria-describedby="input-live-feedback"
              type="password"
              placeholder="Enter password one more time"
          ></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            Passwords must be the same.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>

      <h5 v-if="!show && authErrorStatus">
        Sending activation email failed. Try to sign up again.
      </h5>

      <h5 v-if="!show && !authErrorStatus" class="msg">Please check your email.</h5>
      <div v-if="!show" class="w-100">
        <b-button
          variant="secondary"
          class="float-right"
          @click="onClose"
        >
          Close
        </b-button>
      </div>

      <template v-slot:modal-footer>
        <p> </p>
      </template>

    </b-modal>
  </div>
</template>

<script>
  import { validationMixin } from "vuelidate";
  import {
    required, minLength, maxLength, email, sameAs, alphaNum
  } from "vuelidate/lib/validators";
  import { mapGetters, mapActions } from 'vuex';

  export default {
    name: "SignUpModalForm",
    mixins: [validationMixin],
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          password2: '',
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
        password2: {
          required,
          sameAsPassword: sameAs('password'),
        },
      },
    },
    computed: mapGetters(['authErrorStatus']),
    methods: {
      ...mapActions(['getToken']),

      onSubmit() {
        if (this.isFieldsValid()) {
          const payload = {
            data: this.form,
            url: '/api/auth/register/',
          }
          this.getToken(payload);
          this.show = false;
        }
      },

      isFieldsValid() {
        return Object.keys(this.form).some(key => !this.$v.form[key].$invalid)
      },

      onReset() {
        this.resetFormValues();
      },
      
      resetFormValues() {
        Object.keys(this.form).forEach(key => {
          if (this.form[key]) {
            this.form[key] = ''
          }
        });

        this.$nextTick(() => {
          this.$v.$reset();
        });
      },

      onHidden() {
        this.resetFormValues();
        this.show = true;
      },

      onClose() {
        this.resetFormValues();
        this.$bvModal.hide('modal-sign-up');
        this.show = true;
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

  .msg {
    text-align: center;
  }
</style>