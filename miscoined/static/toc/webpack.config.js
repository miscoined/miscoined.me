const path = require("path");

module.exports = {
    resolve: {
        modulesDirectories: ["node_modules", "miscoined/static/toc"]
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    }
}
