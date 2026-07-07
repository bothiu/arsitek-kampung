---
name: arsitek-kampung
description: "Use when the user wants to discover and document website or project endpoints into a markdown inventory using hybrid code inspection and conditional crawling for verified Next.js targets."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [endpoints, routes, nextjs, crawling, inventory, markdown, linkfinder]
    related_skills: [codebase-inspection, public-web-maintenance, systematic-debugging]
---

# Arsitek Kampung

## Overview

Use this skill to build an **endpoint inventory** for a website or project and save the findings as a **markdown report**. The skill is optimized for mixed situations where the user may provide a local codebase, a live website, or both.

The core behavior is **hybrid by default**:
1. inspect code and route definitions first
2. identify the application stack and likely endpoint sources
3. use crawl/browser-style discovery only when that branch is justified
4. merge confirmed and inferred endpoints into a structured markdown file

This skill is intentionally **documentation-focused**, not a pentest or fuzzing playbook. The goal is to map endpoints with evidence and clear confidence labels.

## When to Use

Use this skill when the user says things like:
- "cek endpoint project ini"
- "list semua endpoint website ini"
- "buat inventaris route"
- "cari semua API endpoint"
- "buat file md daftar endpoint"
- "petakan public surface dan route codebase"

Do **not** use this skill for:
- vulnerability scanning
- brute-force endpoint guessing
- load testing
- authentication bypass testing
- security exploitation workflows

## Input Expectations

Typical input:
- a repo path
- a website/domain
- a specific endpoint to start from
- a request like `tolong cek endpoint ini`

Expected output:
- a markdown file containing the endpoint inventory
- grouped findings by source and confidence
- evidence paths/URLs showing where each endpoint came from

## Discovery Modes

### 1. Code mode
Use when the target is mainly a local project/repository.

Primary tools and methods:
- `search_files`
- `read_file`
- `terminal` when route extraction needs stack-aware commands

Typical targets:
- Laravel route files
- Express/Nest routers
- FastAPI/Flask decorators
- Go mux/router registrations
- Next.js `app/api/**/route.*` and `pages/api/**`
- frontend code containing `fetch`, `axios`, `XMLHttpRequest`, or internal API paths

### 2. Crawl mode
Use when the target is mainly a live website and the user wants surface discovery.

**Hard rule:** browser/web crawling tools are allowed only when the target has been verified as a **Next.js application**.

If the site is not verified as Next.js, do **not** escalate into browser crawling for this skill. Fall back to code inspection or lightweight surface checks.

### 3. Hybrid mode
Default mode for this skill.

Workflow:
1. detect stack
2. inspect code routes and endpoint references first
3. if a live target exists and it is verified as Next.js, run the crawl branch
4. merge everything into one markdown report
5. clearly mark which endpoints are confirmed vs inferred

## Next.js Verification Gate

Before using crawl/browser discovery, verify the target is actually Next.js.

### Verify from codebase
Look for one or more of:
- `package.json` dependency on `next`
- `next.config.js`, `next.config.mjs`, or `next.config.ts`
- `app/` directory
- `pages/` directory
- `app/api/**/route.ts|js`
- `pages/api/**`
- files using `generateStaticParams`, `route.ts`, or Next.js conventions

### Verify from live site
Look for one or more of:
- `/_next/` in HTML or asset URLs
- `/_next/static/` assets
- page source or scripts characteristic of Next.js output
- route/data behavior consistent with Next.js app/router patterns

If Next.js is not verified, document that the crawl branch was skipped by policy.

## LinkFinder Rule

For the crawl branch, use **LinkFinder** (`linkfinder.py` from GerbenJavado/LinkFinder) as the JavaScript endpoint extraction tool.

Repository/source:
- `https://github.com/GerbenJavado/LinkFinder`

### Why LinkFinder here
LinkFinder extracts candidate endpoints/paths from JavaScript sources using regex-based parsing. For Next.js targets, this is useful for discovering:
- API paths referenced from client bundles
- route-like strings embedded in scripts
- relative/internal endpoints not obvious from rendered HTML alone

### When to use LinkFinder
Use LinkFinder only when **all** are true:
1. current branch is `crawl` or the crawl phase of `hybrid`
2. target has been verified as Next.js
3. JavaScript bundle or route script URLs are available to inspect

