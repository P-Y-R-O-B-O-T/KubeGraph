    "use client";
  import React, { useState, useEffect } from 'react';
  import { useRouter } from "next/navigation";
  import Image from 'next/image';

  const SampleLanding: React.FC = () => {
    const router = useRouter();
    // const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;
    const [adminName, setAdminName] = useState('');
    
    useEffect(() => {
    const authToken = localStorage.getItem("authToken"); // Check for the JWT
    setAdminName(localStorage.getItem('username'));
    if (!authToken) {

      router.push("/auth/login");
      alert("You do not have permission to access this page."); // More informative
      return; // Important to return to prevent further checks after redirect
    }
  }, [router]);


  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white p-8 rounded-2xl shadow-md w-96">
        <div className="flex items-center justify-center mb-2">
          <Image
            src="/KubeGraph-logo.png"
            alt="KubeGraph Logo"
            width={50} // Adjust width as needed
            height={50} // Adjust height as needed
            className="mr-2" // Add some margin to the right of the image
          />
          <h1 className="text-3xl font-thin">KubeGraph</h1>
        </div>
        <h2 className="text-2xl font-semibold mb-4 text-center">SampleLanding</h2>
      </div>
    </div>
  );
};

export default SampleLanding;