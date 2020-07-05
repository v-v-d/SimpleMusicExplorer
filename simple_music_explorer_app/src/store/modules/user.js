'use strict';
import apiStatusList from "@/store/apiStatusList";

export default {
  actions: {
    getUser(ctx) {
      if (ctx.getters.isToken) {
        ctx.commit('updateGetUserApiStatus', apiStatusList.LOADING);

        fetch('http://127.0.0.1:8000/api/v1/auth/users/me/', {
          headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token'),
          },
        })
          .then(response => {
            switch (response.status) {
              case 200:
              case 401:
                return response.json();
              default:
                throw Error(`${response.status}: ${response.statusText}`);
            }
          })
          .then(data => {
            if (Object.keys(data).includes('detail')) {
              localStorage.removeItem('token');
              ctx.commit('updateSignInApiStatus', apiStatusList.INIT);
              ctx.commit('updateShowSignInModal', true);
              ctx.commit('updateTokenStatus', false);

              const error = Object.values(data).flat().join(', ');
              throw Error(error);
            } else {
              ctx.commit('updateGetUserApiStatus', apiStatusList.LOADED);
              ctx.commit('updateUser', data);
            }
          })
          .catch(error => {
            ctx.commit('updateGetUserApiStatus', apiStatusList.ERROR);
            ctx.commit('updateUserErrorMessage', error.message);
          })
      } else {
        ctx.commit('updateGetUserApiStatus', apiStatusList.ERROR);
        ctx.commit('updateAuthErrorMessage', 'Token is not exists.');
      }
    },
  },
  mutations: {
    updateGetUserApiStatus(state, apiStatus) {
      state.getUserApiStatus = apiStatus;
    },

    updateUser(state, user) {
      state.user = user;
    },

    updateUserErrorMessage(state, errorMessage) {
      state.userErrorMessage = errorMessage;
    },
  },
  state: {
    getUserApiStatus: apiStatusList.INIT,

    user: {},
    userErrorMessage: '',
  },
  getters: {
    getUserApiStatus(state) {
      return state.getUserApiStatus;
    },

    user(state) {
      return state.user;
    },

    isUser(state) {
      return Boolean(Object.keys(state.user).length);
    },

    userErrorMsg(state) {
      return state.userErrorMessage;
    },
  },
};