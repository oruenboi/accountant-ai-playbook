---
name: ai-visibility-audit
description: Run a repeatable AI visibility audit for a website and produce a prioritized action report. Use when a user asks whether their business appears in ChatGPT/Gemini/Copilot, asks for GEO/AI citation readiness checks, requests llms.txt/schema/robots/crawlability review, or wants an implementation-ready SEO-for-AI gap list.
---

# AI Visibility Audit

## Overview
Run a fast, structured audit that checks AI crawler access, crawlable content, schema coverage, and content readiness signals. Output an executive summary, evidence, and prioritized fixes.

## Quick Start
1. Run the script:
   - `python scripts/audit_site.py https://example.com --markdown`
2. Use results to create a scorecard and priority fixes.
3. If the user asks for implementation, convert top issues into concrete code/content tasks.

## Audit Workflow

### 1) Technical Reachability
Check:
- `robots.txt` exists and allows major AI bots (GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, ClaudeBot, PerplexityBot)
- `sitemap.xml` exists
- `llms.txt` exists
- HTTPS is enabled
- baseline response time

Use:
- `python scripts/audit_site.py <url> --markdown`
- manual verification with `curl` for any unexpected result

### 2) Crawlable Content Risk
Determine whether non-JS bots can extract meaningful content:
- raw HTML word count
- H1 presence
- lists/tables presence
- question-heading signal (`<h2>...?</h2>`)
- `<noscript>` fallback presence

Red flag:
- raw HTML word count is very low (<250) or H1 missing.

### 3) Entity & Schema Coverage
Check high-impact schema types:
- Organization
- FAQPage
- Person
- BreadcrumbList

If missing, list exact type and where to add it.

### 4) Content Readiness Signals
Evaluate practical GEO signals:
- depth (target 1,200+ words on key commercial pages)
- citations language (“according to”, “data from”, “research by”)
- non-promotional explanatory sections
- media presence (images/video)
- clear first-150-words answer block

### 5) Competitive Prompt Pack (manual)
Use `references/prompt-pack.md` and test across available AI products. Capture:
- Mentioned brands/domains
- Whether user brand appears
- Query classes where visibility fails (direct/problem/use-case)

## Output Format
Always provide:
1. **Executive summary** (1 paragraph)
2. **Top 5 issues** (impact-ordered)
3. **Evidence table** (metric, observed, target, status)
4. **Fix plan** (quick wins in 24h, medium in 1 week, strategic in 30 days)

Keep recommendations implementation-ready (file names, schema types, example heading rewrites).

## Resources

### scripts/
- `scripts/audit_site.py`: Generates JSON/markdown technical AI visibility baseline from public pages.

### references/
- `references/prompt-pack.md`: Reusable query set for ChatGPT/Gemini/Copilot visibility checks.
