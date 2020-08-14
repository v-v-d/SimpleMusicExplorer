import Vue from "vue";
import Vuex from "vuex";

import app from "@/store/modules/app";
import auth from "@/store/modules/auth";
import notification from "@/store/modules/notification";
import user from "@/store/modules/user";
import player from "@/store/modules/player";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    app,
    auth,
    notification,
    user,
    player
  }
});
