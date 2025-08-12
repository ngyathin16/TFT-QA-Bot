/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {},
  env: {
    BACKEND_URL: process.env.BACKEND_URL,
  },
}

module.exports = nextConfig