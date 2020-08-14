export default {
  actions: {
    notFoundPage({ commit }, status) {
      commit("SET_NOT_FOUND", status);
    },

    async init({ dispatch }) {
      const token = await dispatch("auth/getAccessToken", null, { root: true });
      if (token) {
        dispatch("user/getUserProfile", null, { root: true });
      }
    }
    //
    // init({ dispatch }) {
    //   dispatch("auth/getAccessToken", null, { root: true }).then(token => {
    //     if (token) {
    //       dispatch("user/getUserProfile", null, { root: true });
    //     }
    //   });
    // }
  },

  mutations: {
    SET_NOT_FOUND(state, status) {
      state.notFound = status;
    }
  },

  state: {
    notFound: false
  },

  getters: {
    notFound: state => state.notFound
  },

  namespaced: true
};
