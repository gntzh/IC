const CompressionWebpackPlugin = require('compression-webpack-plugin')
const productionGzipExtensions = ['js', 'css']
const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}
const isProd = process.env.NODE_ENV === "production";

const min = isProd ? ".min" : "";
let cdn = {
  js: [
    `https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue${min}.js`,
    "https://cdn.jsdelivr.net/npm/vue-router@3.1.5/dist/vue-router.min.js",
    "https://cdn.jsdelivr.net/npm/vuex@3.1.2/dist/vuex.min.js",
    "https://cdn.jsdelivr.net/npm/axios@0.19.0/dist/axios.min.js",
    "https://cdn.jsdelivr.net/npm/qs@6.9.0/dist/qs.min.js"
  ]
};
module.exports = {
  productionSourceMap: false,
  transpileDependencies: ["vuetify"],

  chainWebpack: config => {
    config.resolve.alias.set("@com", resolve("src/components"));
    config.plugin("html").tap(args => {
      args[0].cdn = cdn;
      args[0].title = "电子元器件管理";
      return args;
    });
  },

  configureWebpack: {
    externals: {
      // jquery: "window.$",
      vue: "Vue",
      "vue-router": "VueRouter",
      vuex: "Vuex",
      axios: "axios",
      qs: "Qs"
    },
    plugins: [
      new CompressionWebpackPlugin({
        filename: '[path].gz[query]',
        algorithm: 'gzip',
        test: new RegExp('\\.(' + productionGzipExtensions.join('|') + ')$'),
        threshold: 10240,
        minRatio: 0.8,
        //删除原始文件只保留压缩后的文件
        // deleteOriginalAssets: true
      })
    ]
  }
};
