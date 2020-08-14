<template>
  <div class="delete-user-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Delete User
      </template>
      <template slot="body">
        <form>
          <div>
            <label for="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              v-model="form.current_password"
            />
          </div>
        </form>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onDelete">Delete</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "delete-user-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "delete-user-modal",
      form: {
        current_password: ""
      }
    };
  },

  methods: {
    ...mapActions({
      deleteUserProfile: "user/deleteUserProfile",
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

    async onDelete() {
      if (this.validate()) {
        await this.deleteUserProfile(this.form);
        this.hide();
        this.clearForm();
        this.addNotification({
          type: "success",
          message: "Successfully deleted.",
          duration: 3000
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
