# Directory listings kit

Copy for listing the Protologue MCP server in agent directories. Keep every listing consistent with this file.

## Shared facts

| Field | Value |
|---|---|
| Name | Protologue |
| Endpoint | `https://mcp.protologue.com/mcp` (streamable HTTP, no auth) |
| Official MCP Registry name | `com.protologue/protologue` |
| Website | https://protologue.com/ |
| Docs URL | https://protologue.com/mcp/ |
| Privacy policy URL | https://protologue.com/privacy/ |
| Support | hello@protologue.com, or GitHub issues |
| Source | https://github.com/protologue-org/protologue (server in `mcp/`) |
| License of content | CC BY 4.0 |
| Icon | `static/assets/logo.png` |
| Categories | Research, Education, Developer tools, Reference |
| Tools | `search_terms`, `get_term`, `get_related`, `list_categories`. All read-only (`readOnlyHint: true`, `destructiveHint: false`, `openWorldHint: false`) |

**One-liner (under 200 characters).** Sourced, citable definitions of 230+ prompting and LLM techniques, each with its primary source, synonyms and related techniques.

**Description (under 2,000 characters).** Protologue is an openly licensed (CC BY 4.0) reference taxonomy of prompting and large language model techniques, from chain-of-thought and ReAct to context engineering and prompt injection. Each entry has a permanent identifier, a standalone definition, synonyms, broader, narrower and related techniques, and the primary source (paper or official documentation) that introduced it. Every source is checked against the original.

The server lets an assistant look up a technique by name or synonym, read its sourced definition, explore related techniques and browse the taxonomy's branches. Answers come with a ready-made citation and a canonical link, so the assistant can cite where a definition came from instead of guessing. The server is free, read-only and needs no account. The taxonomy is updated weekly as new techniques appear.

## Test prompts (with expected behaviour)

1. "Using Protologue, what is chain-of-thought prompting and who introduced it?"
   Calls `get_term` and answers with the definition, citing Wei et al., 2022, and https://protologue.com/t/chain-of-thought/.
2. "Look up ReAct in Protologue and list the techniques it is related to."
   Calls `get_related` and lists broader, narrower and related entries.
3. "Search Protologue for techniques about retrieval."
   Calls `search_terms` and returns entries such as Retrieval-Augmented Generation and HyDE, with definitions.
4. "Which Protologue branch covers prompt injection, and what else is in it?"
   Calls `get_term` or `list_categories` and names the Security & Adversarial Prompting branch and its entries.
5. "Is 'quantum prompting' in Protologue?"
   Calls `search_terms` or `get_term` and reports that there is no entry, without making one up.

## Where it is listed

| Directory | How | Status |
|---|---|---|
| Official MCP Registry | `mcp-publisher publish` from `mcp/server.json` (owner's registry key) | Listed since 2026-10-11 at v1.0.0. Republish to update to v1.2.0 |
| Glama | Claim the connector page; `glama.json` at the repo root lists the maintainer | To do |
| PulseMCP | Check whether it already appears from the official registry; otherwise pulsemcp.com/submit | To do |
| MCP.so | mcp.so/submit, Remote Server tab | To do |
| Smithery | smithery.ai/new with the endpoint URL, then Settings → Verification | To do |
| Claude Connectors Directory | claude.ai/directory/manage → Submit new → MCP connector | To do |
| ChatGPT apps | platform.openai.com submission portal (needs individual or business verification) | Business verification in review since 2026-10-18 |
| GitHub MCP Registry (VS Code, Copilot) | github.com/mcp; populated from the official MCP Registry, so republishing there is the step | Check after republish |
| Cursor Directory | cursor.directory/mcp, "Submit" with the endpoint URL | To do |
| mcpservers.org / awesome-mcp-servers | Pull request adding one line under a Knowledge or Research section | To do (draft in `docs/outreach.md`) |

Status checked 2026-10-26: a web search found no Protologue listing on Glama, Smithery, PulseMCP or MCP.so yet.

Update this table as listings go live.
