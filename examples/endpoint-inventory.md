# Endpoint Inventory

## Summary
- Target: /opt/data/workspace/demo-next-app + https://demo.example.com
- Mode: hybrid
- Stack: Next.js 15 + Route Handlers
- Next.js verified: yes
- Crawl branch used: yes
- Output generated at: 2026-07-07 17:00 UTC

## Public Pages
- GET /
- GET /about
- GET /pricing
- GET /blog

## API Endpoints
- GET /api/users
- POST /api/login
- POST /api/contact
- GET /api/blog

## Dynamic / Inferred Routes
- GET /blog/{slug}
- GET /products/{id}

## LinkFinder Discoveries
- /api/search
- /api/revalidate
- /internal/feed

## Evidence
- Code:
  - app/api/users/route.ts
  - app/api/login/route.ts
  - app/blog/[slug]/page.tsx
  - lib/api-client.ts
- Live:
  - https://demo.example.com/sitemap.xml
  - https://demo.example.com/_next/static/chunks/app.js

## Gaps / Unverified
- `/api/revalidate` muncul di JS bundle tapi route definitif belum ditemukan.
- `/internal/feed` muncul dari bundle frontend dan belum terkonfirmasi sebagai endpoint live.
