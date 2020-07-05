'use strict';
import apiStatusList from "@/store/apiStatusList";

export default {
  actions: {
    getTokenFromLocalStorage(ctx) {
      const token = localStorage.getItem('token');
      if (token) {
        ctx.commit('updateTokenStatus', true);
      }
    },

    signUp(ctx, data) {
      ctx.commit('updateSignUpApiStatus', apiStatusList.LOADING);

      fetch('http://127.0.0.1:8000/api/v1/auth/users/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => {
          if (response.status !== 201) {
            throw Error(`${response.status}: ${response.statusText}`);
          }

          ctx.commit('updateSignUpApiStatus', apiStatusList.LOADED);
          ctx.commit('updateShowSignUpModal', false);
        })
        .catch(error => {
          ctx.commit('updateSignUpApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
        });
    },

    activate(ctx, data) {
      ctx.commit('updateActivateApiStatus', apiStatusList.LOADING);

      fetch('http://127.0.0.1:8000/api/v1/auth/users/activation/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => {
          if (response.status !== 204) {
            throw Error(`${response.status}: ${response.statusText}`);
          }

          ctx.commit('updateActivateApiStatus', apiStatusList.LOADED);
        })
        .catch(error => {
          ctx.commit('updateActivateApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
        });
    },

    signIn(ctx, data) {
      ctx.commit('updateSignInApiStatus', apiStatusList.LOADING);

      fetch('http://127.0.0.1:8000/api/v1/auth/token/login/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => {
          if (!response.ok) {
            throw Error(`${response.status}: ${response.statusText}`);
          }

          return response.json();
        })
        .then(tokenObj => {
          const token = tokenObj['auth_token'];
          localStorage.setItem('token', `Token ${token}`);
          ctx.commit('updateSignInApiStatus', apiStatusList.LOADED);
          ctx.commit('updateShowSignInModal', false);
          ctx.commit('updateTokenStatus', true);

          ctx.dispatch('getUser');
        })
        .catch(error => {
          ctx.commit('updateSignInApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
        });
    },

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
            if (!response.ok) {
              throw Error(`${response.status}: ${response.statusText}`);
            }

            return response.json();
          })
          .then(user => {
            ctx.commit('updateGetUserApiStatus', apiStatusList.LOADED);
            ctx.commit('updateUser', user);
          })
          .catch(error => {
            ctx.commit('updateGetUserApiStatus', apiStatusList.ERROR);
            ctx.commit('updateAuthErrorMessage', error.message);
          })
      } else {
        ctx.commit('updateGetUserApiStatus', apiStatusList.ERROR);
        ctx.commit('updateAuthErrorMessage', 'Token is not exists.');
      }
    },

    signOut(ctx) {
      ctx.commit('updateSignOutApiStatus', apiStatusList.LOADING);

      if (ctx.getters.isToken) {
        fetch('http://127.0.0.1:8000/api/v1/auth/token/logout/', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            'Authorization': localStorage.getItem('token'),
          },
        })
          .then(response => {
            if (response.status !== 204) {
              throw Error(`${response.status}: ${response.statusText}`);
            }

            localStorage.removeItem('token');
            ctx.commit('updateSignOutApiStatus', apiStatusList.LOADED);
            ctx.commit('updateShowSignInModal', true);
            ctx.commit('updateShowSignUpModal', true);
            ctx.commit('updateTokenStatus', false);
            ctx.commit('updateUser', {});
          })
          .catch(error => {
            ctx.commit('updateSignOutApiStatus', apiStatusList.ERROR);
            ctx.commit('updateAuthErrorMessage', error.message);
          });
      } else {
        ctx.commit('updateSignOutApiStatus', apiStatusList.ERROR);
        ctx.commit('updateAuthErrorMessage', 'Token is not exists.');
      }
    },
  },
  mutations: {
    updateSignUpApiStatus(state, apiStatus) {
      state.signUpApiStatus = apiStatus;
    },

    updateActivateApiStatus(state, apiStatus) {
      state.activateApiStatus = apiStatus;
    },

    updateSignInApiStatus(state, apiStatus) {
      state.signInApiStatus = apiStatus;
    },

    updateGetUserApiStatus(state, apiStatus) {
      state.getUserApiStatus = apiStatus;
    },

    updateSignOutApiStatus(state, apiStatus) {
      state.signOutApiStatus = apiStatus;
    },

    updateShowSignInModal(state, showStatus) {
      state.showSignInModal = showStatus;
    },

    updateShowSignUpModal(state, showStatus) {
      state.showSignUpModal = showStatus;
    },

    updateTokenStatus(state, tokenStatus) {
      state.isToken = tokenStatus;
    },

    updateUser(state, user) {
      state.user = user;
    },

    updateAuthErrorMessage(state, errorMessage) {
      state.authErrorMessage = errorMessage;
    },
  },
  state: {
    signUpApiStatus: apiStatusList.INIT,
    activateApiStatus: apiStatusList.INIT,
    signInApiStatus: apiStatusList.INIT,
    getUserApiStatus: apiStatusList.INIT,
    signOutApiStatus: apiStatusList.INIT,

    showSignInModal: true,
    showSignUpModal: true,

    isToken: false,
    user: {},
    authErrorMessage: '',
  },
  getters: {
    signUpApiStatus(state) {
      return state.signUpApiStatus;
    },

    activateApiStatus(state) {
      return state.activateApiStatus;
    },

    signInApiStatus(state) {
      return state.signInApiStatus;
    },

    getUserApiStatus(state) {
      return state.getUserApiStatus;
    },

    signOutApiStatus(state) {
      return state.signOutApiStatus;
    },

    showSignInModal(state) {
      return state.showSignInModal;
    },

    showSignUpModal(state) {
      return state.showSignUpModal;
    },

    isToken(state) {
      return state.isToken;
    },

    user(state) {
      return state.user;
    },

    isUser(state) {
      return Boolean(Object.keys(state.user).length);
    },

    authErrorMsg(state) {
      return state.authErrorMessage;
    },
  },
};