import api from "@/api";

export default {
  actions: {
    async getUserProfile({ commit }) {
      const response = await api.user.getUser();
      const data = await response.json();
      commit("SET_PROFILE", data);
    },

    async updateUserProfile({ commit }, body) {
      const response = await api.user.updateUser(body);

      if (response.status === 400) {
        console.log("updateUserProfile status === 400");
        return;
      }

      const data = await response.json();
      commit("SET_PROFILE", data);
    },

    async deleteUserProfile({ dispatch, commit }, body) {
      const response = await api.user.deleteUser(body);

      if (response.status === 400) {
        console.log("deleteUserProfile status === 400");
        return;
      }

      const data = await response.json();
      dispatch("auth/removeAccessToken", null, { root: true });
      commit("SET_PROFILE", data);
    },

    async resetUsername(ctx, body) {
      const response = await api.user.resetUsername(body);

      if (response.status === 400) {
        console.log("resetUsername status === 400");
      }
    },

    async resetUsernameConfirm({ getters, commit }, body) {
      const response = await api.user.resetUsernameConfirm(body);

      if (response.status === 400) {
        console.log("resetUsernameConfirm status === 400");
        return;
      }

      const data = await response.json();
      let profile = getters.profile;
      profile["username"] = data["new_username"];
      commit("SET_PROFILE", profile);
    },

    async resetPassword(ctx, body) {
      const response = await api.user.resetPassword(body);

      if (response.status === 400) {
        console.log("resetPassword status === 400");
      }
    },

    async resetPasswordConfirm(ctx, body) {
      const response = await api.user.resetUsernameConfirm(body);

      if (response.status === 400) {
        console.log("resetPasswordConfirm status === 400");
      }
    }
  },

  mutations: {
    SET_PROFILE(state, profile) {
      state.profile = profile;
    }
  },

  state: {
    profile: {}
  },

  getters: {
    getProfile: state => state.profile,
    isProfile: state => Boolean(Object.keys(state.profile).length)
  },

  namespaced: true
};
