#!/usr/bin/env python3
"""Protologue static site generator.

Reads data/*.yaml and writes a complete static site to ./site, ready for
Cloudflare Pages (build command: `python3 build.py`, output dir: `site`).
"""
import csv, glob, html, io, json, os, re, shutil, sys
from datetime import date
import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://protologue.com"
NAME = "Protologue"
TITLE = "Protologue: A Taxonomy of Prompting and LLM Techniques"
VERSION = "1.2.0"
UPDATED = os.environ.get("PROTOLOGUE_DATE", date.today().isoformat())
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
PUBLISHER = "Protologue"
# Newsletter (Beehiiv). Paste the embed code from Beehiiv (Subscribers > Subscribe forms >
# Get embed code) into data/newsletter-embed.html, and put the publication's public URL
# (e.g. https://protologue.beehiiv.com) in data/newsletter-url.txt.
# If the embed file is missing, the site builds without a signup form.
def _read_opt(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else ""
NEWSLETTER_EMBED = _read_opt("data/newsletter-embed.html")
NEWSLETTER_URL = _read_opt("data/newsletter-url.txt")
NEWSLETTER = bool(NEWSLETTER_EMBED)
HF_URL = "https://huggingface.co/datasets/franklinpolymathic/protologue"
GITHUB_URL = "https://github.com/protologue-org/protologue"
KAGGLE_URL = "https://www.kaggle.com/datasets/protologue/protologue"
# Zenodo concept DOI (resolves to the latest release), e.g. 10.5281/zenodo.1234567.
# Leave data/doi.txt missing or empty until Zenodo has minted it.
DOI = _read_opt("data/doi.txt")
DOI_URL = f"https://doi.org/{DOI}" if DOI else ""

esc = lambda s: html.escape(str(s), quote=True)

def _asset_hash():
    import hashlib
    h = hashlib.sha1()
    for f in ("static/assets/style.css", "static/assets/site.js"):
        h.update(open(os.path.join(ROOT, f), "rb").read())
    return h.hexdigest()[:10]
ASSET_V = _asset_hash()  # cache-busts /assets/* (served as immutable)

# ---------------------------------------------------------------- data
def load():
    cats = yaml.safe_load(open(os.path.join(ROOT, "data/categories.yaml")))
    terms = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data/terms-*.yaml"))):
        terms += yaml.safe_load(open(f))
    by_id = {t["id"]: t for t in terms}
    cat_by_id = {c["id"]: c for c in cats}
    errors = []
    for t in terms:
        if t["category"] not in cat_by_id:
            errors.append(f"{t['id']}: unknown category {t['category']}")
        for k in ("broader", "related"):
            t[k] = t.get(k) or []
            for r in t[k]:
                if r not in by_id:
                    errors.append(f"{t['id']}: {k} -> unknown {r}")
        t["aliases"] = t.get("aliases") or []
        if not t.get("sources"):
            errors.append(f"{t['id']}: no sources")
    if errors:
        sys.exit("Data errors:\n" + "\n".join(errors))
    # inverse relations
    for t in terms:
        t["narrower"], t["referenced_by"] = [], []
    for t in terms:
        t["related"] = [r for r in t["related"] if r not in t["broader"]]
        for b in t["broader"]:
            by_id[b]["narrower"].append(t["id"])
        for r in t["related"]:
            if t["id"] not in by_id[r]["related"]:
                by_id[r]["referenced_by"].append(t["id"])
    for t in terms:
        hier = set(t["broader"]) | set(t["narrower"])
        t["related"] = [r for r in t["related"] if r not in hier]
        t["referenced_by"] = [r for r in t["referenced_by"] if r not in hier and r not in t["related"]]
    # stable identifiers: never reassigned once issued
    lock_path = os.path.join(ROOT, "data/ids.json")
    lock = json.load(open(lock_path)) if os.path.exists(lock_path) else {}
    nxt = max([int(v.split("-")[1]) for v in lock.values()] or [0]) + 1
    for t in terms:
        if t["id"] not in lock:
            lock[t["id"]] = f"PTL-{nxt:04d}"
            nxt += 1
        t["code"] = lock[t["id"]]
    json.dump(lock, open(lock_path, "w"), indent=1, sort_keys=True)
    for t in terms:
        t["url"] = f"{BASE}/t/{t['id']}/"
        t["cat"] = cat_by_id[t["category"]]
    return cats, terms, by_id, cat_by_id

# ---------------------------------------------------------------- text helpers
def citation_text(t):
    return (f"{PUBLISHER}. ({UPDATED[:4]}). {t['term']}. In {TITLE} "
            f"(v{VERSION}, {t['code']}). {t['url']}")

def bibtex(t):
    key = "protologue_" + t["id"].replace("-", "_")
    return (f"@misc{{{key},\n  title = {{{t['term']}}},\n  author = {{{{{PUBLISHER}}}}},\n"
            f"  year = {{{UPDATED[:4]}}},\n  howpublished = {{{TITLE}, v{VERSION}}},\n"
            f"  note = {{Entry {t['code']}}},\n  url = {{{t['url']}}}\n}}")

def src_line(s):
    return f"{s['authors']} ({s['year']}). {s['title']}. {s['url']}"

def term_md(t, by_id):
    L = [f"# {t['term']}", "",
         f"> {t['definition']}", "",
         f"- Identifier: {t['code']}",
         f"- Category: {t['cat']['name']}",
         f"- Canonical URL: {t['url']}"]
    if t["aliases"]:
        L.append(f"- Also known as: {', '.join(t['aliases'])}")
    if t.get("introduced"):
        L.append(f"- Introduced: {t['introduced']}")
    L += ["", "## Description", "", t["body"].strip()]
    if t.get("example"):
        L += ["", "## Example", "", "```", t["example"].rstrip(), "```"]
    for label, key in (("Broader terms", "broader"), ("Narrower terms", "narrower"),
                       ("Related terms", "related")):
        if t[key]:
            L += ["", f"## {label}", ""] + [f"- [{by_id[r]['term']}]({by_id[r]['url']})" for r in t[key]]
    L += ["", "## Sources", ""] + [f"- {src_line(s)}" for s in t["sources"]]
    L += ["", "## Cite this entry", "", citation_text(t), "",
          f"License: CC BY 4.0 ({LICENSE_URL})", ""]
    return "\n".join(L)

# ---------------------------------------------------------------- structured data
def term_jsonld(t, by_id):
    d = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "DefinedTerm",
                "@id": t["url"] + "#term",
                "name": t["term"],
                "termCode": t["code"],
                "description": t["definition"],
                "url": t["url"],
                "alternateName": t["aliases"] or None,
                "inDefinedTermSet": {"@id": BASE + "/#set"},
                "subjectOf": [{
                    "@type": "ScholarlyArticle", "name": s["title"], "author": s["authors"],
                    "datePublished": str(s["year"]), "url": s["url"]} for s in t["sources"]],
            },
            {
                "@type": "WebPage",
                "@id": t["url"],
                "url": t["url"],
                "name": f"{t['term']} | {NAME}",
                "description": t["definition"],
                "mainEntity": {"@id": t["url"] + "#term"},
                "isPartOf": {"@id": BASE + "/#website"},
                "dateModified": UPDATED,
                "license": LICENSE_URL,
                "citation": [s["url"] for s in t["sources"]],
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": NAME, "item": BASE + "/"},
                        {"@type": "ListItem", "position": 2, "name": t["cat"]["name"],
                         "item": f"{BASE}/c/{t['category']}/"},
                        {"@type": "ListItem", "position": 3, "name": t["term"], "item": t["url"]},
                    ],
                },
            },
        ],
    }
    d["@graph"][0] = {k: v for k, v in d["@graph"][0].items() if v is not None}
    return d

