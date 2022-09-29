const webpack = require('webpack')
const dotenv = require('dotenv')

// this will update the process.env with environment variables in .env file
dotenv.config();

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            'process.env.AWS_ACCESS_KEY_ID': JSON.stringify(process.env.AWS_ACCESS_KEY_ID),
            'process.env.AWS_SECRET_ACCESS_KEY': JSON.stringify(process.env.AWS_SECRET_ACCESS_KEY),
        })
    ],
    resolve: {
        fallback: {
            "fs": false
        },
    }
}
