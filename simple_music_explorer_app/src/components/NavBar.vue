<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="secondary">
      <b-navbar-brand :to="{ name: 'Index' }" class="logo-link">
        Simple Music Explorer
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input
                @input="changeQuery"
                :value="query"
                size="sm"
                class="mr-sm-2"
                placeholder="Search"
            ></b-form-input>
            <b-button
                @click.stop.prevent="filterAlbums"
                size="sm"
                class="my-2 my-sm-0"
                type="submit"
            >
              Search
            </b-button>
          </b-nav-form>

          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>User</em>
            </template>
            <b-dropdown-item v-if="!isToken" v-b-modal.modal-sign-up>Sign Up</b-dropdown-item>
            <b-dropdown-item v-if="!isToken" v-b-modal.modal-sign-in>Sign In</b-dropdown-item>

            <b-dropdown-item :to="{ name: 'account' }" v-if="isToken">Account</b-dropdown-item>

            <b-dropdown-item v-if="isToken" @click="signOut">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <SignInModalForm/>
    <SignUpModalForm/>
  </div>
</template>

<script>
  import SignInModalForm from './SignInModalForm.vue'
  import SignUpModalForm from './SignUpModalForm.vue'
  import { mapGetters, mapActions } from 'vuex';

  export default {
    name: "NavBar",
    components: {
      SignInModalForm,
      SignUpModalForm,
    },
    computed: mapGetters(['isToken']),
    methods: mapActions(['signOut']),
  }
</script>

<style scoped>
  .logo-link:hover,
  .logo-link:active,
  .logo-link {
    color: unset;
    text-decoration: unset;
  }

</style>