module.exports = {
  webpack: function (config, env) {
    return config;
  },
  jest: function (config) {
    return config;
  },
  devServer: function (configFunction) {
    return function (proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);
      config.watchOptions = {
        ignored: [
          '**/public/graph*.png',
          '**/public/user_data.json'
        ]
      };
      return config;
    }
  },
  paths: function (paths, env) {
    return paths;
  },
}
