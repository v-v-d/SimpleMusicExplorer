import request from "@/api/request";

const artistApiRoot = "artists/";

export default {
  getArtists: async () => await request({ url: artistApiRoot }),

  getArtist: async id => await request({ url: `${artistApiRoot}${id}/` }),

  async createArtist(body) {
    return await request({
      url: artistApiRoot,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async updateArtist(id, body) {
    return await request({
      url: `${artistApiRoot}${id}/`,
      method: "PATCH",
      body: body,
      authorized: true
    });
  },

  async deleteArtist(id) {
    return await request({
      url: `${artistApiRoot}${id}/`,
      method: "DELETE",
      authorized: true
    });
  }
};
