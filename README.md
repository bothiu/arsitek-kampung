# Arsitek Kampung

Skill Hermes untuk **inventaris endpoint website/project** dengan pendekatan:
- hybrid by default
- code inspection dulu
- crawl hanya untuk target **Next.js** yang sudah terverifikasi
- `LinkFinder` dipakai untuk ekstraksi kandidat endpoint dari JavaScript pada cabang crawl

## Cocok dipakai untuk
- memetakan semua route dari codebase
- membuat file markdown daftar endpoint
- menggabungkan hasil code scan + surface live
- audit endpoint Next.js yang route-nya tersebar di route file dan bundle frontend

## Isi repo
- `SKILL.md` — definisi skill utama
- `LICENSE` — lisensi MIT

## Cara install di Hermes

### Opsi 1 — langsung dari raw `SKILL.md`
```bash
hermes skills install https://raw.githubusercontent.com/bothiu/arsitek-kampung/main/SKILL.md
```

### Opsi 2 — via `npx skills`
```bash
npx -y skills add bothiu/arsitek-kampung --skill arsitek-kampung --agent hermes-agent --global --yes
```

## Cara pakai singkat
Contoh trigger:
- `cek endpoint project ini`
- `buat file md daftar endpoint`
- `petakan semua route website ini`

## Catatan policy skill
- browser/web crawl **tidak** dipakai sembarangan
- crawl branch hanya aktif kalau target **terverifikasi Next.js**
- hasil LinkFinder dianggap **candidate evidence** sampai ada bukti tambahan dari code atau live surface

## Repo
- GitHub: https://github.com/bothiu/arsitek-kampung
- Raw skill: https://raw.githubusercontent.com/bothiu/arsitek-kampung/main/SKILL.md
