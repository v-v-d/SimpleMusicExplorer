<template>
  <div class="resend-activation-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Resend Activation
      </template>
      <template slot="body">
        <form>
          <div>
            <label for="email">Email</label>
            <input
              id="email"
              name="email"
              placeholder="example@mail.com"
              v-model="form.email"
              maxlength="100"
            />
          </div>
        </form>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onResend">Resend</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "resend-activation-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "resend-activation-modal",
      form: {
        email: ""
      }
    };
  },

  methods: {
    ...mapActions({
      resendActivation: "auth/resendActivation",
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
            message: "Filed is required.",
            duration: 3000
          });

          return false;
        }
      });

      return valid;
    },

    async onResend() {
      if (this.validate()) {
        await this.resendActivation(this.form);
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
