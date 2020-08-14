import request from "@/api/request";

const albumApiRoot = "albums/";

export default {
  getAlbumTracks: async albumId =>
    await request({ url: `${albumApiRoot}${albumId}/tracks/` }),

  getTrack: async (albumId, songId) =>
    await request({ url: `${albumApiRoot}${albumId}/tracks/${songId}` }),

  async createTrack(body, albumId) {
    return await request({
      url: `${albumApiRoot}${albumId}/tracks/`,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async updateTrack(albumId, songId, body) {
    return await request({
      url: `${albumApiRoot}${albumId}/tracks/${songId}`,
      method: "PATCH",
      body: body,
      authorized: true
    });
  },

  async deleteTrack(albumId, songId) {
    return await request({
      url: `${albumApiRoot}${albumId}/tracks/${songId}`,
      method: "DELETE",
      authorized: true
    });
  }
};
