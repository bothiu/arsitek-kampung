# arsitek-kampung

Hermes skill repository for **Arsitek Kampung**.

This skill is used to discover and document website/project endpoints into a markdown inventory using hybrid code inspection and conditional Next.js crawling.

## Main rules
- Hybrid by default
- Code inspection first
- Crawl branch only after Next.js verification
- LinkFinder is the JS endpoint extraction tool for the crawl branch
- Output must be a markdown endpoint report with evidence and confidence labels

## Files
- `SKILL.md` — main Hermes skill definition
