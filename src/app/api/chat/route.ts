import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    // Connect to Python backend with cache-busting
    const timestamp = Date.now();
    const response = await fetch(`http://localhost:5000/api/chat?t=${timestamp}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
      },
      body: JSON.stringify({ message }),
    });

    if (response.ok) {
      const data = await response.json();
      const response_obj = NextResponse.json({ response: data.response });
      response_obj.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
      response_obj.headers.set('Pragma', 'no-cache');
      response_obj.headers.set('Expires', '0');
      return response_obj;
    } else {
      console.error('Backend error:', response.status, response.statusText);
      return NextResponse.json(
        { error: 'Backend server error' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 