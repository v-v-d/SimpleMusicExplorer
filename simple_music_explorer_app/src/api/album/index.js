import request from "@/api/request";

const albumApiRoot = "albums/";
const artistApiRoot = "artists/";

export default {
  getAlbums: async (limit = 25, offset = 0) =>
    await request({
      url: albumApiRoot,
      params: { limit, offset }
    }),

  getAlbum: async id => await request({ url: `${albumApiRoot}${id}/` }),

  getAlbumSongs: async id =>
    await request({ url: `${albumApiRoot}${id}/tracks/` }),

  getArtistAlbums: async id =>
    await request({ url: `${artistApiRoot}${id}/albums/` }),

  async createAlbum(body) {
    return await request({
      url: `${artistApiRoot}/albums/`,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async updateAlbum(id, body) {
    return await request({
      url: `${albumApiRoot}${id}/`,
      method: "PATCH",
      body: body,
      authorized: true
    });
  },

  async deleteAlbum(id) {
    return await request({
      url: `${albumApiRoot}${id}/`,
      method: "DELETE",
      authorized: true
    });
  }
};
