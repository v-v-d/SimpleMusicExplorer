<template>
  <div class="sign-in-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Sign In
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
            <label for="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              v-model="form.password"
              maxlength="100"
            />
          </div>
        </form>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onSignIn">Sign In</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "sign-in-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "sign-in-modal",
      form: {
        username: "",
        password: ""
      }
    };
  },

  methods: {
    ...mapActions({
      signIn: "auth/signIn",
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

    async onSignIn() {
      if (this.validate()) {
        await this.signIn(this.form);
        this.hide();
        this.clearForm();
      }
    }
  },

  created() {
    this.clearForm();
  }
};
</script>

<style lang="sass"></style>
