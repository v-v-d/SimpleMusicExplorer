<template>
  <div class="album-view" v-scroll>
    <div>
      <entity-info
        v-if="album"
        type="album"
        :coverImg="album.image"
        :title="album.title"
        :genre="album.genre"
        :description="album.description"
        :date="album.date"
        :price="album.price"
        :artist="{ name: album.artist_name, id: album.artist }"
      />

      <tracks-list v-if="album && tracks" :tracks="tracks" />
    </div>
  </div>
</template>

<script>
import api from "@/api";
import { mapActions } from "vuex";
import EntityInfo from "@/components/EntityInfo";
import TracksList from "@/components/TracksList";

export default {
  name: "album-view",

  components: {
    EntityInfo,
    TracksList
  },

  props: {
    id: {
      required: true
    }
  },

  data() {
    return {
      album: null,
      tracks: null
    };
  },

  methods: {
    ...mapActions({
      notFoundPage: "app/notFoundPage"
    }),

    async getAlbum(id) {
      try {
        const response = await api.album.getAlbum(id);
        this.album = await response.json();
      } catch (error) {
        this.notFoundPage(true);
      }
    },

    async getAlbumTracks(id) {
      try {
        const response = await api.track.getAlbumTracks(id);
        this.tracks = await response.json();
      } catch (error) {
        this.notFoundPage(true);
      }
    }
  },

  created() {
    this.getAlbum(this.id);
    this.getAlbumTracks(this.id);
  }
};
</script>

<style scoped lang="sass"></style>
