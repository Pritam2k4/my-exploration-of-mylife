# XP Hub — Next.js MVP Scaffold

This is a starter scaffold for the XP Hub web app (MVP).

## What's included
- Next.js (frontend + API routes)
- TailwindCSS
- Supabase client integration points
- OpenAI server-side proxy API routes
- Monaco Editor integration in Coding Lab
- Demo mode (localStorage) so you can run without Supabase

## Quickstart (local)
1. Install Node 18+ and npm.
2. Clone/unzip this project.
3. Copy `.env.example` to `.env.local` and fill values (Supabase and OpenAI keys).
4. Install dependencies:

```bash
npm install
```

5. Run dev server:

```bash
npm run dev
```

6. Open http://localhost:3000

## Deploy to Vercel
1. Create a Vercel account and connect your repo.
2. Set environment variables in Vercel using the keys from `.env.example`.
3. Deploy — Vercel will build and deploy the Next.js app.

## Notes
- Keep OpenAI key server-side (used in API routes). Do not expose it in the client.
- Demo mode allows trying the app without Supabase.

