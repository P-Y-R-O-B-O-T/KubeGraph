"use client";
  import React, { useState } from 'react';
  import { useRouter } from "next/navigation";
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import Image from 'next/image';

  const Login: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

  const router = useRouter();
  // const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;
  const backendApiUrl = "http://localhost:8008";

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (!backendApiUrl) {
        setError("API URL is not configured. Please contact support.");
        setLoading(false);
        return;
    }

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const res = await fetch(`${backendApiUrl}/api/auth/token`, { // Changed to /api/auth/token
        method: "POST",
        headers: { 
            "Content-Type": "application/x-www-form-urlencoded" // Correct header for form data
        },
        body: formData.toString(), // Send as URL-encoded string
      });

      const data = await res.json();

      if (res.ok && data.access_token) { // Check for res.ok and the actual access_token
        localStorage.setItem("authToken", data.access_token); // Store the JWT
        localStorage.setItem("username", username);
        
        localStorage.removeItem("auth"); 

        // Redirect based on access level
        if (data.access_token) {
          router.push("/sample-landing");    
        } else {
            setError("Unknown user role received from server.");
            localStorage.removeItem("authToken");
            localStorage.removeItem("username");
        }
      } else {
        setError(data.detail || "Invalid credentials or login failed.");
      }
    } catch (err) {
      console.error("Login error:", err);
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred.";
      setError(`Login failed: ${errorMessage}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

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
        <h2 className="text-2xl font-semibold mb-4 text-center">Login</h2>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">
              Username:
            </label>
            <Input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
              Password:
            </label>
            <Input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="flex items-center justify-center">
            <Button type="submit">
              Login
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;