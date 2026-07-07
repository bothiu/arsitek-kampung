# Template Laporan Endpoint Inventory

Gunakan template ini saat menulis output final dari skill **Arsitek Kampung**.

```md
# Endpoint Inventory

## Summary
- Target:
- Mode:
- Stack:
- Next.js verified:
- Crawl branch used:
- Output generated at:

## Public Pages
- GET /

## API Endpoints
- GET /api/example
- POST /api/example

## Dynamic / Inferred Routes
- GET /resource/{id}

## LinkFinder Discoveries
- /api/internal-search

## Evidence
- Code:
  - path/to/route.file
  - path/to/client/file
- Live:
  - https://example.com/sitemap.xml
  - https://example.com/_next/static/chunks/app.js

## Gaps / Unverified
- endpoint kandidat yang belum punya bukti kuat
- route dinamis yang belum diverifikasi penuh
```

## Catatan Pengisian
- Pisahkan endpoint berdasarkan kategori.
- Jangan campur hasil confirmed dengan inferred tanpa label.
- Untuk hasil dari LinkFinder, mulai dari label `linkfinder-discovered`.
- Kalau crawl dilewati karena target bukan Next.js, tulis alasannya di `Summary` atau `Gaps / Unverified`.
