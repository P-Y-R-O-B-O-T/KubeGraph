"use client";
import { useRouter } from "next/navigation";
import { Button } from '@/components/ui/button';
import Image from 'next/image';

const HomePage: React.FC = () => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await fetch('/next-api/logout', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });
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
            src="/project-logo.png"
            alt="KubeGraph Logo"
            width={50}
            height={50}
            className="mr-2"
          />
          <h1 className="text-3xl font-thin">KubeGraph</h1>
        </div>
        <h2 className="text-2xl font-semibold mb-4 text-center">This is a Ghose Front-Page</h2>
        <div className="flex items-center justify-center mt-4">
          <Button type="button" onClick={handleLogout}>
            Logout
          </Button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;