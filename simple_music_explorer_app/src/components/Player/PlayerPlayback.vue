<template>
  <div class="player-playback">
    <div class="player-playback__time">
      {{ currentTimeSec | secToHHMMSS }}
    </div>
    <div class="player-playback__progress-bar">
      <vue-slider
        ref="slider"
        :value="currentTimeSec"
        @drag-end="onDragEnd"
        :max="durationSec"
        :dot-size="15"
        :drag-on-click="true"
        :process-style="{ background: '#1db954' }"
        :bg-style="{ background: '#737575' }"
      />
    </div>
    <div class=" player-playback__time">
      {{ durationSec | secToHHMMSS }}
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "player-player-playback",

  computed: mapGetters("player", {
    $audioEl: "getAudioEl",
    durationSec: "getDurationSec",
    currentTimeSec: "getCurrentTimeSec",
    playStatus: "getPlayStatus"
  }),

  methods: {
    ...mapActions("player", {
      changeAudioCurrentTime: "changeCurrentTimeSec"
    }),

    onDragEnd() {
      this.changeAudioCurrentTime(this.$refs.slider.getValue());
    }
  }
};
</script>

<style lang="sass">

.player-playback
  display: flex
  width: 100%

  &__time
    min-width: 40px
    margin: 0 10px 0 10px

  &__progress-bar
    width: 100%
</style>
