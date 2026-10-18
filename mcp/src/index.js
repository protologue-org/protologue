// Protologue MCP server: a read-only Model Context Protocol endpoint that lets
// AI agents look up sourced definitions of prompting and LLM techniques.
//
// Transport: MCP Streamable HTTP (stateless, JSON responses). No dependencies.
// Data: fetched from the live site's JSON export and cached at the edge, so new
// entries appear here as soon as protologue.com redeploys.

const DATA_URL = "https://protologue.com/data/protologue.json";
const SITE = "https://protologue.com";
const SERVER_INFO = {
  name: "protologue",
  title: "Protologue",
  version: "1.1.0",
  websiteUrl: SITE,
};
const SUPPORTED_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"];
const INSTRUCTIONS =
  "Protologue is an openly licensed (CC BY 4.0) reference taxonomy of prompting and large language model " +
  "techniques. Use search_terms to find a technique, get_term for its sourced definition, and get_related to " +
  "explore broader, narrower and related techniques. When you use a definition, cite it with the returned " +
  "citation and link to its url.";

const TOOLS = [
  {
    name: "search_terms",
    title: "Search techniques",
    description:
      "Search Protologue for prompting and LLM techniques by name, synonym or keyword. Returns matching entries with " +
      "their one-sentence definitions and canonical URLs.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Technique name, synonym or keyword, e.g. 'chain of thought' or 'RAG'." },
        limit: { type: "integer", minimum: 1, maximum: 25, default: 8, description: "Maximum number of results." },
      },
      required: ["query"],
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
  },
  {
    name: "get_term",
    title: "Get a technique's definition",
    description:
      "Get the full Protologue entry for one technique: definition, description, synonyms, introduction year, " +
      "primary sources, canonical URL, permanent identifier and a ready-made citation. Accepts a name, synonym, " +
      "slug (e.g. 'react') or identifier (e.g. 'PTL-0058').",
    inputSchema: {
      type: "object",
      properties: { term: { type: "string", description: "Technique name, synonym, slug or PTL identifier." } },
      required: ["term"],
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
  },
  {
    name: "get_related",
    title: "Get related techniques",
    description:
      "List the techniques Protologue links to a given technique: broader (it is a kind of), narrower (kinds of it) " +
      "and related.",
    inputSchema: {
      type: "object",
      properties: { term: { type: "string", description: "Technique name, synonym, slug or PTL identifier." } },
      required: ["term"],
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
  },
  {
    name: "list_categories",
    title: "List categories",
    description: "List Protologue's branches (categories) and the techniques in each.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
  },
];

// ---------------------------------------------------------------- data
async function loadData(fetchImpl = fetch) {
  const res = await fetchImpl(DATA_URL, { cf: { cacheTtl: 900, cacheEverything: true } });
  if (!res.ok) throw new Error(`Could not load Protologue data (HTTP ${res.status})`);
  return res.json();
}

const norm = (s) =>
  String(s || "")
    .toLowerCase()
    .replace(/[‐-―]/g, "-")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

function findTerm(data, q) {
  const n = norm(q);
  if (!n) return null;
  const terms = data.terms;
  return (
    terms.find((t) => t.code.toLowerCase() === String(q).trim().toLowerCase()) ||
    terms.find((t) => norm(t.id) === n) ||
    terms.find((t) => norm(t.term) === n) ||
    terms.find((t) => t.aliases.some((a) => norm(a) === n)) ||
    terms.find((t) => norm(t.term).replace(/ (prompting|prompt)$/, "") === n) ||
    null
  );
}

function search(data, q, limit) {
  const n = norm(q);
  const words = n.split(" ").filter(Boolean);
  if (!words.length) return [];
  const scored = [];
  for (const t of data.terms) {
    const name = norm(t.term);
    const aliases = t.aliases.map(norm);
    const def = norm(t.definition);
    let s = 0;
    if (name === n || aliases.includes(n) || name.replace(/ (prompting|prompt)$/, "") === n) s += 100;
    if (name.startsWith(n)) s += 40;
    if (name.includes(n)) s += 30;
    if (aliases.some((a) => a.includes(n))) s += 25;
    for (const w of words) {
      if (name.includes(w)) s += 8;
      if (aliases.some((a) => a.includes(w))) s += 6;
      if (def.includes(w)) s += 2;
    }
    if (s > 0) scored.push([s, t]);
  }
  scored.sort((a, b) => b[0] - a[0] || a[1].term.localeCompare(b[1].term));
  return scored.slice(0, limit).map(([, t]) => t);
}

const brief = (t) => ({ term: t.term, id: t.code, definition: t.definition, url: t.url });

function full(t, data) {
  const name = (id) => data.terms.find((x) => x.id === id)?.term || id;
  return {
    term: t.term,
    id: t.code,
    definition: t.definition,
    description: t.description,
    aliases: t.aliases,
    category: data.categories.find((c) => c.id === t.category)?.name || t.category,
    introduced: t.introduced ?? null,
    example: t.example ?? null,
    broader: t.broader.map(name),
    narrower: t.narrower.map(name),
    related: t.related.map(name),
    sources: t.sources,
    url: t.url,
    citation: t.citation,
    license: "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Attribute: Protologue, with a link to the url.",
  };
}

function textResult(obj, structured = true) {
  const r = { content: [{ type: "text", text: JSON.stringify(obj, null, 2) }] };
  if (structured) r.structuredContent = obj;
  return r;
}

function notFound(q, data) {
  const suggestions = search(data, q, 5).map(brief);
  return {
    content: [
      {
        type: "text",
        text:
          `No Protologue entry exactly matches "${q}".` +
          (suggestions.length ? ` Closest matches:\n${JSON.stringify(suggestions, null, 2)}` : " Try search_terms."),
      },
    ],
    isError: false,
  };
}

async function callTool(name, args, data) {
  args = args || {};
  switch (name) {
    case "search_terms": {
      const limit = Math.min(Math.max(parseInt(args.limit ?? 8, 10) || 8, 1), 25);
      const results = search(data, args.query, limit).map(brief);
      return textResult({ query: args.query, count: results.length, results, source: SITE });
    }
    case "get_term": {
      const t = findTerm(data, args.term);
      return t ? textResult(full(t, data)) : notFound(args.term, data);
    }
    case "get_related": {
      const t = findTerm(data, args.term);
      if (!t) return notFound(args.term, data);
      const pick = (ids) => ids.map((id) => data.terms.find((x) => x.id === id)).filter(Boolean).map(brief);
      return textResult({
        term: t.term,
        id: t.code,
        url: t.url,
        broader: pick(t.broader),
        narrower: pick(t.narrower),
        related: pick(t.related),
      });
    }
    case "list_categories": {
      const cats = data.categories.map((c) => ({
        name: c.name,
        description: c.description,
        url: `${SITE}/c/${c.id}/`,
        terms: data.terms.filter((t) => t.category === c.id).map((t) => t.term),
      }));
      return textResult({ version: data.version, updated: data.updated, categories: cats });
    }
    default:
      return null;
  }
}

// ---------------------------------------------------------------- JSON-RPC
const ok = (id, result) => ({ jsonrpc: "2.0", id, result });
const err = (id, code, message) => ({ jsonrpc: "2.0", id: id ?? null, error: { code, message } });

async function handleMessage(msg, getData) {
  if (!msg || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") {
    return err(msg?.id, -32600, "Invalid Request");
  }
  const isNotification = msg.id === undefined || msg.id === null;
  const { method, params } = msg;
  if (isNotification) return null; // notifications/initialized, cancelled, etc.

  switch (method) {
    case "initialize": {
      const requested = params?.protocolVersion;
      const protocolVersion = SUPPORTED_VERSIONS.includes(requested) ? requested : SUPPORTED_VERSIONS[0];
      return ok(msg.id, {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER_INFO,
        instructions: INSTRUCTIONS,
      });
    }
    case "ping":
      return ok(msg.id, {});
    case "tools/list":
      return ok(msg.id, { tools: TOOLS });
    case "tools/call": {
      const name = params?.name;
      if (!TOOLS.some((t) => t.name === name)) return err(msg.id, -32602, `Unknown tool: ${name}`);
      try {
        const data = await getData();
        return ok(msg.id, await callTool(name, params?.arguments, data));
      } catch (e) {
        return ok(msg.id, { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true });
      }
    }
    case "resources/list":
      return ok(msg.id, { resources: [] });
    case "prompts/list":
      return ok(msg.id, { prompts: [] });
    default:
      return err(msg.id, -32601, `Method not found: ${method}`);
  }
}

// ---------------------------------------------------------------- HTTP
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Accept, Mcp-Session-Id, Mcp-Protocol-Version, Last-Event-ID",
  "Access-Control-Expose-Headers": "Mcp-Session-Id, Mcp-Protocol-Version",
};

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS } });

