module.exports = {
  devServer: {
    port: 8080
  },

  css: {
    loaderOptions: {
      sass: {
        prependData: "@import ./src/styles/util/util.sass"
      }
    }
  }
};
