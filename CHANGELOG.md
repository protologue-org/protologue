# Changelog

## 1.2.2 (2026-10-14)

**Added**
- Recursive Language Model (PTL-0213): an inference strategy that keeps a long prompt outside the context window and processes it through recursive self-calls. Source: Zhang, Kraska and Khattab (2025).
- Agentic Context Engineering (PTL-0214): improving an application by incrementally updating its context as an evolving playbook. Source: Zhang et al. (2025).
- Sleep-time Compute (PTL-0215): computation done on a context before queries arrive. Source: Lin et al. (2025).

## 1.2.1 (2026-10-14)

Weekly review. All 211 source links were re-checked: every arXiv ID matches its cited title and first author, and every documentation link resolves.

**Added**
- Harness Engineering (PTL-0212): the design of the software around a model that turns it into an agent. Sources: OpenAI's "Harness engineering" post (Lopopolo, 2026) and Barbaste et al. (2026).

**Updated**
- Extended Thinking: the fixed thinking budget is deprecated on Claude 4.6 models and rejected by Claude 4.7 and later, which use adaptive thinking with an effort level. The source title is now "Extended thinking", matching Anthropic's page.
- Prefill: states more precisely what Anthropic's documentation says. From Claude 4.6, prefilling the final assistant turn returns an error. Earlier models still accept it, and assistant messages elsewhere in the conversation are unaffected.
- Model Context Protocol: the specification source now points to the current specification (version 2026-07-28) instead of the site's home page.
- Needle in a Haystack: the source repository was renamed to gkamradt/needle-in-a-haystack.

**Could not verify**
- Two DOI links (BM25: 10.1561/1500000019; hybrid search: 10.1145/1571941.1572114) and one x.com post (vibe coding). The publishers' sites and x.com block automated fetching, so these links are unchanged.
