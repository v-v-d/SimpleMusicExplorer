<template>
  <div class="artist-view" v-scroll @vScroll="loadMore">
    <div class="artist-view__content">
      <entity-info
        v-if="artist"
        :coverImg="artist.image"
        type="Artist"
        :title="artist.name"
        :description="artist.bio"
      />

      <entity-header v-if="albums" title="Albums" :small="true" />
      <media-container v-if="albums">
        <media-object
          v-for="(item, index) in albums.items"
          :key="index"
          :id="item.id"
          :coverImg="item.image"
          :name="item.title"
          :artist="{ name: item.artist_name, id: item.artist }"
          type="album"
        />
      </media-container>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import { mapActions } from "vuex";
import EntityHeader from "@/components/EntityHeader";
import EntityInfo from "@/components/EntityInfo";
import MediaObject from "@/components/MediaObject";
import MediaContainer from "@/components/MediaContainer";

export default {
  name: "artist-view",

  components: {
    EntityHeader,
    EntityInfo,
    MediaObject,
    MediaContainer
  },

  props: ["id"],

  data() {
    return {
      artist: null,
      albums: null
      // isMore: null
    };
  },

  methods: {
    ...mapActions({
      notFoundPage: "app/notFoundPage"
    }),

    initData() {
      this.artist = null;
      this.albums = {
        // limit: 25,
        // offset: 0,
        // total: 1,
        items: []
      };
    },

    async getArtist(artistID) {
      try {
        const response = await api.artist.getArtist(artistID);
        this.artist = await response.json();
      } catch (error) {
        this.notFoundPage(true);
      }
    },

    async getArtistAlbums() {
      const response = await api.album.getArtistAlbums(this.id);
      this.albums.items = await response.json();
      // async getArtistAlbums(artistID) {
      // try {
      //   if (this.albums.total > this.albums.offset) {
      //     const response = await api.album.getArtistAlbums(
      //       this.id,
      //       this.albums.offset,
      //       this.albums.limit
      //     );
      //
      //     this.albums.offset = response.data.offset + this.albums.limit;
      //     this.albums.total = response.data.total;
      //     this.albums.items.push(...response.data.items);
      //     this.isMore = false;
      //   }
      // } catch (e) {
      //   console.log(e);
      // }
    },

    async loadMore() {
      // async loadMore(ev) {
      // if (this.isMore) {
      //   return false;
      // }
      //
      // if (ev.detail.scrollbarV.percent > 70) {
      //   this.isMore = true;
      //   this.getArtistAlbums(this.artistID);
      // }
    },

    init() {
      this.initData();
      this.getArtist(this.id);
      this.getArtistAlbums(this.id);
    }
  },

  watch: {
    $route() {
      this.init();
    }
  },

  created() {
    this.init();
  }
};
</script>

<style scoped lang="sass"></style>