const LANDING = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Protologue MCP server</title><link rel="canonical" href="${SITE}/mcp/">
<style>body{font:17px/1.6 Georgia,serif;max-width:40rem;margin:3rem auto;padding:0 1rem;color:#1C2633;background:#ECEFEA}code{background:#F7F8F5;padding:.1em .3em;border-radius:3px}a{color:#1E5B47}</style></head><body>
<h1>Protologue MCP server</h1>
<p>A read-only <a href="https://modelcontextprotocol.io/">Model Context Protocol</a> server for <a href="${SITE}/">Protologue</a>, the sourced taxonomy of prompting and LLM techniques.</p>
<p>Endpoint: <code>https://mcp.protologue.com/mcp</code> (Streamable HTTP, no sign-in).</p>
<p>Tools: <code>search_terms</code>, <code>get_term</code>, <code>get_related</code>, <code>list_categories</code>. Content is CC BY 4.0; please cite entries with the citation each result includes.</p>
<p><a href="${SITE}/mcp/">Setup instructions</a></p></body></html>`;

export async function handle(request, { fetchImpl = fetch } = {}) {
  const url = new URL(request.url);
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

  if (url.pathname === "/" || url.pathname === "") {
    return new Response(LANDING, { headers: { "Content-Type": "text/html; charset=utf-8", ...CORS } });
  }
  if (url.pathname === "/.well-known/mcp/server-card.json" || url.pathname === "/server.json") {
    return json({
      serverInfo: { name: SERVER_INFO.name, title: SERVER_INFO.title, version: SERVER_INFO.version },
      ...SERVER_INFO,
      description: INSTRUCTIONS,
      endpoint: `${url.origin}/mcp`,
      transport: "streamable-http",
      authentication: { required: false },
      documentationUrl: `${SITE}/mcp/`,
      privacyPolicyUrl: `${SITE}/privacy/`,
      supportEmail: "hello@protologue.com",
      tools: TOOLS.map((t) => ({ name: t.name, title: t.title, description: t.description, inputSchema: t.inputSchema, annotations: t.annotations })),
    });
  }
  if (url.pathname !== "/mcp") return json(err(null, -32000, "Not found. The MCP endpoint is /mcp."), 404);

  if (request.method === "GET") {
    // No server-initiated stream in this stateless server.
    return new Response("Method Not Allowed", { status: 405, headers: { Allow: "POST, OPTIONS", ...CORS } });
  }
  if (request.method === "DELETE") return new Response(null, { status: 204, headers: CORS });
  if (request.method !== "POST") return new Response("Method Not Allowed", { status: 405, headers: CORS });

  let body;
  try {
    body = await request.json();
  } catch {
    return json(err(null, -32700, "Parse error"), 400);
  }

  let cached = null;
  const getData = async () => (cached ??= await loadData(fetchImpl));

  if (Array.isArray(body)) {
    const out = (await Promise.all(body.map((m) => handleMessage(m, getData)))).filter(Boolean);
    return out.length ? json(out) : new Response(null, { status: 202, headers: CORS });
  }
  const res = await handleMessage(body, getData);
  return res ? json(res) : new Response(null, { status: 202, headers: CORS });
}

export default {
  fetch(request) {
    return handle(request);
  },
};
