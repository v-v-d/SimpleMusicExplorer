import request from "@/api/request";

const userApiRoot = "auth/users/";

export default {
  async getUser() {
    return await request({
      url: `${userApiRoot}me/`,
      authorized: true
    });
  },

  async updateUser(body) {
    return await request({
      url: `${userApiRoot}me/`,
      method: "PATCH",
      body: body,
      authorized: true
    });
  },

  async deleteUser(body) {
    return await request({
      url: `${userApiRoot}me/`,
      method: "DELETE",
      body: body,
      authorized: true
    });
  },

  async resetUsername(body) {
    return await request({
      url: `${userApiRoot}reset_username/`,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async resetUsernameConfirm(body) {
    return await request({
      url: `${userApiRoot}reset_username_confirm/`,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async resetPassword(body) {
    return await request({
      url: `${userApiRoot}reset_password/`,
      method: "POST",
      body: body,
      authorized: true
    });
  },

  async resetPasswordConfirm(body) {
    return await request({
      url: `${userApiRoot}reset_password_confirm/`,
      method: "POST",
      body: body,
      authorized: true
    });
  }
};
