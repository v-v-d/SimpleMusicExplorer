<template>
  <div v-if="tracks" class="tracks-list">
    <div
      v-for="(track, index) in tracks"
      :key="index"
      class="tracks-list__row"
      :class="isActiveTrack(track)"
    >
      <div class="tracks-list__cell tracks-list__cell--index">
        <span class="tracks-list__cell-index">{{ index + 1 }}</span>
        <track-playback :track="track" :tracks="tracks" />
      </div>

      <div class="tracks-list__cell tracks-list__cell--name">
        {{ `${track.title} - ` }}
        <router-link
          class="tracks-list__link"
          :to="{ name: 'artist', params: { id: track.artist } }"
        >
          {{ track.artist_name }}
        </router-link>
      </div>

      <div class="tracks-list__cell tracks-list__cell--duration">
        {{ track.duration }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import TrackPlayback from "@/components/TrackPlayback";

export default {
  name: "tracks-list",

  components: {
    TrackPlayback
  },

  props: {
    tracks: {
      type: Array,
      required: true
    }
  },

  computed: mapGetters("player", {
    playback: "getPlayback",
    playStatus: "getPlayStatus"
  }),

  methods: {
    isActiveTrack(current) {
      const isActiveTrack = this.playback && this.playback === current;

      return {
        "tracks-list__row--active": isActiveTrack,
        "tracks-list__row--paused": isActiveTrack && !this.playStatus
      };
    }
  }
};
</script>

<style lang="sass">
.tracks-list
  padding: 0 15px

  &__link
    color: $c-gray

    &:hover
      color: $c-white
      text-decoration: underline

  &__row
    position: relative
    display: flex
    min-height: 40px
    color: $c-white
    font-size: 13px
    line-height: 15px
    border-bottom: 1px solid $c-mine-shaft

    &:first-of-type
      border-top: 1px solid $c-mine-shaft

    &:hover
      &:not(.tracks-list__row--active)
        background: $c-mine-shaft
        color: $c-white

      .track-addition__button
        color: $c-white

      .track-playback
        display: block

      .tracks-list__cell-index
        display: none

    &--active
      background: $c-mine-shaft
      color: $c-green

      .tracks-list__cell-index
        display: none

      .track-playback
        display: block !important

  &__cell
    display: flex
    align-items: center

    &:not(:first-of-type)
      margin: 0 8px

    &--index
      margin: 0 5px
      min-width: 35px

    &--playback
      width: 40px

    &--name
      width: 100%

  &__img
    width: 40px
    height: 40px

  &__explicit-label
    padding: 3px
    border: 1px solid $c-gray
    border-radius: 3px
    color: $c-gray
    font-size: 9px
    line-height: 1
    letter-spacing: 1.5px
    text-transform: uppercase

  .track-playback
    display: none
</style>
