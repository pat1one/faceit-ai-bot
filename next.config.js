/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  compress: true,
  poweredByHeader: false,
  
  // TypeScript config
  typescript: {
    ignoreBuildErrors: true,  // Игнорируем ошибки TypeScript при билде
  },

  // ESLint config  
  eslint: {
    ignoreDuringBuilds: true,  // Игнорируем ESLint при билде
  },

  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
  },
};

module.exports = nextConfig;
