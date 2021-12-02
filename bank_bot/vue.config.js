module.exports = {
  pluginOptions: {
    'style-resources-loader': {
      preProcessor: 'scss',
      patterns: []
    }
  },
  devServer: {
    proxy: {
        '/api': {
            target: 'http://localhost:8000',
        },
    },
  }
}
