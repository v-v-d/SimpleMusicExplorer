<template>
  <div class="player">
    <audio v-show="false" :src="playback.audio_file" preload="auto" />

    <div v-if="isPlayback" class="player__inner">
      <current-track class="player__left" />

      <div class="player__center">
        <player-controls />
        <player-playback />
      </div>

      <div class="player__right">
        <volume-bar />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import VolumeBar from "./VolumeBar";
import CurrentTrack from "./CurrentTrack";
import PlayerControls from "./PlayerControls";
import PlayerPlayback from "./PlayerPlayback";

export default {
  name: "player",

  data() {
    return {
      currentTime: 0
    };
  },

  components: {
    VolumeBar,
    CurrentTrack,
    PlayerControls,
    PlayerPlayback
  },

  computed: {
    ...mapGetters("player", {
      playback: "getPlayback",
      $audioEl: "getAudioEl",
      playStatus: "getPlayStatus"
    }),

    isPlayback() {
      return Object.keys(this.playback).length;
    }
  },

  methods: {
    ...mapActions("player", {
      setAudioEl: "setAudioEl",
      changePlayStatus: "changePlayStatus",
      setDurationSec: "setDurationSec",
      setCurrentTimeSec: "setCurrentTimeSec",
      changeLoadedStatus: "changeLoadedStatus"
    }),

    load() {
      this.setCurrentTimeSec(this.$audioEl.currentTime);
      this.setDurationSec(Math.floor(this.$audioEl.duration));
      this.changeLoadedStatus(true);

      if (this.playStatus) {
        this.$audioEl.play();
      }
    },

    updateAudioTime(event) {
      const updatedTime = Math.floor(event.target.currentTime);

      if (this.currentTime !== updatedTime) {
        this.setCurrentTimeSec(updatedTime);
        this.currentTime = updatedTime;
      }
    },

    init($audioEl) {
      $audioEl.addEventListener("canplay", () => {
        this.load();
      });
      $audioEl.addEventListener("ended", () => {
        this.changePlayStatus(false);
      });
      $audioEl.addEventListener("timeupdate", e => {
        this.updateAudioTime(e);
      });
    }
  },

  mounted() {
    this.setAudioEl(this.$el.querySelectorAll("audio")[0]);
    this.init(this.$audioEl);
  }
};
</script>

<style scoped lang="sass">

.player
  position: fixed
  bottom: 0
  width: 100%
  height: 90px
  z-index: 2
  background: $c-shark

  &__inner
    display: flex
    align-items: center
    height: 100%

  &__left
    width: 30%
    min-width: 180px

  &__right
    display: flex
    justify-content: center
    width: 30%
    min-width: 180px

    .volume-bar
      margin: 0 15px 0 5px

  &__center
    width: 60%
</style>
