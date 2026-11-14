# Outreach kit

Drafts for earning links and citations from the places AI assistants and researchers draw on. Everything here is sent or opened by the owner, from the owner's own accounts. Send each item once; do not mass-submit or repeat a pitch that went unanswered.

## 1. Awesome-list pull requests

Open each PR from your own GitHub account. Before opening one, read the list's CONTRIBUTING file and match its section names, sort order and line format exactly. Maintainers close PRs that ignore the format.

| List | Section to look for | Line to add |
|---|---|---|
| promptslab/Awesome-Prompt-Engineering | Datasets, or Guides/Resources | `- [Protologue](https://protologue.com/) - Open (CC BY 4.0) taxonomy of 250+ prompting and LLM techniques, each with a citable definition, permanent ID and primary source. Also as JSON, CSV, SKOS and an MCP server.` |
| snwfdhmp/awesome-gpt-prompt-engineering | Resources / Guides | same line |
| dair-ai/Prompt-Engineering-Guide | Its "Additional Readings" or resources page (opened as an issue first, since that repo is a guide, not a list) | same line |
| punkpeye/awesome-mcp-servers | Knowledge & Memory, or Research | `- [protologue-org/protologue](https://github.com/protologue-org/protologue) ☁️ - Look up sourced, citable definitions of 250+ prompting and LLM techniques, with related techniques and primary sources. Remote server: https://mcp.protologue.com/mcp` (check the list's legend for the correct emoji set: language, cloud/local, OS) |
| kaushikb11/awesome-llm-agents | Resources / Learning | `- [Protologue](https://protologue.com/c/agents/) - Sourced definitions of agent patterns (ReAct, plan-and-execute, orchestrator-workers, harness engineering, context engineering) with their original papers.` |

More lists found on 2026-11-14, all active in the last month. The same rules apply: read CONTRIBUTING, match the format, one PR each.

| List | Stars | Fit |
|---|---|---|
| WangRongsheng/awesome-LLM-resources | 9k | General LLM resources; look for a "Tutorials/Courses" or "Other" section |
| Meirtz/Awesome-Context-Engineering | 3.3k | Link https://protologue.com/t/context-engineering/ and the agents branch |
| yzfly/awesome-context-engineering | 230 | Same as above |
| slavakurilyak/awesome-ai-agents | 2.9k | Link https://protologue.com/c/agents/ |
| Jenqyang/Awesome-AI-Agents | 1.3k | Same as above |
| Danielskry/Awesome-RAG | 1.4k | Link https://protologue.com/c/retrieval-tools/ (RAG, HyDE, GraphRAG, reranking, contextual retrieval) |
| brandonhimpfen/awesome-prompt-engineering | 255 | Main site line |
| natnew/Awesome-Prompt-Engineering | 115 | Main site line |

**PR title:** Add Protologue (open taxonomy of prompting and LLM techniques)

**PR description:**

> Protologue (https://protologue.com/) is an openly licensed (CC BY 4.0) reference for prompting and LLM techniques. Each of its 250+ entries has a permanent identifier, a one-to-two-sentence definition, synonyms, broader/narrower/related links, and the primary source that introduced the technique, with every source checked against the original. The data is downloadable as JSON, CSV and SKOS, archived on Zenodo (DOI 10.5281/zenodo.23304106), and available to agents through an MCP server. It is free, with no account, ads or paywall. I maintain it, so I'm happy to adjust the wording or section.

## 2. Survey and course authors

The most valuable links are from people who already write about prompting taxonomies. One personal email each; no follow-up beyond one polite reminder after two weeks.

**To:** Sander Schulhoff / Learn Prompting (authors of *The Prompt Report*, arXiv 2406.06608). Contact through learnprompting.org.

**Subject:** An open, citable companion to The Prompt Report's taxonomy

> Hi Sander,
>
> The Prompt Report was one of the sources I used to build Protologue (https://protologue.com/), an openly licensed taxonomy of prompting and LLM techniques. It's cited on our Prompt Optimization entry.
>
> Protologue gives each technique a permanent ID and URL, a standalone definition and its primary source, and it adds new terms as they appear: this week, for example, spec-driven development, evaluation awareness and diffusion language models. Everything is CC BY 4.0 and downloadable as JSON, CSV and SKOS, with a Zenodo DOI.
>
> Two things that might be useful to you: if you're updating the report or the Learn Prompting docs, Protologue could serve as a citable, versioned reference for definitions, and if you spot a definition you think is wrong, I'd like to fix it.
>
> Thanks for the report, it set the standard for this.
>
> [Name]
> Protologue, hello@protologue.com

Other recipients worth the same short note (adapt the first paragraph to their work): authors of recent prompting or agent surveys on arXiv, and instructors of courses that link to glossaries (for example, the Johns Hopkins spec-driven development class).

## 3. Answering questions (Stack Overflow, Reddit, GitHub issues)

Only where the entry genuinely answers the question, and write the answer itself in the post. Link the entry as the source, not as the answer. Good fits are questions that ask for a definition or a difference:

- "What's the difference between prompt injection and jailbreaking?" → https://protologue.com/compare/prompt-injection-vs-jailbreak/
- "RAG or fine-tuning?" → https://protologue.com/compare/rag-vs-fine-tuning/
- "What is a dark factory / software factory?" → https://protologue.com/t/dark-factory/
- "What does evaluation awareness mean?" → https://protologue.com/t/evaluation-awareness/

Disclose that you maintain the site when you link it. Subreddits such as r/PromptEngineering and r/LocalLLaMA remove undisclosed self-promotion.

## 4. New-term announcements

When a release adds a newly coined term, one short post on the channels you already use (newsletter, X, LinkedIn, Bluesky), naming the term and its primary source. A first clean definition with its source tends to get linked; promotion of the site as a whole does not.


## 5. Show HN

Post once, on a weekday morning US Eastern time, from your own HN account, and stay around for two hours to answer comments. Do not ask anyone to upvote it; HN penalizes that.

**Title:** Show HN: Protologue – an open, sourced glossary of 250 LLM and prompting techniques

**URL:** https://protologue.com/

**Text (first comment):**

> I built Protologue because definitions of LLM techniques are scattered across papers, vendor docs and blog posts, and many glossaries get the original source wrong.
>
> Each of the 253 entries has a permanent ID, a one-to-two-sentence definition, synonyms, links to broader and related techniques, and the paper or official doc that introduced it. Every source is opened and checked against its title and author before it goes in. New terms are added as they appear. This week's are dreaming (agents curating their own memory) and auto mode (a model approving an agent's actions), and recent ones include harness engineering and evaluation awareness. Vendor claims are labelled as vendor-reported.
>
> It's CC BY 4.0. You can download it as JSON, CSV, SKOS and Turtle, and the releases are archived on Zenodo with a DOI. Every page also has a Markdown version and an llms.txt, and there's a read-only MCP server (https://mcp.protologue.com/mcp) so agents can look terms up and cite them. The site is static, built by one Python script from YAML in a public GitHub repo.
>
> I'd welcome corrections, especially wrong attributions, and suggestions for terms that are missing.

## 6. Reddit

Read each subreddit's rules first; both below require disclosure for your own projects. Post once per subreddit, never cross-post the same text the same day.

**r/PromptEngineering:** title "I maintain an open glossary of 250 prompting techniques, each with its original paper. Corrections welcome". Body: two sentences on what it is, three example entries people often get wrong (Chain-of-Draft vs Chain-of-Density, both abbreviated CoD; self-consistency vs chain-of-thought; prompt injection vs jailbreak), the link, "I'm the maintainer", and an ask for missing terms.

**r/LocalLLaMA:** do not post the site itself. Post the substance of https://protologue.com/compare/flashattention-vs-pagedattention/ as a short text post ("FlashAttention vs PagedAttention: what each one fixes"), with the two papers linked, and the Protologue page as "I wrote this up here", with disclosure.

## 7. Cross-posted article (dev.to or Medium)

Publish with the canonical URL set to the Protologue page, so the copy credits the original instead of competing with it. On dev.to, put `canonical_url: https://protologue.com/compare/dreaming-vs-sleep-time-compute/` in the front matter.

**Title:** Three ways AI agents use their downtime: compaction, sleep-time compute and dreaming

> Agents that run for hours or across many sessions all hit the same wall. The context window fills, memory goes stale, and every new session starts by relearning what the last one knew. Three techniques use idle time to deal with this, and they are easy to confuse.
>
> **Context compaction** happens inside a session. When the context nears its limit, the conversation so far is summarized and the agent continues from the summary. The cost is that details, and sometimes instructions, can be lost in the summary. (https://protologue.com/t/context-compaction/)
>
> **Sleep-time compute** happens before a query. Given a context that will be asked about many times, such as a codebase or a document, the model reasons over it ahead of time and stores its inferences, so later answers need less test-time compute. It works best when the questions are predictable from the context (Lin et al., 2025). (https://protologue.com/t/sleep-time-compute/)
>
> **Dreaming** happens between sessions. A model rereads past session transcripts alongside the agent's stored memories. It merges duplicates, replaces stale or contradicted entries, and records new insights, writing a new memory store that a person can review before it is used. Anthropic popularized the term with Claude Managed Agents in 2026. Its reported gains are vendor-reported so far. (https://protologue.com/t/dreaming/)
>
> In short: compaction keeps one session going, sleep-time compute prepares for questions about a fixed context, and dreaming curates what an agent has learned across many sessions. Side-by-side table: https://protologue.com/compare/dreaming-vs-sleep-time-compute/

Every claim above comes from the three entries and their sources. If an entry changes, update the article.

## 8. More survey authors

Use the same email as section 2, adapted. Open each paper first and write to the corresponding author named on it.

- "The Periodic Table of LLM Reasoning: A Structured Survey of Reasoning Paradigms, Methods, and Failure Modes" (arXiv 2606.11470).
- "A Cross-Domain Evaluation of Prompting Techniques for Large Language Models" (arXiv 2610.24913).
- "Graph Engineering in the Era of LLM Agents" (arXiv 2608.21156).