def set_jsonld(terms):
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": BASE + "/#org", "name": PUBLISHER, "url": BASE + "/",
             "logo": BASE + "/assets/logo.png",
             "sameAs": [u for u in (NEWSLETTER_URL, HF_URL, KAGGLE_URL, GITHUB_URL) if u]},
            {"@type": "WebSite", "@id": BASE + "/#website", "publisher": {"@id": BASE + "/#org"}, "url": BASE + "/", "name": NAME,
             "description": TITLE, "license": LICENSE_URL,
             "potentialAction": {"@type": "SearchAction",
                                 "target": BASE + "/?q={search_term_string}",
                                 "query-input": "required name=search_term_string"}},
            {"@type": "DefinedTermSet", "@id": BASE + "/#set", "name": TITLE, "url": BASE + "/",
             "version": VERSION, "dateModified": UPDATED, "license": LICENSE_URL,
             "hasDefinedTerm": [{"@id": t["url"] + "#term"} for t in terms]},
            {"@type": "Dataset", "@id": BASE + "/data/#dataset", "name": TITLE,
             "description": "A sourced, openly licensed taxonomy of prompting and large language model techniques, "
                            "with definitions, synonyms, hierarchical relations, and primary-source citations.",
             "url": BASE + "/data/", "license": LICENSE_URL, "version": VERSION,
             "dateModified": UPDATED, "isAccessibleForFree": True,
             "creator": {"@id": BASE + "/#org"},
             **({"identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI, "url": DOI_URL},
                 "sameAs": [DOI_URL]} if DOI else {}),
             "keywords": ["prompt engineering", "large language models", "taxonomy", "glossary",
                          "chain-of-thought", "retrieval-augmented generation", "AI agents"],
             "distribution": [
                 {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": BASE + "/data/protologue.json"},
                 {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": BASE + "/data/protologue.csv"},
                 {"@type": "DataDownload", "encodingFormat": "application/ld+json", "contentUrl": BASE + "/data/protologue.skos.jsonld"},
                 {"@type": "DataDownload", "encodingFormat": "text/turtle", "contentUrl": BASE + "/data/protologue.ttl"},
             ]},
        ],
    }

