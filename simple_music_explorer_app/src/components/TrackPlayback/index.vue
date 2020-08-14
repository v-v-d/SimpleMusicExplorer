<template>
  <div :class="elClass">
    <button
      class="track-playback__button track-playback__button--sound-on icon-sound-on"
    ></button>
    <button
      @click="play"
      class="track-playback__button track-playback__button--play icon-play-circle"
    ></button>
    <button
      @click="pause"
      class="track-playback__button track-playback__button--pause icon-pause-circle"
    ></button>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "track-playback",

  props: {
    track: {
      type: Object,
      required: true
    },
    tracks: {
      type: Array,
      required: true
    }
  },

  computed: {
    ...mapGetters("player", {
      playback: "getPlayback",

      $audioEl: "getAudioEl",
      playStatus: "getPlayStatus",
      loaded: "getLoadedStatus"
    }),

    elClass() {
      const isActiveTrack = this.playback && this.playback === this.track;

      return [
        "track-playback",
        {
          "track-playback--active": isActiveTrack,
          "track-playback--paused": isActiveTrack && !this.playStatus
        }
      ];
    }
  },

  methods: {
    ...mapActions("player", {
      setPlayback: "setPlayback",
      setTracksToPlayer: "setTracks",
      setAudioEl: "setAudioEl",
      changePlayStatus: "changePlayStatus"
    }),

    play() {
      this.setPlayback(this.track);
      this.changePlayStatus(true);
      if (this.loaded) {
        this.$audioEl.play();
      }
      this.setTracksToPlayer(this.tracks);
    },

    pause() {
      this.changePlayStatus(false);
      this.$audioEl.pause();
    }
  }
};
</script>

<style scoped lang="sass">

.track-playback
  .track-playback__button--play
    display: block

  &--active
    &:hover
      .track-playback__button--play,
      .track-playback__button--sound-on
        display: none

      .track-playback__button--pause
        display: block

    .track-playback__button--play,
    .track-playback__button--pause
      display: none

    .track-playback__button--sound-on
      display: block

  &--paused
    &:hover
      .track-playback__button--pause,
      .track-playback__button--sound-on
        display: none

      .track-playback__button--play
        display: block

  &__button
    display: none
    width: 25px
    height: 25px
    color: $c-gray
    font-size: 25px
    line-height: 1
    outline: 0

    &:hover
      color: $c-white

    &--sound-on
      height: 18px
      color: $c-white
      font-size: 18px
</style>
