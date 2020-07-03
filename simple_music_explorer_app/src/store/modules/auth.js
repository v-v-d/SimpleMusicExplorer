'use strict';

export default {
  actions: {
    getTokenFromLocalStorage(ctx) {
      const token = localStorage.getItem('token');
      if (token) {
        ctx.commit('updateToken', token);
      }
    },

    signUp(ctx, data) {
      fetch('/api/v1/auth/users/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => {
          response.status === 201 ? ctx.commit('updateAuthErrorStatus', false) : throw Error(response.statusText);
        })
        .catch(error => {
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    activate(ctx, data) {
      fetch('/api/v1/auth/users/activation/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => {
          if (response.status !== 204) {
            throw Error(response.statusText);
          }

          ctx.commit('updateUserActiveStatus', true);
          ctx.commit('updateAuthErrorStatus', false);
          // return response.json();
        })
        .catch(error => {
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    signIn(ctx, data) {
      fetch('/api/v1/auth/token/login/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json',
        }
      })
        .then(response => response.ok ? response.json() : throw Error(response.statusText))
        .then(tokenObj => {
          const token = tokenObj['auth_token'];
          localStorage.setItem('token', `Token ${token}`);
          ctx.commit('updateToken', token);

          ctx.dispatch('getUser');
        })
        .catch(error => {
          ctx.commit('updateAuthErrorMessage', error.message);
          ctx.commit('updateAuthErrorStatus', true);
        });
    },

    getUser(ctx) {
      if (ctx.getters.isToken) {
        fetch('/api/v1/auth/users/me/', {
          headers: {
            'Content-type': 'application/json',
            'Authorization': ctx.getters.token,
          },
        })
          .then(response => response.ok ? response.json() : throw Error(response.statusText))
          .then(user => {
            ctx.commit('updateUser', user);
            ctx.commit('updateAuthErrorStatus', false);
          })
          .catch(error => {
            ctx.commit('updateAuthErrorMessage', error.message);
            ctx.commit('updateAuthErrorStatus', true);
          })
      } else {
        const message = 'Token is not exists';
        ctx.commit('updateAuthErrorMessage', message);
        ctx.commit('updateAuthErrorStatus', true);
      }
    },

    signOut(ctx) {
      if (ctx.getters.isToken) {
        fetch('/api/v1/auth/token/logout/', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            'Authorization': ctx.getters.token,
          },
        })
          .then(response => {
            if (response.status !== 204) {
              throw Error(response.statusText);
            }

            localStorage.removeItem('token');
            ctx.commit('updateToken', '');
            ctx.commit('updateUser', {});
            ctx.commit('updateAuthErrorStatus', false);
          })
          .catch(error => {
            ctx.commit('updateAuthErrorMessage', error.message);
            ctx.commit('updateAuthErrorStatus', true);
          });
      } else {
        const message = 'Token is not exists';
        ctx.commit('updateAuthErrorMessage', message);
        ctx.commit('updateAuthErrorStatus', true);
      }
    },
  },
  mutations: {
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
    token: '',
    user: {},
    userActiveStatus: false,
    hasAuthError: false,
    authErrorMessage: '',
  },
  getters: {
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