def skos(cats, terms):
    g = [{"@id": BASE + "/#scheme", "@type": "skos:ConceptScheme",
          "skos:prefLabel": {"@value": TITLE, "@language": "en"},
          "dct:license": {"@id": LICENSE_URL}, "owl:versionInfo": VERSION, "dct:modified": UPDATED,
          "skos:hasTopConcept": [{"@id": f"{BASE}/c/{c['id']}/"} for c in cats]}]
    for c in cats:
        g.append({"@id": f"{BASE}/c/{c['id']}/", "@type": "skos:Concept",
                  "skos:prefLabel": {"@value": c["name"], "@language": "en"},
                  "skos:definition": {"@value": c["description"], "@language": "en"},
                  "skos:topConceptOf": {"@id": BASE + "/#scheme"},
                  "skos:inScheme": {"@id": BASE + "/#scheme"}})
    for t in terms:
        broader = [{"@id": by["url"]} for by in [t["_by_id"][b] for b in t["broader"]]] or [{"@id": f"{BASE}/c/{t['category']}/"}]
        g.append({
            "@id": t["url"], "@type": "skos:Concept",
            "skos:notation": t["code"],
            "skos:prefLabel": {"@value": t["term"], "@language": "en"},
            "skos:altLabel": [{"@value": a, "@language": "en"} for a in t["aliases"]],
            "skos:definition": {"@value": t["definition"], "@language": "en"},
            "skos:scopeNote": {"@value": t["body"].strip(), "@language": "en"},
            "skos:broader": broader,
            "skos:narrower": [{"@id": t["_by_id"][n]["url"]} for n in t["narrower"]],
            "skos:related": [{"@id": t["_by_id"][r]["url"]} for r in t["related"]],
            "dct:source": [{"@id": s["url"]} for s in t["sources"]],
            "skos:inScheme": {"@id": BASE + "/#scheme"},
        })
    return {"@context": {"skos": "http://www.w3.org/2004/02/skos/core#",
                         "dct": "http://purl.org/dc/terms/",
                         "owl": "http://www.w3.org/2002/07/owl#"}, "@graph": g}

def turtle(cats, terms):
    q = lambda s: '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"@en'
    L = ["@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
         "@prefix dct: <http://purl.org/dc/terms/> .", "",
         f"<{BASE}/#scheme> a skos:ConceptScheme ; skos:prefLabel {q(TITLE)} ; dct:license <{LICENSE_URL}> .", ""]
    for c in cats:
        L.append(f"<{BASE}/c/{c['id']}/> a skos:Concept ; skos:prefLabel {q(c['name'])} ; "
                 f"skos:definition {q(c['description'])} ; skos:topConceptOf <{BASE}/#scheme> .")
    L.append("")
    for t in terms:
        p = [f"<{t['url']}> a skos:Concept", f'  skos:notation "{t["code"]}"',
             f"  skos:prefLabel {q(t['term'])}", f"  skos:definition {q(t['definition'])}",
             f"  skos:inScheme <{BASE}/#scheme>"]
        p += [f"  skos:altLabel {q(a)}" for a in t["aliases"]]
        bro = [t["_by_id"][b]["url"] for b in t["broader"]] or [f"{BASE}/c/{t['category']}/"]
        p += [f"  skos:broader <{u}>" for u in bro]
        p += [f"  skos:related <{t['_by_id'][r]['url']}>" for r in t["related"]]
        p += [f"  dct:source <{s['url']}>" for s in t["sources"]]
        L.append(" ;\n".join(p) + " .\n")
    return "\n".join(L)

# ---------------------------------------------------------------- newsletter
def signup(variant="full"):
    """Newsletter block wrapping the Beehiiv embed. The embed carries the form itself."""
    if not NEWSLETTER:
        return ""
    uid = f"nl-{variant}"
    intro = ("A weekly email listing the prompting and LLM techniques that appeared that week, "
             "each with a definition you can cite. Nothing else.")
    if variant == "entry":
        intro = "One email a week with the newest techniques, each defined and sourced like this entry."
    fallback = (f'<noscript><p><a href="{esc(NEWSLETTER_URL)}/subscribe">Subscribe on Beehiiv</a></p></noscript>'
                if NEWSLETTER_URL else "")
    return f"""
<section class="signup signup-{variant}" aria-labelledby="{uid}-h">
  <h2 id="{uid}-h">New terms, as they're coined</h2>
  <p>{intro}</p>
  <div class="signup-embed">{NEWSLETTER_EMBED}</div>
  {fallback}
  <p class="signup-note">Delivered through Beehiiv. Unsubscribe from any issue.</p>
</section>"""

