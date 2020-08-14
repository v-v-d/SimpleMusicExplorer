export default {
  actions: {
    setTracks({ commit }, tracks) {
      commit("TRACKS_SET", tracks);
    },

    setPlayback({ commit }, playback) {
      commit("PLAYBACK_SET", playback);
    },

    changePlayStatus({ commit }, status) {
      commit("PLAY_STATUS_SET", status);
    },

    setAudioEl({ commit }, element) {
      commit("AUDIO_EL_SET", element);
    },

    setDurationSec({ commit }, data) {
      commit("DURATION_SET", data);
    },

    setCurrentTimeSec({ commit }, data) {
      commit("CURRENT_TIME_SET", data);
    },

    changeCurrentTimeSec({ commit }, data) {
      commit("CURRENT_TIME_CHANGE", data);
    },

    changeLoadedStatus({ commit }, status) {
      commit("LOADED_STATUS_CHANGE", status);
    }
  },

  mutations: {
    TRACKS_SET(state, tracks) {
      state.tracks = tracks;
    },

    PLAYBACK_SET(state, playback) {
      state.playback = playback;
    },

    PLAY_STATUS_SET(state, status) {
      state.playing = status;
    },

    AUDIO_EL_SET(state, $element) {
      state.$audioEl = $element;
    },

    DURATION_SET(state, data) {
      state.durationSec = data;
    },

    CURRENT_TIME_SET(state, data) {
      state.currentTimeSec = data;
    },

    CURRENT_TIME_CHANGE(state, time) {
      state.$audioEl.currentTime = time;
    },

    LOADED_STATUS_CHANGE(state, status) {
      state.loaded = status;
    }
  },

  state: {
    tracks: [],
    playback: {},

    $audioEl: null,
    playing: false,
    durationSec: 0,
    currentTimeSec: 0,
    loaded: false
  },

  getters: {
    getTracks: state => state.tracks,
    getPlayback: state => state.playback,
    getPlayStatus: state => state.playing,
    getAudioEl: state => state.$audioEl,
    getDurationSec: state => state.durationSec,
    getCurrentTimeSec: state => state.currentTimeSec,
    getLoadedStatus: state => state.loaded
  },

  namespaced: true
};
