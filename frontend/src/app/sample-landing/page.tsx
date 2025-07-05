"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from "next/navigation";
import { Button } from '@/components/ui/button';
import Image from 'next/image';

const SampleLanding: React.FC = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [authToken, setAuthToken] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/next-api/me', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setUsername(data.username || ''))
      .catch((err) => {
        setUsername('');
        setError('Failed to load user info');
        console.error('API error:', err, '\nError Caught:', error);
      });
  }, [error]);
  

  useEffect(() => {
    fetch('/next-api/get-token', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setAuthToken(data.authToken || ''))
      .catch((err) => {
        setAuthToken('');
        setError('Failed to load token info');
        console.error('API error:', err, '\nError Caught:', error);
      });
  }, [error]);

  const handleLogout = async () => {
    try {
      await fetch('/next-api/logout', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      });
      setUsername('');
      router.push('/login');
    } catch (err) {
      console.error(err);
      alert('Logout failed. Please try again.');
    }
  };

  // Output is automatically escaped by React, so no manual escaping needed
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white p-8 rounded-2xl shadow-md w-96">
        <div className="flex items-center justify-center mb-2">
          <Image
            src="/project-logo.png"
            alt="KubeGraph Logo"
            width={50}
            height={50}
            className="mr-2"
          />
          <h1 className="text-3xl font-thin">KubeGraph</h1>
        </div>
        <h2 className="text-2xl font-semibold mb-4 text-center">Sample KubeGraph Landing</h2>
        <h2 className="text-2xl font-semibold mb-4 text-center">{username}</h2>
        <h2 className="text-2xl font-semibold mb-4 text-center">{authToken}</h2>
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