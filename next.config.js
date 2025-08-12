const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {},
  env: {
    BACKEND_URL: process.env.BACKEND_URL,
  },
  webpack: (config) => {
    // Ensure '@' alias resolves to 'src' during build (especially on Vercel)
    config.resolve.alias['@'] = path.resolve(__dirname, 'src')
    return config
  },
}

module.exports = nextConfig