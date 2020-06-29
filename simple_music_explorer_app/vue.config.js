module.exports = {
  devServer: {
    hot: true,
    publicPath: '/',
    proxy: {
      '/': {
        target: 'http://127.0.0.1:8000/',
        secure: false,
        changeOrigin: true,
      }
    },
  },
  configureWebpack: {
    devtool: 'source-map',
  },
};