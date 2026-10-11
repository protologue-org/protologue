# Protologue

A sourced, citable taxonomy of prompting and LLM techniques, built as a static site for **protologue.com**.

- 101 entries in 10 branches, each with a permanent ID (`PTL-0001`), a standalone definition, synonyms, broader/narrower/related links, and primary sources (all arXiv IDs and links checked on 2026-10-10).
- Machine-readable everywhere: schema.org `DefinedTerm` JSON-LD on every page, `llms.txt` and `llms-full.txt`, per-entry `.md` and `.json`, and full exports as JSON, CSV, SKOS JSON-LD and Turtle.
- Citation tooling on every entry: a plain citation, BibTeX, and Google Scholar (Highwire) meta tags.
- Licensed CC BY 4.0, so AI systems and people can reuse it freely with attribution.

## Project layout

| Path | What it is |
|---|---|
| `data/categories.yaml` | The 10 branches |
| `data/terms-*.yaml` | The entries. Edit these to add or change terms. |
| `data/ids.json` | Permanent identifiers. Commit it and never edit existing values. |
| `static/` | CSS, JS, favicon, `robots.txt`, Cloudflare `_headers` and `_redirects` |
| `build.py` | The generator. It writes everything into `site/`. |
| `site/` | The built website, ready to upload |
| `wrangler.jsonc` | Config for deploying with Cloudflare's command-line tool |

Build it locally:

```
pip install pyyaml
python3 build.py
```

## How it's deployed

- **Source:** github.com/protologue-org/protologue (this repository).
- **Hosting:** Cloudflare Pages project `protologue-site`, connected to this repo. Every push to `main` rebuilds and deploys protologue.com automatically.
  - Build command: `pip install -r requirements.txt && python3 build.py`
  - Output directory: `site`
- **Domain:** protologue.com (DNS on Cloudflare; registration at GoDaddy). AI crawlers are allowed in Cloudflare and in `static/robots.txt`.
- **Newsletter:** Beehiiv (protologue.beehiiv.com). The signup embed lives in `data/newsletter-embed.html`.

- **MCP server:** `mcp/` is a Cloudflare Worker (`protologue-mcp`) at https://mcp.protologue.com/mcp, deployed automatically from this repo. It is listed in the official MCP registry as `com.protologue/protologue` (`mcp/server.json`). Registry ownership is proven by `static/.well-known/mcp-registry-auth`; to re-key, generate a new Ed25519 key and replace that file.

Proposed changes arrive as pull requests; merging one publishes it.

## Growing citations after launch

1. **Get indexed.**
   - Add the site to Google Search Console and Bing Webmaster Tools, and submit `https://protologue.com/sitemap.xml`.
   - Bing matters a lot, because its index feeds several AI assistants' web search.
   - Turn on IndexNow in Cloudflare (Caching → Configuration → Crawler Hints) so updates are announced automatically.
2. **Mint a DOI.** Publish the GitHub repo and connect it to Zenodo. Each release then gets a DOI. Researchers cite DOIs, and DOIs are what academic search and AI research tools resolve.
3. **Publish the dataset where models are trained and evaluated.** Mirror `site/data/protologue.json` as a Hugging Face dataset and a Kaggle dataset. Both should link back to the canonical URLs.
4. **Earn links from the places answers come from.** Link entries when answering on Stack Overflow, Reddit or GitHub issues, and propose Protologue as a source in "awesome prompt engineering" lists.
5. **Keep it alive.** Release on a regular cadence: add new techniques as papers appear, bump `VERSION` in `build.py`, and keep "Last reviewed" dates current. Fresh, dated pages are preferred over stale ones.

## Adding a term

Append an entry to one of the `data/terms-*.yaml` files:

```yaml
- id: my-technique                # becomes protologue.com/t/my-technique/
  term: My Technique
  category: reasoning             # an id from categories.yaml
  definition: One or two sentences that stand alone when quoted.
  body: Context, limitations and how it relates to other techniques.
  aliases: [other name]
  broader: [chain-of-thought]     # optional: "is a kind of"
  related: [self-consistency]
  introduced: 2026
  sources:
    - {title: "Paper title", authors: "Surname et al.", year: 2026, url: "https://arxiv.org/abs/XXXX.XXXXX"}
```

Then run `python3 build.py`. The build fails with a clear message if a link points to a term that doesn't exist. New terms get the next free `PTL-` number automatically.

**Renaming or merging a term:** keep the old ID in `data/ids.json`, and add a line to `static/_redirects`:

```
/t/old-slug/  /t/new-slug/  301
```
