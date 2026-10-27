# Outreach kit

Drafts for earning links and citations from the places AI assistants and researchers draw on. Everything here is sent or opened by the owner, from the owner's own accounts. Send each item once; do not mass-submit or repeat a pitch that went unanswered.

## 1. Awesome-list pull requests

Open each PR from your own GitHub account. Before opening one, read the list's CONTRIBUTING file and match its section names, sort order and line format exactly. Maintainers close PRs that ignore the format.

| List | Section to look for | Line to add |
|---|---|---|
| promptslab/Awesome-Prompt-Engineering | Datasets, or Guides/Resources | `- [Protologue](https://protologue.com/) - Open (CC BY 4.0) taxonomy of 230+ prompting and LLM techniques, each with a citable definition, permanent ID and primary source. Also as JSON, CSV, SKOS and an MCP server.` |
| snwfdhmp/awesome-gpt-prompt-engineering | Resources / Guides | same line |
| dair-ai/Prompt-Engineering-Guide | Its "Additional Readings" or resources page (opened as an issue first, since that repo is a guide, not a list) | same line |
| punkpeye/awesome-mcp-servers | Knowledge & Memory, or Research | `- [protologue-org/protologue](https://github.com/protologue-org/protologue) ☁️ - Look up sourced, citable definitions of 230+ prompting and LLM techniques, with related techniques and primary sources. Remote server: https://mcp.protologue.com/mcp` (check the list's legend for the correct emoji set: language, cloud/local, OS) |
| kaushikb11/awesome-llm-agents | Resources / Learning | `- [Protologue](https://protologue.com/c/agents/) - Sourced definitions of agent patterns (ReAct, plan-and-execute, orchestrator-workers, harness engineering, context engineering) with their original papers.` |

**PR title:** Add Protologue (open taxonomy of prompting and LLM techniques)

**PR description:**

> Protologue (https://protologue.com/) is an openly licensed (CC BY 4.0) reference for prompting and LLM techniques. Each of its 230+ entries has a permanent identifier, a one-to-two-sentence definition, synonyms, broader/narrower/related links, and the primary source that introduced the technique, with every source checked against the original. The data is downloadable as JSON, CSV and SKOS, archived on Zenodo (DOI 10.5281/zenodo.23304106), and available to agents through an MCP server. It is free, with no account, ads or paywall. I maintain it, so I'm happy to adjust the wording or section.

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