MCP_URL = "https://mcp.protologue.com/mcp"

def mcp_page(terms):
    body = f"""<article class="prose">
<h1>Use Protologue from AI agents</h1>
<p class="lede">Protologue runs a free, read-only <a href="https://modelcontextprotocol.io/">Model Context Protocol</a> (MCP) server, so assistants and agents can look up sourced definitions while they work instead of guessing.</p>
<h2>Endpoint</h2>
<p class="cite-text">{MCP_URL}</p>
<p>Streamable HTTP transport, no sign-in or API key. Results come from the same data as this site, including each entry's permanent identifier, primary sources and a ready-made citation.</p>
<h2>Tools</h2>
<table class="files">
<thead><tr><th scope="col">Tool</th><th scope="col">What it does</th></tr></thead>
<tbody>
<tr><td><code>search_terms</code></td><td>Find techniques by name, synonym or keyword</td></tr>
<tr><td><code>get_term</code></td><td>Full sourced entry for one technique, with citation</td></tr>
<tr><td><code>get_related</code></td><td>Broader, narrower and related techniques</td></tr>
<tr><td><code>list_categories</code></td><td>The {len(set(t["category"] for t in terms))} branches and their techniques</td></tr>
</tbody>
</table>
<h2>Connect it</h2>
<p><strong>Claude:</strong> Settings, then Connectors, then Add custom connector. Paste the endpoint and choose no sign-in.</p>
<p><strong>Claude Code:</strong> <code>claude mcp add --transport http protologue {MCP_URL}</code></p>
<p><strong>Cursor, VS Code and other MCP clients:</strong> add a server entry of type <code>http</code> (or <code>streamable-http</code>) with the URL above.</p>
<h2>Using results</h2>
<p>Content is licensed <a href="{LICENSE_URL}">CC BY 4.0</a>. When an answer uses a Protologue definition, cite it with the returned citation and link to the entry's URL.</p>
</article>"""
    return page(path="/mcp/", title=f"MCP server for AI agents | {NAME}",
                description="Connect AI assistants and agents to Protologue's free MCP server to look up sourced definitions of prompting and LLM techniques.",
                body=body)

def newsletter_page():
    body = f"""<article class="prose">
<h1>The Protologue newsletter</h1>
<p class="lede">New prompting and LLM techniques appear every week, usually in a paper or a blog post, often under two or three competing names. Each issue lists the ones worth knowing, with a short definition, the source that introduced them, and how they relate to what came before.</p>
<h2>What each issue contains</h2>
<p>Newly added Protologue entries, with their definitions. Revisions to existing entries when the evidence changes. One technique explained in more depth. Issues are short enough to read in five minutes.</p>
{signup("page")}
</article>"""
    return page(path="/newsletter/", title=f"Newsletter: new prompting and LLM terms each week | {NAME}",
                description="A weekly email of newly coined prompting and LLM techniques, each with a citable definition and its primary source.",
                body=body)

