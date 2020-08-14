<template>
  <div class="player-controls">
    <button
      @click="prev"
      class="player-controls__button icon-previous"
      title="Previous"
    ></button>

    <template v-if="playStatus">
      <button
        @click="pause"
        class="player-controls__button player-controls__button--pause icon-pause-circle"
      ></button>
    </template>
    <template v-else>
      <button
        @click="play"
        class="player-controls__button player-controls__button--play icon-play-circle"
      ></button>
    </template>

    <button
      @click="next"
      class="player-controls__button icon-next"
      title="Next"
    ></button>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "player-controls",

  computed: mapGetters("player", {
    tracks: "getTracks",
    playback: "getPlayback",

    $audioEl: "getAudioEl",
    playStatus: "getPlayStatus"
  }),

  methods: {
    ...mapActions("player", {
      setPlayback: "setPlayback",
      changePlayStatus: "changePlayStatus"
    }),

    getCurrentTrackIdx() {
      return this.tracks.findIndex(track => track.id === this.playback.id);
    },

    next() {
      const currentTrackNumber = this.getCurrentTrackIdx() + 1;
      if (Object.keys(this.tracks).length > currentTrackNumber) {
        const currentTrack = this.tracks[currentTrackNumber];
        this.setPlayback(currentTrack);
      }
    },

    prev() {
      console.log("prev");
      const currentTrackNumber = this.getCurrentTrackIdx();
      if (currentTrackNumber) {
        const currentTrack = this.tracks[currentTrackNumber - 1];
        this.setPlayback(currentTrack);
      }
    },

    pause() {
      this.changePlayStatus(false);
      this.$audioEl.pause();
    },

    play() {
      this.changePlayStatus(true);
      this.$audioEl.play();
    }
  }
};
</script>

<style scoped lang="sass">

.player-controls
  display: flex
  justify-content: center

  &__button
    margin: auto 10px
    color: $c-gray
    font-size: 15px
    cursor: pointer
    outline: none

    &:hover
      color: $c-white

    &--active
      color: $c-green

    &--play,
    &--pause
      font-size: 35px

      &:hover
        color: $c-white
        transform: scale(1.1)
</style>
