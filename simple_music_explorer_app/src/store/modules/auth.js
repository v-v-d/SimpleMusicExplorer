'use strict';
import apiStatusList from "@/store/apiStatusList";

export default {
  actions: {
    getTokenFromLocalStorage(ctx) {
      const token = localStorage.getItem('token');
      if (token) {
        ctx.commit('updateToken', token);
      }
    },

    signUp(ctx, data) {
      ctx.commit('updateAuthApiStatus', apiStatusList.LOADING);

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

          ctx.commit('updateAuthApiStatus', apiStatusList.LOADED);
          ctx.commit('updateAuthErrorStatus', false);
        })
        .catch(error => {
          ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    activate(ctx, data) {
      ctx.commit('updateAuthApiStatus', apiStatusList.LOADING);

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

          ctx.commit('updateAuthApiStatus', apiStatusList.LOADED);
          ctx.commit('updateUserActiveStatus', true);
          ctx.commit('updateAuthErrorStatus', false);
        })
        .catch(error => {
          ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    signIn(ctx, data) {
      ctx.commit('updateAuthApiStatus', apiStatusList.LOADING);

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
          ctx.commit('updateToken', token);

          ctx.dispatch('getUser');
        })
        .catch(error => {
          ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    getUser(ctx) {
      if (ctx.getters.isToken) {
        fetch('http://127.0.0.1:8000/api/v1/auth/users/me/', {
          headers: {
            'Content-type': 'application/json',
            'Authorization': ctx.getters.token,
          },
        })
          .then(response => {
            if (!response.ok) {
              throw Error(`${response.status}: ${response.statusText}`);
            }

            return response.json();
          })
          .then(user => {
            ctx.commit('updateAuthApiStatus', apiStatusList.LOADED);
            ctx.commit('updateUser', user);
            ctx.commit('updateAuthErrorStatus', false);
          })
          .catch(error => {
            ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
            ctx.commit('updateAuthErrorMessage', error.message);
            ctx.commit('updateAuthErrorStatus', true);
          })
      } else {
        ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
        const message = 'Token is not exists';
        ctx.commit('updateAuthErrorMessage', message);
        ctx.commit('updateAuthErrorStatus', true);
      }
    },

    signOut(ctx) {
      ctx.commit('updateAuthApiStatus', apiStatusList.LOADING);

      if (ctx.getters.isToken) {
        fetch('http://127.0.0.1:8000/api/v1/auth/token/logout/', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            'Authorization': ctx.getters.token,
          },
        })
          .then(response => {
            if (response.status !== 204) {
              throw Error(`${response.status}: ${response.statusText}`);
            }

            localStorage.removeItem('token');
            ctx.commit('updateToken', '');
            ctx.commit('updateUser', {});
            ctx.commit('updateAuthApiStatus', apiStatusList.LOADED);
            ctx.commit('updateAuthErrorStatus', false);
          })
          .catch(error => {
            ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
            ctx.commit('updateAuthErrorMessage', error.message);
            ctx.commit('updateAuthErrorStatus', true);
          });
      } else {
        ctx.commit('updateAuthApiStatus', apiStatusList.ERROR);
        const message = 'Token is not exists';
        ctx.commit('updateAuthErrorMessage', message);
        ctx.commit('updateAuthErrorStatus', true);
      }
    },
  },
  mutations: {
    updateAuthApiStatus(state, apiStatus) {
      state.authApiStatus = apiStatus;
    },

    updateToken(state, token) {
      state.token = token;
    },

    updateUser(state, user) {
      state.user = user;
    },

    updateUserActiveStatus(state, status) {
      state.userActiveStatus = status;
    },

    updateAuthErrorStatus(state, errorStatus) {
      state.hasAuthError = errorStatus;
    },

    updateAuthErrorMessage(state, errorMessage) {
      state.authErrorMessage = errorMessage;
    },
  },
  state: {
    authApiStatus: apiStatusList.INIT,
    token: '',
    user: {},
    userActiveStatus: false,
    hasAuthError: false,
    authErrorMessage: '',
  },
  getters: {
    authApiStatus(state) {
      return state.authApiStatus;
    },

    token(state) {
      return state.token;
    },

    isToken(state) {
      return Boolean(state.token && typeof state.token !== 'undefined');
    },

    user(state) {
      return state.user;
    },

    isUserActive(state) {
      return state.userActiveStatus;
    },

    isUser(state) {
      return Boolean(Object.keys(state.user).length);
    },

    authErrorStatus(state) {
      return state.hasAuthError;
    },

    authErrorMsg(state) {
      return state.authErrorMessage;
    },
  },
};