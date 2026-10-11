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

## Deploy on Cloudflare (domain stays registered at GoDaddy)

### 1. Move DNS for protologue.com to Cloudflare

1. Create a free Cloudflare account and choose **Add a domain**. Enter `protologue.com` and pick the Free plan.
2. During onboarding Cloudflare asks how to treat AI crawlers. **Choose to allow them.** If you miss the question, check afterwards (see step 4). Blocking AI crawlers would defeat the purpose of this site.
3. Cloudflare shows two nameservers, such as `xxx.ns.cloudflare.com`.
4. In GoDaddy, go to **My Products → protologue.com → DNS → Nameservers → Change nameservers → I'll use my own nameservers**. Paste the two Cloudflare nameservers and save. If DNSSEC is on at GoDaddy, turn it off first; you can re-enable it in Cloudflare later.
5. Wait for Cloudflare to email that the domain is active. This usually takes minutes but can take up to 24 hours.

### 2. Create the site (pick one)

**A. Fastest: upload the built folder, no Git**

Go to **Workers & Pages → Create → Pages → Upload assets**. Name the project `protologue` and drag in the `site/` folder.

**B. Recommended for ongoing edits: connect a GitHub repo**

Push this folder to GitHub, then go to **Workers & Pages → Create → Pages → Connect to Git** and use these settings:

- Build command: `pip install -r requirements.txt && python3 build.py`
- Build output directory: `site`

Every push to the repo then rebuilds the site.

**C. Command line**

Run `npx wrangler deploy` from this folder. It uses `wrangler.jsonc`.

### 3. Attach the domain

In the project, open **Custom domains** and add both `protologue.com` and `www.protologue.com`. Then add a **Redirect Rule** that sends `www.protologue.com/*` to `https://protologue.com/${1}` with a 301. Every page already declares `https://protologue.com/...` as its canonical URL.

### 4. Settings that matter for AI citation

- **Security → Bots:** leave "Block AI bots" off. Bot Fight Mode can also challenge crawlers, so keep it off unless you see abuse.
- **AI Crawl Control:** if offered, set AI crawlers to **Allow**. Do not enable a Cloudflare-managed robots.txt that disallows AI use. This site ships its own `robots.txt`, which explicitly allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended and others.
- Leave caching at the defaults. `_headers` already marks assets as long-lived and data files as open to cross-origin requests.

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
