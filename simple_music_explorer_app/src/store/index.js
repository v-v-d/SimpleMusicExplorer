import Vue from 'vue';
import Vuex from 'vuex';
import auth from '@/store/modules/auth';
import user from "@/store/modules/user";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    apiRoot: 'http://127.0.0.1:8000/api/v1',
  },
  getters: {
    apiAuth(state) {
      return `${state.apiRoot}/auth`;
    },

    apiMusic(state) {
      return `${state.apiRoot}/music`;
    },

    apiMerch(state) {
      return `${state.apiRoot}/merch`;
    },
  },
  modules: {
    auth,
    user,
  },
});