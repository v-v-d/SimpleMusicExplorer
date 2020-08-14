<template>
  <div v-if="user" class="navbar-nav">
    <div class="navbar-nav__item">
      {{ isUser ? user.username : "Menu" }}
      <button class="navbar-nav__icon" @click="onClick">
        <icon name="chevron-down" />
      </button>
    </div>
    <transition name="fade">
      <ul class="navbar-nav__dropdown" v-show="isVisible" v-if="!isUser">
        <li class="navbar-nav__list-item" @click="$modal.show('sign-up-modal')">
          Sign Up
        </li>
        <li class="navbar-nav__list-item" @click="$modal.show('sign-in-modal')">
          Sign In
        </li>
        <li
          class="navbar-nav__list-item"
          @click="$modal.show('resend-activation-modal')"
        >
          Resend Activation
        </li>
      </ul>

      <ul class="navbar-nav__dropdown" v-show="isVisible" v-if="isUser">
        <li
          class="navbar-nav__list-item"
          @click="$modal.show('update-user-modal')"
        >
          Update User
        </li>
        <li
          class="navbar-nav__list-item"
          @click="$modal.show('delete-user-modal')"
        >
          Delete User
        </li>
        <li
          class="navbar-nav__list-item"
          @click="$modal.show('change-username-modal')"
        >
          Change Username
        </li>
        <li
          class="navbar-nav__list-item"
          @click="$modal.show('change-password-modal')"
        >
          Change Password
        </li>
        <li class="navbar-nav__list-item" @click="signOut">
          Sign Out
        </li>
      </ul>
    </transition>

    <sign-up-modal />
    <sign-in-modal />
    <resend-activation-modal />
    <update-user-modal />
    <delete-user-modal />
    <change-username-modal />
    <change-password-modal />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import SignUpModal from "./Modals/SignUpModal";
import SignInModal from "./Modals/SignInModal";
import ResendActivationModal from "./Modals/ResendActivationModal";
import UpdateUserModal from "./Modals/UpdateUserModal";
import DeleteUserModal from "./Modals/DeleteUserModal";
import ChangeUsernameModal from "./Modals/ChangeUsernameModal";
import ChangePasswordModal from "./Modals/ChangePasswordModal";

export default {
  name: "navbar-nav",

  components: {
    SignUpModal,
    SignInModal,
    ResendActivationModal,
    UpdateUserModal,
    DeleteUserModal,
    ChangeUsernameModal,
    ChangePasswordModal
  },

  data() {
    return {
      isVisible: false
    };
  },

  computed: {
    ...mapGetters({
      user: "user/getProfile",
      isUser: "user/isProfile"
    })
  },

  methods: {
    ...mapActions("auth", ["signOut"]),

    clickOutEvent: function(e) {
      const $dropdown = this.$el.children[0];
      if (e.target !== $dropdown && !$dropdown.contains(e.target)) {
        this.close();
      }
    },

    onClick() {
      this.isVisible = !this.isVisible;

      if (this.isVisible) {
        setTimeout(
          () => document.addEventListener("click", this.clickOutEvent),
          100
        );
      } else {
        this.close();
      }
    },

    close: function() {
      this.isVisible = false;
      document.removeEventListener("click", this.clickOutEvent);
    }
  }
};
</script>

<style scoped lang="sass">

.navbar-nav
  position: relative
  z-index: 10

  &__item
    display: flex
    align-items: center
    height: 40px

  &__link
    color: $c-white
    font-size: 13px

    &:hover
      text-decoration: underline

  &__icon
    margin: 0 6px
    color: $c-white
    font-size: 12px
    line-height: 0
    outline: none
    cursor: pointer

  &__dropdown
    font:
      size: 13px
      weight: normal
    background: $c-tundora
    box-shadow: -2px 2px 5px 0 rgba(0, 0, 0, .75)

  &__list-item
    padding: 10px
    cursor: pointer

    &:hover
      background: $c-black-light

  .fade-enter-active,
  .fade-leave-active
    transition: opacity .3s

  .fade-enter,
  .fade-leave-to
    opacity: 0
</style>
