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

    patchUser(ctx, data) {
      if (ctx.getters.isToken) {
        ctx.commit('updatePatchUserApiStatus', apiStatusList.LOADING);

        fetch('http://127.0.0.1:8000/api/v1/auth/users/me/', {
          method: 'PATCH',
          body: JSON.stringify(data),
          headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token'),
          },
        })
          .then(response => {
            switch (response.status) {
              case 200:
              case 400:
                return response.json();
              default:
                throw Error(`${response.status}: ${response.statusText}`);
            }
          })
          .then(data => {
            console.log(data);
          })
          .catch(error => {
            ctx.commit('updatePatchUserApiStatus', apiStatusList.ERROR);
            ctx.commit('updateUserErrorMessage', error.message);
          })
      } else {
        ctx.commit('updatePatchUserApiStatus', apiStatusList.ERROR);
        ctx.commit('updateAuthErrorMessage', 'Token is not exists.');
      }
    },

    deleteUser(ctx) {
      console.log(ctx)
    },

    resetUsername(ctx) {
      console.log(ctx)
    },

    resetUsernameConfirm(ctx) {
      console.log(ctx)
    },

    resetPassword(ctx) {
      console.log(ctx)
    },

    resetPasswordConfirm(ctx) {
      console.log(ctx)
    },

  },
  mutations: {
    updateGetUserApiStatus(state, apiStatus) {
      state.getUserApiStatus = apiStatus;
    },

    updatePatchUserApiStatus(state, apiStatus) {
      state.patchUserApiStatus = apiStatus;
    },

    updateDeleteUserApiStatus(state, apiStatus) {
      state.deleteUserApiStatus = apiStatus;
    },

    updateResetUsernameApiStatus(state, apiStatus) {
      state.resetUsernameApiStatus = apiStatus;
    },

    updateResetUsernameConfirmApiStatus(state, apiStatus) {
      state.resetUsernameConfirmApiStatus = apiStatus;
    },

    updateResetPasswordApiStatus(state, apiStatus) {
      state.resetPasswordApiStatus = apiStatus;
    },

    updateResetPasswordConfirmApiStatus(state, apiStatus) {
      state.resetPasswordConfirmApiStatus = apiStatus;
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
    patchUserApiStatus: apiStatusList.INIT,
    deleteUserApiStatus: apiStatusList.INIT,
    resetUsernameApiStatus: apiStatusList.INIT,
    resetUsernameConfirmApiStatus: apiStatusList.INIT,
    resetPasswordApiStatus: apiStatusList.INIT,
    resetPasswordConfirmApiStatus: apiStatusList.INIT,

    user: {},
    userErrorMessage: '',
  },
  getters: {
    getUserApiStatus(state) {
      return state.getUserApiStatus;
    },

    patchUserApiStatus(state) {
      return state.patchUserApiStatus;
    },

    deleteUserApiStatus(state) {
      return state.deleteUserApiStatus;
    },

    resetUsernameApiStatus(state) {
      return state.resetUsernameApiStatus;
    },

    resetUsernameConfirmApiStatus(state) {
      return state.resetUsernameConfirmApiStatus;
    },

    resetPasswordApiStatus(state) {
      return state.resetPasswordApiStatus;
    },

    resetPasswordConfirmApiStatus(state) {
      return state.resetPasswordConfirmApiStatus;
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