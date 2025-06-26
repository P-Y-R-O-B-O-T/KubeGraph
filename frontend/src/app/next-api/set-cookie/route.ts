import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { token, username } = await req.json();
  const response = NextResponse.json({ success: true });

  // Set HTTP-only cookie for auth token (not accessible to JS)
  response.cookies.set('authToken', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 * 24, // 1 day
  });

  // Set non-HTTP-only cookie for username (accessible to JS)
  response.cookies.set('username', username, {
    // httpOnly omitted, so JS can access
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 * 24, // 1 day
  });

  return response;
}
