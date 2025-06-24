import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
// };

const nextConfig = {
  // You can add other Next.js configurations here, for example:
  // output: 'standalone',

  // This is the part that solves your problem:
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
