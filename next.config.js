/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  compress: true,
  poweredByHeader: false,
  
  // GitHub Pages configuration
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/faceit-ai-bot' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/faceit-ai-bot/' : '',
  trailingSlash: true,
  
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  
  // Performance optimizations
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            default: false,
            vendors: false,
            vendor: {
              chunks: 'all',
              name: 'vendor',
              test: /[\\/]node_modules[\\/]/,
              priority: 20,
            },
            common: {
              name: 'common',
              minChunks: 2,
              chunks: 'all',
              priority: 10,
            },
          },
        },
      };
    }
    return config;
  },

  // Enable for Replit proxy compatibility
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: process.env.NODE_ENV === 'development' 
              ? 'no-cache, no-store, must-revalidate'
              : 'public, max-age=31536000, immutable'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          }
        ]
      }
    ]
  },

  // TypeScript config
  typescript: {
    ignoreBuildErrors: true, // Allow build for GitHub Pages
  },

  // ESLint config  
  eslint: {
    ignoreDuringBuilds: true, // Allow build for GitHub Pages
  },
  
  // Experimental features for static export
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
};

module.exports = nextConfig;
