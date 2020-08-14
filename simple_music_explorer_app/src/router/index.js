import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store";

import AlbumView from "@/views/Album";
import ArtistView from "@/views/Artist";
import BrowseView from "@/views/Browse";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    redirect: {
      name: "browse"
    }
  },

  {
    path: "/browse",
    name: "browse",
    component: BrowseView
  },

  {
    path: "/album/:id",
    name: "album",
    component: AlbumView,
    props: true
  },

  {
    path: "/artist/:id",
    name: "artist",
    component: ArtistView,
    props: true
  },

  {
    path: "*",
    beforeEnter: function(to, from, next) {
      store.dispatch("app/notFoundPage", true);
      next();
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
