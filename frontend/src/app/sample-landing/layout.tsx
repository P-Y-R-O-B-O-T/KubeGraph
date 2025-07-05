'use client'
import React from 'react'

import Image from 'next/image';

interface LayoutProps {
  children: React.ReactNode;
}

const RootLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <Image
        src="/Login-Page-Background.png" // Path to your image
        alt="Login Page Background"
        layout="fill"
        objectFit="cover"
        quality={100}
      />
      <div style={{ position: 'relative', zIndex: 1 }}>{children}</div>
    </div>
  );
};

export default RootLayout;