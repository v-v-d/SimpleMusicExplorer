<template>
  <div class="sign-up-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Sign Up
      </template>
      <template slot="body">
        <form>
          <div>
            <label for="username">Username</label>
            <input
              id="username"
              name="username"
              placeholder="enter your username"
              v-model="form.username"
              maxlength="100"
            />
          </div>
          <div>
            <label for="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="example@mail.com"
              v-model="form.email"
              maxlength="100"
            />
          </div>
          <div>
            <label for="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="enter password"
              v-model="form.password"
              maxlength="100"
            />
          </div>
          <div>
            <label for="re_password">Repeat password</label>
            <input
              id="re_password"
              name="re_password"
              type="password"
              placeholder="enter password one more time"
              v-model="form.re_password"
              maxlength="100"
            />
          </div>
        </form>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onSignUp">Sign Up</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "sign-up-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "sign-up-modal",
      form: {
        username: "",
        email: "",
        password: "",
        re_password: ""
      }
    };
  },

  methods: {
    ...mapActions({
      signUp: "auth/signUp",
      addNotification: "notification/add"
    }),

    hide() {
      this.$modal.hide(this.modalName);
    },

    clearForm() {
      Object.keys(this.form).forEach(key => {
        if (this.form[key]) {
          this.form[key] = "";
        }
      });
    },

    validate() {
      let valid = true;

      Object.keys(this.form).forEach(key => {
        if (!this.form[key]) {
          this.addNotification({
            type: "error",
            message: "All fields are required.",
            duration: 3000
          });

          return false;
        }
      });

      return valid;
    },

    async onSignUp() {
      if (this.validate()) {
        await this.signUp(this.form);
        this.hide();
        this.clearForm();
        this.addNotification({
          type: "success",
          message: "Please check your email.",
          duration: 0
        });
      }
    }
  },

  created() {
    this.clearForm();
  }
};
</script>

<style lang="sass"></style>