### When not to use LinkFinder
Do not use LinkFinder when:
- the task is code-only
- the target is not verified as Next.js
- the endpoint list is already sufficiently recoverable from route files
- the workflow would become guessy/noisy without clear evidence

### LinkFinder usage pattern
Preferred operator pattern:
1. identify relevant JavaScript URLs or local JS artifacts
2. run LinkFinder against those assets
3. normalize and deduplicate matches
4. classify results as `linkfinder-discovered`, not automatically `confirmed-live`

Treat LinkFinder results as **candidate evidence** unless they are corroborated by route definitions, live behavior, or other concrete sources.

## Endpoint Sources to Inspect

### Code sources
- route definition files
- controller/handler registration
- API client helpers
- service modules with fixed paths
- frontend calls to `fetch`, `axios`, `useSWR`, `graphql`, etc.
- webhook callback definitions
- sitemap generators or path builders

### Live sources
- homepage links
- sitemap.xml
- robots.txt
- JS bundles and route chunks
- navigation, footer, static links
- documented callback or API paths exposed in public pages

## Classification Rules

Every endpoint in the report should be classified.

Recommended labels:
- `confirmed-code` — explicitly defined in route or handler code
- `confirmed-live` — observed directly on the live surface
- `linkfinder-discovered` — extracted from JS via LinkFinder
- `inferred-dynamic` — dynamic route pattern inferred from code conventions
- `unverified` — candidate exists but was not confirmed

Recommended categories:
- `public-page`
- `api`
- `auth`
- `admin`
- `webhook`
- `static-or-support`

## Report Format

Write the inventory to a markdown file.

Recommended structure:

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
- GET /about

## API Endpoints
- GET /api/users
- POST /api/login

## Dynamic / Inferred Routes
- GET /blog/{slug}
- GET /products/{id}

## LinkFinder Discoveries
- /api/search
- /internal/feed

## Evidence
- Code:
  - routes/web.php
  - app/api/users/route.ts
- Live:
  - https://example.com/sitemap.xml
  - https://example.com/_next/static/...

## Gaps / Unverified
- Route family inferred but not live-verified
- Candidate JS endpoint not mapped to route file
```

## Workflow

1. **Identify target scope**
   - repo path, live website, or both

2. **Determine mode**
   - code, crawl, or hybrid
   - default to hybrid when both repo and live target are available

3. **Detect stack first**
   - inspect framework/runtime before choosing extraction strategy

4. **Inspect code sources first**
   - route files
   - handlers/controllers
   - endpoint references in frontend/backend code

5. **Apply Next.js verification gate**
   - if verified and crawl branch is in scope, proceed
   - otherwise skip browser/web crawling and document the skip

6. **Run LinkFinder for the crawl branch**
   - target relevant JS assets
   - collect candidate endpoints
   - deduplicate and classify them separately

7. **Merge and normalize findings**
   - combine route definitions, live URLs, and JS discoveries
   - normalize slashes, query patterns, and duplicates

8. **Write markdown report**
   - include summary, inventory sections, evidence, and gaps

9. **Verify the report**
   - confirm file path
   - confirm categories are present
   - confirm Next.js/crawl decision is documented

## Common Pitfalls

1. Calling the result "all endpoints" when only one discovery source was checked.
2. Using browser/web crawl before verifying the target is Next.js.
3. Treating LinkFinder output as confirmed-live evidence by default.
4. Missing dynamic routes such as `[slug]`, `[id]`, and catch-all segments.
5. Ignoring nested routers or framework-specific route registration.
6. Failing to distinguish public pages from APIs and callbacks.
7. Producing a flat list without evidence paths.
8. Overwriting the markdown report without stating its output path.
9. Skipping JS-based endpoint references in frontend-heavy apps.
10. Letting crawl noise dominate stronger code evidence.

## Verification Checklist

- [ ] Target scope identified (repo, website, or both)
- [ ] Mode chosen and stated in the report
- [ ] Stack detection completed before extraction
- [ ] Code route inspection completed
- [ ] Next.js verification completed before any crawl escalation
- [ ] LinkFinder used only when policy conditions were met
- [ ] Endpoints classified by confidence/source
- [ ] Markdown report written to a clear output path
- [ ] Evidence section includes file paths and/or URLs
- [ ] Unverified findings are explicitly labeled
