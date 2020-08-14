export default {
  actions: {
    add({ commit, dispatch }, notification) {
      commit("NOTIFICATION_ADD", notification);

      if (notification.duration > 0) {
        setTimeout(() => {
          dispatch("remove", notification);
        }, notification.duration);
      }
    },

    remove({ commit }, notification) {
      commit("NOTIFICATION_REMOVE", notification);
    }
  },

  mutations: {
    NOTIFICATION_ADD(state, data) {
      state.notifications.push(data);
    },

    NOTIFICATION_REMOVE(state, data) {
      const index = state.notifications.indexOf(data);
      state.notifications.splice(index, 1);
    }
  },

  state: {
    notifications: []
  },

  getters: {
    getNotifications: state => state.notifications
  },

  namespaced: true
};