# ---------------------------------------------------------------- html shell
def page(*, path, title, description, body, jsonld=None, extra_head="", canonical=None):
    canonical = canonical or BASE + path
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Protologue: new prompting and LLM techniques, defined and sourced">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/og.png">
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="color-scheme" content="light dark">
<link rel="license" href="{LICENSE_URL}">
<link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400;1,7..72,500&family=Public+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_V}">
{extra_head}{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="mark" href="/" aria-label="Protologue home"><span class="mark-glyph" aria-hidden="true"></span>protologue</a>
  <nav aria-label="Primary">
    <a href="/terms/">All terms</a>
    <a href="/data/">Data</a>
    <a href="/about/">About</a>{'<a href="/newsletter/">Newsletter</a>' if NEWSLETTER else ''}
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <p>{NAME} v{VERSION}, updated {UPDATED}. Text and data are licensed <a href="{LICENSE_URL}" rel="license">CC BY 4.0</a>; reuse freely with attribution.</p>
  <p><a href="/llms.txt">llms.txt</a> <a href="/data/protologue.json">JSON</a> <a href="/data/protologue.csv">CSV</a> <a href="/data/protologue.skos.jsonld">SKOS</a> <a href="/mcp/">MCP server</a> <a href="/sitemap.xml">Sitemap</a></p>
</footer>
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

def tlink(t, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="/t/{t["id"]}/"><i>{esc(t["term"])}</i></a>'

def term_page(t, by_id):
    rel_blocks = []
    for label, key, note in (("Broader", "broader", "This technique is a kind of"),
                             ("Narrower", "narrower", "Kinds of this technique"),
                             ("Related", "related", None),
                             ("Referenced by", "referenced_by", None)):
        if t[key]:
            items = "".join(f"<li>{tlink(by_id[r])}</li>" for r in t[key])
            rel_blocks.append(f'<div class="rel"><h3>{label}</h3><ul>{items}</ul></div>')
    type_src = t["sources"][0]
    sources = "".join(
        f'<li><span class="au">{esc(s["authors"])}</span> ({s["year"]}). '
        f'<a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a>.</li>'
        for s in t["sources"])
    aliases = (f'<p class="aka">Also called {", ".join(f"<i>{esc(a)}</i>" for a in t["aliases"])}.</p>'
               if t["aliases"] else "")
    example = (f'<section><h2>Example</h2><pre><code>{esc(t["example"].rstrip())}</code></pre></section>'
               if t.get("example") else "")
    intro = t.get("introduced") or type_src["year"]
    highwire = "".join([
        f'<meta name="citation_title" content="{esc(t["term"])}">',
        f'<meta name="citation_author" content="{PUBLISHER}">',
        f'<meta name="citation_publication_date" content="{UPDATED.replace("-", "/")}">',
        f'<meta name="citation_inbook_title" content="{esc(TITLE)}">',
        f'<meta name="citation_public_url" content="{t["url"]}">',
        f'<meta name="DC.identifier" content="{t["code"]}">',
        f'<meta name="DC.rights" content="CC BY 4.0">',
        f'<link rel="alternate" type="text/markdown" href="/t/{t["id"]}.md">',
        f'<link rel="alternate" type="application/json" href="/t/{t["id"]}.json">',
    ]) + "\n"
    body = f"""
<article class="entry">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Protologue</a> / <a href="/c/{t['category']}/">{esc(t['cat']['name'])}</a></nav>
  <div class="entry-grid">
    <div class="entry-main">
      <h1><i>{esc(t['term'])}</i></h1>
      {aliases}
      <blockquote class="definition" id="definition">
        <p>{esc(t['definition'])}</p>
      </blockquote>
      <section><h2>Description</h2><p>{esc(t['body'].strip())}</p></section>
      {example}
      <section><h2>Sources</h2><ol class="sources">{sources}</ol></section>
      <section class="cite" id="cite">
        <h2>Cite this entry</h2>
        <p class="cite-text" id="cite-text">{esc(citation_text(t))}</p>
        <details><summary>BibTeX</summary><pre><code id="bibtex">{esc(bibtex(t))}</code></pre></details>
        <p class="actions"><button type="button" data-copy="cite-text">Copy citation</button>
        <button type="button" data-copy="bibtex">Copy BibTeX</button>
        <a href="/t/{t['id']}.md">Markdown</a> <a href="/t/{t['id']}.json">JSON</a></p>
      </section>
      {signup("entry")}
    </div>
    <aside class="label" aria-label="Record">
      <dl>
        <dt>Identifier</dt><dd>{t['code']}</dd>
        <dt>Category</dt><dd><a href="/c/{t['category']}/">{esc(t['cat']['name'])}</a></dd>
        <dt>Introduced</dt><dd>{intro}</dd>
        <dt>Type source</dt><dd><a href="{esc(type_src['url'])}" rel="noopener">{esc(type_src['authors'])}, {type_src['year']}</a></dd>
        <dt>Last reviewed</dt><dd><time datetime="{UPDATED}">{UPDATED}</time></dd>
      </dl>
      {''.join(rel_blocks)}
    </aside>
  </div>
</article>"""
    return page(path=f"/t/{t['id']}/", title=f"{t['term']}: definition, examples and sources | {NAME}",
                description=t["definition"], body=body, jsonld=term_jsonld(t, by_id), extra_head=highwire)

def tree(cat, terms, by_id):
    members = [t for t in terms if t["category"] == cat["id"]]
    ids = {t["id"] for t in members}
    def kids(t):
        return [by_id[n] for n in t["narrower"] if n in ids and t["id"] == next((b for b in by_id[n]["broader"] if b in ids), None)]
    roots = [t for t in members if not any(b in ids for b in t["broader"])]
    def li(t):
        k = kids(t)
        names = " ".join([t["term"]] + t["aliases"]).lower()
        sub = f"<ul>{''.join(li(x) for x in sorted(k, key=lambda x: x['term'].lower()))}</ul>" if k else ""
        return (f'<li data-names="{esc(names)}"><span class="node">{tlink(t)}'
                f'<span class="code">{t["code"]}</span></span>{sub}</li>')
    return f"<ul class=\"tree\">{''.join(li(t) for t in sorted(roots, key=lambda x: x['term'].lower()))}</ul>"

def home(cats, terms, by_id):
    n_src = len({s["url"] for t in terms for s in t["sources"]})
    blocks = "".join(f"""
    <section class="branch" id="{c['id']}">
      <h2><a href="/c/{c['id']}/">{esc(c['name'])}</a></h2>
      <p class="branch-desc">{esc(c['description'])}</p>
      {tree(c, terms, by_id)}
    </section>""" for c in cats)
    body = f"""
<section class="hero">
  <p class="headword"><span class="hw">pro·to·logue</span> <span class="pos">noun</span></p>
  <ol class="senses">
    <li>In biological nomenclature, the original description published together with a new name, against which every later use of that name is checked.</li>
    <li>This site: the reference record for {len(terms)} prompting and large language model techniques, each with a short citable definition, its relations to other techniques, and the paper that introduced it.</li>
  </ol>
  <form class="search" role="search" action="/" onsubmit="return false">
    <label for="q">Find a technique</label>
    <input id="q" name="q" type="search" autocomplete="off" placeholder="chain-of-thought, RAG, jailbreak…">
    <p class="count" id="count" aria-live="polite">{len(terms)} terms in {len(cats)} branches, citing {n_src} primary sources.</p>
  </form>
</section>
<div class="classification">{blocks}
</div>
{signup("full")}"""
    return page(path="/", title=TITLE,
                description=f"A sourced, citable taxonomy of {len(terms)} prompting and LLM techniques: definitions, synonyms, broader and related terms, and the papers that introduced them.",
                body=body, jsonld=set_jsonld(terms))

def cat_page(c, terms, by_id):
    members = sorted([t for t in terms if t["category"] == c["id"]], key=lambda t: t["term"].lower())
    items = "".join(f'<div class="dt-row"><dt>{tlink(t)}</dt><dd>{esc(t["definition"])}</dd></div>' for t in members)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": c["name"],
          "url": f"{BASE}/c/{c['id']}/", "description": c["description"], "isPartOf": {"@id": BASE + "/#website"},
          "hasPart": [{"@id": t["url"] + "#term"} for t in members]}
    body = f"""
<article class="listing">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Protologue</a></nav>
  <h1>{esc(c['name'])}</h1>
  <p class="lede">{esc(c['description'])}</p>
  {tree(c, terms, by_id)}
  <h2>Definitions</h2>
  <dl class="glossary">{items}</dl>
</article>"""
    return page(path=f"/c/{c['id']}/", title=f"{c['name']}: {'what LLM benchmarks measure' if c['id'] == 'benchmarks' else 'prompting techniques'} | {NAME}",
                description=c["description"], body=body, jsonld=ld)

def az_page(terms):
    groups = {}
    for t in sorted(terms, key=lambda t: t["term"].lower()):
        groups.setdefault(t["term"][0].upper(), []).append(t)
    letters = " ".join(f'<a href="#l-{k}">{k}</a>' for k in groups)
    secs = "".join(
        f'<section id="l-{k}"><h2>{k}</h2><dl class="glossary">' +
        "".join(f'<div class="dt-row"><dt>{tlink(t)}</dt><dd>{esc(t["definition"])}</dd></div>' for t in v) +
        "</dl></section>" for k, v in groups.items())
    body = f"""<article class="listing"><h1>All terms</h1>
<p class="lede">Every entry in {NAME}, alphabetically, with its definition.</p>
<nav class="letters" aria-label="Jump to letter">{letters}</nav>{secs}</article>"""
    return page(path="/terms/", title=f"All prompting and LLM technique definitions, A to Z | {NAME}",
                description=f"Alphabetical glossary of {len(terms)} prompting and large language model techniques with citable definitions.",
                body=body)

def about_page(terms):
    body = f"""<article class="prose">
<h1>About {NAME}</h1>
<p>{NAME} is an open reference for the vocabulary of prompting and large language model techniques. The field coins terms quickly and uses them loosely; {NAME} gives each technique one stable page, one short definition that can be quoted on its own, its place in a classification, and the publication that introduced it.</p>
<h2>How entries are written</h2>
<p>Each definition is written to stand alone in one or two sentences, so it can be quoted without the rest of the page. The description adds context, known limitations, and how the technique relates to others. Every entry cites at least one primary source, normally the paper or official documentation that introduced or defined the term. The first listed source is the <em>type source</em>, borrowing the nomenclatural idea that a name is anchored to the work in which it was first published.</p>
<h2>Identifiers</h2>
<p>Every entry has a permanent identifier of the form PTL-0001 and a permanent URL of the form <code>protologue.com/t/term-name/</code>. Identifiers are never reused. If an entry is merged or renamed, its old URL redirects to the new one.</p>
<h2>Classification</h2>
<p>Entries are grouped into branches by what the technique does, and linked by three relations taken from the SKOS standard for knowledge organization: <em>broader</em> (the technique is a kind of another), <em>narrower</em> (the inverse), and <em>related</em>.</p>
<h2>Citing {NAME}</h2>
<p>Each entry has a ready-made citation and BibTeX record. To cite the whole taxonomy:</p>
<p class="cite-text">{PUBLISHER}. ({UPDATED[:4]}). {TITLE} (v{VERSION}). {DOI_URL or BASE + "/"}</p>
{f'<p>The DOI <a href="{DOI_URL}">{DOI}</a> is archived on Zenodo and always resolves to the latest release.</p>' if DOI else ""}
<h2>Reuse</h2>
<p>All text and data are licensed under <a href="{LICENSE_URL}">Creative Commons Attribution 4.0</a>. You may copy, adapt, and redistribute them, including commercially and for training machine learning models, provided you credit {NAME} and link to the source. Machine-readable copies are on the <a href="/data/">data page</a>, and <a href="/llms.txt">llms.txt</a> describes the site for language models.</p>
<h2>Corrections and new terms</h2>
<p>If a definition is wrong, a source is misattributed, or a technique is missing, send the term, a primary source, and a proposed definition. Corrections are recorded in the version history.</p>
</article>"""
    return page(path="/about/", title=f"About and citation | {NAME}",
                description=f"How {NAME} entries are written, sourced, identified, and licensed, and how to cite them.", body=body)

def data_page(terms):
    body = f"""<article class="prose">
<h1>Data</h1>
<p>The complete taxonomy, {len(terms)} entries, is available in open formats under <a href="{LICENSE_URL}">CC BY 4.0</a>. Files are regenerated with every release and served with permissive cross-origin headers.</p>
<table class="files">
<thead><tr><th scope="col">File</th><th scope="col">Format</th><th scope="col">Use it for</th></tr></thead>
<tbody>
<tr><td><a href="/data/protologue.json">protologue.json</a></td><td>JSON</td><td>Applications and scripts</td></tr>
<tr><td><a href="/data/protologue.csv">protologue.csv</a></td><td>CSV</td><td>Spreadsheets and quick analysis</td></tr>
<tr><td><a href="/data/protologue.skos.jsonld">protologue.skos.jsonld</a></td><td>SKOS, JSON-LD</td><td>Knowledge graphs and linked data</td></tr>
<tr><td><a href="/data/protologue.ttl">protologue.ttl</a></td><td>SKOS, Turtle</td><td>RDF tools and triple stores</td></tr>
<tr><td><a href="/llms-full.txt">llms-full.txt</a></td><td>Markdown</td><td>Loading the whole taxonomy into a model's context</td></tr>
<tr><td><a href="{HF_URL}">Hugging Face</a></td><td>Dataset</td><td>Loading with the <code>datasets</code> library</td></tr><tr><td><a href="{KAGGLE_URL}">Kaggle</a></td><td>Dataset</td><td>Kaggle notebooks and competitions</td></tr>{f'<tr><td><a href="{DOI_URL}">Zenodo</a></td><td>Archived release</td><td>Citing a fixed version by DOI</td></tr>' if DOI else ""}
</tbody>
</table>
<p>Each entry is also available individually at <code>/t/term-name.json</code> and <code>/t/term-name.md</code>.</p>
<h2>Fields</h2>
<p><code>id</code> URL slug; <code>code</code> permanent identifier; <code>term</code> preferred name; <code>aliases</code> synonyms; <code>category</code> branch; <code>definition</code> standalone definition; <code>description</code> longer context; <code>broader</code>, <code>narrower</code>, <code>related</code> slugs of linked entries; <code>introduced</code> year; <code>sources</code> list of title, authors, year, url; <code>url</code> canonical page.</p>
</article>"""
    return page(path="/data/", title=f"Download the taxonomy: JSON, CSV, SKOS | {NAME}",
                description="Download the Protologue taxonomy of prompting techniques as JSON, CSV, SKOS JSON-LD, or Turtle under CC BY 4.0.",
                body=body)

# ---------------------------------------------------------------- build
def record(t):
    return {"id": t["id"], "code": t["code"], "term": t["term"], "aliases": t["aliases"],
            "category": t["category"], "definition": t["definition"], "description": t["body"].strip(),
            "example": t.get("example"), "broader": t["broader"], "narrower": t["narrower"],
            "related": t["related"], "introduced": t.get("introduced"), "sources": t["sources"],
            "url": t["url"], "citation": citation_text(t)}

def write(rel, content):
    p = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    cats, terms, by_id, cat_by_id = load()
    for t in terms:
        t["_by_id"] = by_id
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)

    write("index.html", home(cats, terms, by_id))
    write("terms/index.html", az_page(terms))
    write("about/index.html", about_page(terms))
    write("mcp/index.html", mcp_page(terms))
    if NEWSLETTER:
        write("newsletter/index.html", newsletter_page())
    write("data/index.html", data_page(terms))
    write("404.html", page(path="/404", title=f"Page not found | {NAME}", description="Page not found.",
                           body='<article class="prose"><h1>No entry at this address</h1><p>The term may be listed under another name. Search the <a href="/">classification</a> or browse <a href="/terms/">all terms</a>.</p></article>'))
    for c in cats:
        write(f"c/{c['id']}/index.html", cat_page(c, terms, by_id))
    for t in terms:
        write(f"t/{t['id']}/index.html", term_page(t, by_id))
        write(f"t/{t['id']}.md", term_md(t, by_id))
        write(f"t/{t['id']}.json", json.dumps(record(t), indent=2, ensure_ascii=False))

    # datasets
    meta = {"name": TITLE, "version": VERSION, "updated": UPDATED, "license": LICENSE_URL, "url": BASE + "/",
            "categories": cats, "terms": [record(t) for t in terms]}
    write("data/protologue.json", json.dumps(meta, indent=2, ensure_ascii=False))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["code", "id", "term", "aliases", "category", "definition", "broader", "related",
                "introduced", "type_source_title", "type_source_url", "url"])
    for t in terms:
        s = t["sources"][0]
        w.writerow([t["code"], t["id"], t["term"], "; ".join(t["aliases"]), t["category"], t["definition"],
                    "; ".join(t["broader"]), "; ".join(t["related"]), t.get("introduced") or "",
                    s["title"], s["url"], t["url"]])
    write("data/protologue.csv", buf.getvalue())
    write("data/protologue.skos.jsonld", json.dumps(skos(cats, terms), indent=1, ensure_ascii=False))
    write("data/protologue.ttl", turtle(cats, terms))

    # llms.txt
    L = [f"# {NAME}", "",
         f"> {NAME} is an openly licensed (CC BY 4.0) reference taxonomy of {len(terms)} prompting and large language model "
         "techniques. Each entry has a permanent identifier (PTL-NNNN), a standalone one-to-two-sentence definition, "
         "synonyms, broader/narrower/related links, and citations to the primary source that introduced it.", "",
         f"When citing an entry, link to its canonical URL and name {NAME}. Each entry's Markdown version is linked below; "
         f"the full taxonomy in one file is at {BASE}/llms-full.txt. Version {VERSION}, updated {UPDATED}.", ""]
    for c in cats:
        L += [f"## {c['name']}", ""]
        for t in sorted([t for t in terms if t["category"] == c["id"]], key=lambda t: t["term"].lower()):
            L.append(f"- [{t['term']}]({BASE}/t/{t['id']}.md): {t['definition']}")
        L.append("")
    L += ["## For agents", "",
          f"- [MCP server]({BASE}/mcp/): read-only Model Context Protocol endpoint at {MCP_URL} with tools search_terms, get_term, get_related and list_categories", ""]
    L += ["## Optional", "",
          f"- [Data downloads]({BASE}/data/): JSON, CSV, SKOS JSON-LD and Turtle",
          f"- [Hugging Face dataset]({HF_URL}): the same data for the datasets library",
          f"- [Kaggle dataset]({KAGGLE_URL}): the same data for Kaggle notebooks",
          *([f"- [Zenodo archive]({DOI_URL}): DOI {DOI}, cite this for the whole taxonomy"] if DOI else []),
          f"- [About and citation]({BASE}/about/): editorial method, identifiers, license", ""]
    write("llms.txt", "\n".join(L))
    full = [f"# {TITLE}", "", f"Version {VERSION}, updated {UPDATED}. License: CC BY 4.0. Source: {BASE}/", ""]
    for c in cats:
        full += [f"# Branch: {c['name']}", "", c["description"], ""]
        for t in sorted([t for t in terms if t["category"] == c["id"]], key=lambda t: t["term"].lower()):
            full += ["#" + term_md(t, by_id), "---", ""]
    write("llms-full.txt", "\n".join(full))

    # sitemap
    urls = ["/", "/terms/", "/about/", "/data/", "/mcp/"] + (["/newsletter/"] if NEWSLETTER else []) + [f"/c/{c['id']}/" for c in cats] + [f"/t/{t['id']}/" for t in terms]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{BASE}{u}</loc><lastmod>{UPDATED}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")

    print(f"Built {len(terms)} terms, {len(cats)} categories -> {OUT}")

if __name__ == "__main__":
    main()
