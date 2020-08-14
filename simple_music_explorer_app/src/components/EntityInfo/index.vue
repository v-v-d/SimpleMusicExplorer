<template>
  <div class="entity-info">
    <div class="entity-info__cover">
      <img
        v-if="coverImg"
        class="entity-info__cover-img"
        :src="coverImg"
        alt="cover"
      />
      <icon v-else class="entity-info__cover-icon" name="music" />
    </div>

    <div class="entity-info__info">
      <div class="entity-info__type">{{ type }}</div>
      <h2 class="entity-info__name">{{ title }}</h2>
      <div v-if="genre" class="entity-info__desc">Genre: {{ genre }}</div>
      <p v-if="description" class="entity-info__desc">{{ description }}</p>
      <p v-if="date" class="entity-info__desc">Release date: {{ date }}</p>

      <div v-if="artist" class="entity-info__artist">
        By
        <router-link
          class="entity-info__link"
          :to="{ name: 'artist', params: { id: artist.id } }"
        >
          {{ artist.name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "entity-info",

  props: {
    coverImg: {
      type: String,
      required: false
    },
    type: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    genre: {
      type: String,
      required: false
    },
    description: {
      type: String,
      required: false
    },
    date: {
      type: String,
      required: false
    },
    price: {
      type: String,
      required: false
    },
    artist: {
      type: Object,
      required: false
    }
  }
};
</script>

<style scoped lang="sass">

.entity-info
  display: flex
  position: relative
  padding: 15px
  font-size: 12px

  &--editable
    .entity-info__cover
      &:hover
        > .entity-info__cover-icon
          display: none

        .entity-info__cover-hover
          display: block

  &__cover
    position: relative
    width: 40%
    min-width: 150px
    max-width: 200px
    max-height: 200px
    background: $c-mine-shaft
    box-shadow: 2px 2px 10px 3px rgba(0, 0, 0, .4)

  &__cover-img
    position: relative
    z-index: 2
    width: 100%
    height: 100%

  &__cover-icon
    +absolute-center
    width: 40%
    height: 40%

  &__cover-hover
    display: none
    position: absolute
    top: 0
    z-index: 10
    width: 100%
    height: 100%
    background: rgba(0, 0, 0, 0.7)
    cursor: pointer

  &__info
    display: flex
    flex-direction: column
    justify-content: flex-end
    width: 60%
    padding: 15px 15px 0

  &__type
    font-size: 11px
    text-transform: uppercase

  &__name
    margin: 10px 0
    font-size: 30px

  &__desc
    color: $c-gray

  &__artist
    color: $c-gray

  &__link,
  a
    color: $c-white

    &:hover
      text-decoration: underline
</style>
