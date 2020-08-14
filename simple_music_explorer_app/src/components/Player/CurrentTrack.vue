<template>
  <!--  <div v-if="playback" class="current-track">-->
  <div class="current-track">
    <div class="current-track__cover">
      <router-link :to="{ name: 'album', params: { id: playback.album } }">
        <img class="current-track__img" :src="playback.album_image" alt="" />
      </router-link>
    </div>

    <div class="current-track__info">
      <router-link
        class="current-track__name"
        :to="{ name: 'album', params: { id: playback.album } }"
      >
        {{ playback.title }}
      </router-link>

      <div class="current-track__artists">
        <router-link
          class="current-track__link"
          :to="{ name: 'artist', params: { id: playback.artist } }"
        >
          {{ playback.artist_name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "current-track",

  computed: mapGetters("player", {
    playback: "getPlayback"
  })
};
</script>

<style lang="sass">

.current-track
  display: flex
  align-items: center

  &__cover
    width: 56px
    min-width: 56px
    height: 56px
    margin: 0 15px

  &__img
    width: 100%

  &__info
    position: relative
    overflow: hidden
    padding-right: 20px
    white-space: nowrap
    text-overflow: ellipsis

    .track-addition
      position: absolute
      right: 0
      top: 2px

  &__name
    color: $c-white
    font-size: 14px

    &:hover
      text-decoration: underline

  &__artists
    overflow: hidden
    white-space: nowrap
    text-overflow: ellipsis
    padding: 5px 0
    font-size: 11px

  &__link
    color: $c-gray

    &:hover
      color: $c-white
      text-decoration: underline
</style>
