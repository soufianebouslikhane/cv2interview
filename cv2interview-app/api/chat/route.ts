import { NextRequest, NextResponse } from 'next/server';

const FASTAPI_BACKEND_URL = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';

export async function POST(req: NextRequest) {
  try {
    const contentType = req.headers.get('content-type');
    let backendResponse;

    if (contentType && contentType.includes('multipart/form-data')) {
      // Handle file upload
      const formData = await req.formData();
      const file = formData.get('file') as Blob | null;

      if (!file) {
        return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
      }

      // Use Blob for file, since File may not be available in Node.js
      const backendFormData = new FormData();
      backendFormData.append('file', file);

      backendResponse = await fetch(`${FASTAPI_BACKEND_URL}/agent/chat`, {
        method: 'POST',
        body: backendFormData,
      });

    } else if (contentType && contentType.includes('application/json')) {
      // Handle JSON requests (for text prompts)
      const body = await req.json();
      backendResponse = await fetch(`${FASTAPI_BACKEND_URL}/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
    } else {
      return NextResponse.json({ error: 'Unsupported Content-Type' }, { status: 415 });
    }

    if (!backendResponse.ok) {
      let errorData;
      try {
        errorData = await backendResponse.json();
      } catch {
        errorData = { detail: await backendResponse.text() };
      }
      return NextResponse.json({ error: errorData.detail || 'Backend error' }, { status: backendResponse.status });
    }

    let data;
    try {
      data = await backendResponse.json();
    } catch {
      data = { result: await backendResponse.text() };
    }
    return NextResponse.json(data);

  } catch (error) {
    console.error('Proxy API error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
    console.error('Proxy API error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
