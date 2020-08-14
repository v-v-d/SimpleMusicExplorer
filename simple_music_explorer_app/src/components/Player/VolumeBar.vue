<template>
  <div class="volume-bar">
    <button :class="classesButton" @click="onButtonClick"></button>
    <vue-slider
      class="volume-bar__slider"
      ref="volume"
      v-model="volume"
      @drag-start="onDragStart"
      @callback="onSliderChange"
      @drag-end="onDragEnd"
      tooltip="active"
      :dot-size="15"
      :drag-on-click="true"
      :style="{ 'min-width': '100%' }"
      :process-style="{ background: '#1db954' }"
      :bg-style="{ background: '#737575', width: '80px' }"
    ></vue-slider>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "volume-bar",

  data() {
    return {
      volume: 50,
      tmpVolume: 0,
      dragStartVolume: 0
    };
  },

  computed: {
    ...mapGetters("player", {
      $audioEl: "getAudioEl"
    }),

    classesButton() {
      return [
        "volume-bar__button",
        {
          "icon-sound-on": this.volume,
          "icon-sound-off": !this.volume
        }
      ];
    }
  },

  methods: {
    setVolume(val) {
      this.$audioEl.volume = val / 100;
    },

    onButtonClick() {
      if (this.volume > 0) {
        this.tmpVolume = this.volume;
        this.volume = 0;
      } else {
        this.volume = this.tmpVolume;
      }

      this.setVolume(this.volume);
    },

    onDragStart() {
      this.dragStartVolume = this.$refs.volume.getValue();
    },

    onDragEnd() {
      this.setVolume(this.$refs.volume.getValue());
    },

    onSliderChange(currentValue) {
      const diff = Math.abs(this.dragStartVolume - currentValue);

      if (diff >= 10) {
        this.dragStartVolume = currentValue;
        this.setVolume(currentValue);
      }
    }
  }
};
</script>

<style lang="sass">
.volume-bar
  display: flex
  width: 50%

  &__button
    margin-right: 10px
    color: $c-gray
    cursor: pointer
    outline: none

    &:hover
      color: $c-white
</style>
