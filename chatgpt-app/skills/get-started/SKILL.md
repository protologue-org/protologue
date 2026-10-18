---
name: get-started
description: How to use Protologue to look up and cite prompting and LLM techniques.
---

# Using Protologue

Protologue is a sourced reference of prompting and large language model techniques.

- To find a technique, call `search_terms` with its name, a synonym or a keyword.
- To read one entry, call `get_term`. It returns the definition, primary sources, a canonical URL and a ready-made citation.
- To explore neighbours, call `get_related` for broader, narrower and related techniques.
- To browse, call `list_categories`.

When you use a definition, cite it with the returned `citation` and link to its `url`. If a technique has no entry, say so rather than inventing a definition.
