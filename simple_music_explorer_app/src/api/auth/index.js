import request from "@/api/request";

const authApiRoot = "auth/users/";
const tokenApiRoot = "auth/token/";

export default {
  async signUp(body) {
    return await request({
      url: authApiRoot,
      method: "POST",
      body: body
    });
  },

  async activate(body) {
    return await request({
      url: `${authApiRoot}activation/`,
      method: "POST",
      body: body
    });
  },

  async resendActivation(body) {
    return await request({
      url: `${authApiRoot}resend_activation/`,
      method: "POST",
      body: body
    });
  },

  async signIn(body) {
    return await request({
      url: `${tokenApiRoot}login/`,
      method: "POST",
      body: body
    });
  },

  async signOut() {
    return await request({
      url: `${tokenApiRoot}logout/`,
      method: "POST",
      authorized: true
    });
  }
};
