import api from "@/api";

export default {
  actions: {
    getAccessToken: () => localStorage.getItem("token"),

    removeAccessToken({ commit }) {
      localStorage.removeItem("token");
      commit("SET_ACCESS_TOKEN", "");
    },

    async signUp(ctx, body) {
      const response = await api.auth.signUp(body);

      if (response.status === 400) {
        console.log("signUp status === 400");
      }
    },

    async activate(body) {
      const response = await api.auth.activate(body);

      if (response.status === 400 || response.status === 403) {
        console.log("activate status === 400 or 403");
      }
    },

    async resendActivation(ctx, body) {
      const response = await api.auth.resendActivation(body);

      if (response.status === 400) {
        console.log("resendActivation status === 400");
      }
    },

    async signIn({ commit, dispatch }, body) {
      const response = await api.auth.signIn(body);

      if (response.status === 400) {
        console.log("signIn status === 400");
        return;
      }

      const data = await response.json();
      const token = `Token ${data["auth_token"]}`;
      localStorage.setItem("token", token);
      commit("SET_ACCESS_TOKEN", token);
      dispatch("user/getUserProfile", null, { root: true });
    },

    async signOut({ commit, dispatch }) {
      await api.auth.signOut();
      dispatch("auth/removeAccessToken", null, { root: true });
      commit("user/SET_PROFILE", {}, { root: true });
    }
  },

  mutations: {
    SET_ACCESS_TOKEN(state, token) {
      state.accessToken = token;
    }
  },

  state: {
    accessToken: ""
  },

  getters: {
    getAccessToken: state => state.accessToken
  },

  namespaced: true
};
