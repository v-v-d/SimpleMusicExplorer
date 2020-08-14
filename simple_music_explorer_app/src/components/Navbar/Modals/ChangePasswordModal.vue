<template>
  <div class="change-password-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Change Password
      </template>
      <template slot="body">
        <p>Please confirm that you want to change your password.</p>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onChange">Change</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "change-password-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "change-password-modal"
    };
  },

  computed: mapGetters({ profile: "user/getProfile" }),

  methods: {
    ...mapActions({
      resetPassword: "user/resetPassword",
      addNotification: "notification/add"
    }),

    hide() {
      this.$modal.hide(this.modalName);
    },

    async onChange() {
      await this.resetPassword({ email: this.profile.email });
      this.hide();
      this.addNotification({
        type: "success",
        message: "Please check your email.",
        duration: 0
      });
    }
  }
};
</script>

<style lang="sass"></style>
