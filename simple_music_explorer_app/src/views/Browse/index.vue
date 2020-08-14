<template>
  <div class="albums-view" v-scroll @vScroll="loadMore">
    <entity-header title="Albums & singles" :small="true" />
    <div class="albums-view__inner">
      <media-container>
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
import MediaObject from "@/components/MediaObject";
import EntityHeader from "@/components/EntityHeader";
import MediaContainer from "@/components/MediaContainer";

export default {
  name: "browse",

  components: {
    EntityHeader,
    MediaObject,
    MediaContainer
  },

  data() {
    return {
      albums: {
        limit: 25,
        offset: 0,
        total: 1,
        items: []
      },
      more: null
    };
  },

  methods: {
    async getAlbums() {
      if (this.albums.total > this.albums.offset) {
        const response = await api.album.getAlbums(
          this.albums.limit,
          this.albums.offset
        );
        const albums = await response.json();

        this.albums.offset += this.albums.limit;
        this.albums.total = albums.count;
        this.albums.items.push(...albums.results);

        this.more = false;
      }
    },

    async loadMore(ev) {
      if (this.more) {
        return false;
      }

      if (ev.detail.scrollbarV.percent > 70) {
        this.more = true;
        await this.getAlbums();
      }
    }
  },

  created() {
    this.getAlbums();
  }
};
</script>

<style scoped lang="sass">

.albums-view
  height: calc(100vh - 130px)
</style>
