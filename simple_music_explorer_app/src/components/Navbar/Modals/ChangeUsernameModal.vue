<template>
  <div class="change-username-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Change Username
      </template>
      <template slot="body">
        <p>Please confirm that you want to change your username.</p>
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
  name: "change-username-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "change-username-modal"
    };
  },

  computed: mapGetters({ profile: "user/getProfile" }),

  methods: {
    ...mapActions({
      resetUsername: "user/resetUsername",
      addNotification: "notification/add"
    }),

    hide() {
      this.$modal.hide(this.modalName);
    },

    async onChange() {
      await this.resetUsername({ email: this.profile.email });
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
