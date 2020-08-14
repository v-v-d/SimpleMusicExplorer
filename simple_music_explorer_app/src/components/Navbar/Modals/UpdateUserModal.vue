<template>
  <div class="update-user-modal">
    <v-modal :modalName="modalName">
      <template slot="header">
        Update User
      </template>
      <template slot="body">
        <form>
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
        </form>
      </template>
      <template slot="footer">
        <v-button :onClick="hide" :isBlack="true">Cancel</v-button>
        <v-button :onClick="onUpdate">Update</v-button>
      </template>
    </v-modal>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import VButton from "@/components/VButton/index";
import VModal from "@/components/VModal/index";

export default {
  name: "update-user-modal",

  components: {
    VButton,
    VModal
  },

  data() {
    return {
      modalName: "update-user-modal",
      form: {
        email: ""
      }
    };
  },

  methods: {
    ...mapActions({
      updateUserProfile: "user/updateUserProfile",
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

    async onUpdate() {
      if (this.validate()) {
        await this.updateUserProfile(this.form);
        this.hide();
        this.clearForm();
        this.addNotification({
          type: "success",
          message: "Successfully updated.",
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
