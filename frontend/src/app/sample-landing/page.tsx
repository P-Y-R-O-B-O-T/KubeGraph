"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from "next/navigation";
import { Button } from '@/components/ui/button';
import Image from 'next/image';

function getCookie(name: string): string | null {
  const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return match ? decodeURIComponent(match.pop() as string) : null;
}

const SampleLanding: React.FC = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');

  useEffect(() => {
    setUsername(getCookie('username') || '');
  }, []);

  const handleLogout = async () => {
    try {
      await fetch('/next-api/logout', {
        method: 'POST',
        credentials: 'include', // Ensure cookies are sent
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setUsername('');
      router.push('/login');
    } catch (err) {
      console.error(err);
      alert('Logout failed. Please try again.');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white p-8 rounded-2xl shadow-md w-96">
        <div className="flex items-center justify-center mb-2">
          <Image
            src="/KubeGraph-logo.png"
            alt="KubeGraph Logo"
            width={50}
            height={50}
            className="mr-2"
          />
          <h1 className="text-3xl font-thin">KubeGraph</h1>
        </div>
        <h2 className="text-2xl font-semibold mb-4 text-center">Sample KubeGraph Landing</h2>
        <h2 className="text-2xl font-semibold mb-4 text-center">{username}</h2>
        <div className="flex items-center justify-center mt-4">
          <Button type="button" onClick={handleLogout}>
            Logout
          </Button>
        </div>
      </div>
    </div>
  );
};

export default SampleLanding;