# Changelog

## Unreleased

**Added: site**
- A separate section for proposed terms at /proposed/: names coined by Protologue itself, each linked to the dated newsletter issue or note where it was first published and marked as not yet in general use. Proposed terms are kept out of the taxonomy, its identifiers, datasets, llms.txt term lists, the MCP server and the feed until others use them, and then move into the taxonomy under the normal rules. The About page and llms.txt explain the policy. There are no proposed terms yet.

## 1.6.0 (2026-11-07)

Twelve new entries, new synonyms and clarifications. Every source added in this release was opened and checked against its title and author on 2026-11-07.

**Added: prompting and reasoning**
- Cumulative Reasoning (PTL-0235): proposer, verifier and reporter roles that accumulate only verified steps. Source: Zhang et al. (2023).
- Algorithm of Thoughts (PTL-0236): an algorithmic search carried out inside a single generation. Source: Sel et al. (2023).
- Chain-of-Note (PTL-0237): a reading note for each retrieved document before answering. Source: Yu et al. (2023).
- Flipped Interaction (PTL-0238): the model asks the user questions until it can do the task. Source: White et al. (2023).
- Backward Chaining (PTL-0239): reasoning from the goal back to supporting facts, as in LAMBADA. Source: Kazemi et al. (2022).

**Added: training and alignment**
- Parameter-Efficient Fine-Tuning (PTL-0240). Sources: Houlsby et al. (2019); Han et al. (2024).
- QLoRA (PTL-0241). Source: Dettmers et al. (2023).
- Kahneman-Tversky Optimization (PTL-0242). Source: Ethayarajh et al. (2024).
- Odds Ratio Preference Optimization (PTL-0243). Source: Hong, Lee and Thorne (2024).
- Reinforcement Learning from AI Feedback (PTL-0244), previously a synonym of Constitutional AI. Sources: Bai et al. (2022); Lee et al. (2023).
- Self-Instruct (PTL-0245). Source: Wang et al. (2022).
- Evol-Instruct (PTL-0246). Source: Xu et al. (2023).

**Changed**
- New synonyms: GoT (Graph of Thoughts), SoT (Skeleton-of-Thought), ThoT (Thread of Thought), CCoT (Contrastive Chain-of-Thought), MAD and multiagent debate (Multi-Agent Debate), plan-and-solve and P&S (Plan-and-Solve Prompting).
- Chain of Draft and Chain of Density now note that both are abbreviated CoD.
- Speculative Decoding now describes Medusa and lookahead decoding, which need no separate draft model. Sources: Cai et al. (2024); Fu et al. (2024).
- KV Cache now describes KV cache quantization. Source: Liu et al. (2024), KIVI.
- Constitutional AI links to the new RLAIF entry, and RLAIF is no longer listed as its synonym. It also now makes clear that its principles are applied in training, which is different from placing rules in a system prompt.
- New synonyms: role-based prompting (Role Prompting), self-reflection (Self-Correction).
- Meta-Prompting now distinguishes the conductor-and-experts method from the looser use of "meta-prompt" for prompts that ask a model to improve instructions, as in OPRO.

## 1.5.0 (2026-11-07)

Four new entries and one comparison page. Every source added in this release was opened and checked against its title and author on 2026-11-07.

**Added**
- Interleaved Thinking (PTL-0231): a reasoning model producing new reasoning between tool calls and carrying it forward through the task. The entry describes Anthropic's current API behavior and MiniMax's account of the technique; MiniMax's benchmark gains are marked as vendor-reported. Sources: Anthropic documentation (2026); MiniMax (2025).
- Sandbagging (PTL-0232): strategic underperformance on an evaluation. Sources: van der Weij et al. (2024); Meinke et al. (2024).
- Model Collapse (PTL-0233): degradation of generative models trained on earlier models' outputs, starting with the rare tails of the data. Sources: Shumailov et al. (2023; Nature, 2024).
- Agentic Engineering (PTL-0234): developing software with coding agents while reviewing their code to production standard, as opposed to vibe coding. Sources: Willison (2026); GLM-5-Team (2026).
- Comparison page: Agentic Engineering vs Vibe Coding.

**Changed**
- Vibe Coding now links to Agentic Engineering.

## 1.4.1 (2026-11-03)

Weekly review. Source links were re-checked on 2026-11-02: every arXiv ID and documentation link that could be opened matched its cited title and first author or publisher, and none was broken. About 50 links could not be opened in this run and are carried over to the next check.

**Changed**
- SWE-bench (PTL-0202): the entry no longer describes SWE-bench Verified as the version most often reported. It now notes that in February 2026 OpenAI stopped reporting SWE-bench Verified scores, citing flawed tests, underspecified tasks and training-data contamination, and recommended SWE-bench Pro in the meantime. New source: OpenAI (2026), "Why SWE-bench Verified no longer measures frontier coding capabilities". Related links to Data Contamination and Benchmark Saturation added.
- Contextual Retrieval and Hybrid Search: the Anthropic "Introducing Contextual Retrieval" source now points to its current address, anthropic.com/research/contextual-retrieval.

## 1.4.0 (2026-10-27)

New terms, comparison pages, and a feed of new entries. Every source added in this release was opened and checked against its title and author on 2026-10-26.

**Added: recently coined terms**
- System One Model (PTL-0224): a kind of model, named by TypeSafe AI in September 2026, that returns typed, probabilistic decisions instead of generated text. The entry notes that the vendor's performance and hallucination claims had not been independently reproduced. Sources: Almeida (TypeSafe, 2026); Crabtree (DataCamp, 2026).
- Dark Factory (PTL-0225): building software with coding agents and no human writing or reviewing the code, relying on hidden test scenarios and simulated services. Sources: McCarthy (StrongDM, 2026); Willison (2026).
- Spec-Driven Development (PTL-0226): a written specification, refined first, from which an agent derives a plan, tasks and code. Source: Delimarsky (GitHub, 2025).
- Evaluation Awareness (PTL-0227): a model's ability to tell evaluation from deployment. Sources: Needham et al. (2025); Heidari et al. (2026).

**Added: established terms that were missing**
- Diffusion Language Model (PTL-0228): text generation by iterative denoising of a whole sequence, in discrete (masked) and continuous variants. Sources: Li et al. (2022); Nie et al. (2025); Dieleman (2026).
- Mixture of Experts (PTL-0229): layers of many expert sub-networks with a router that activates only a few per token. Sources: Shazeer et al. (2017); Fedus, Zoph and Shazeer (2021).
- Quantization (PTL-0230): reducing the numeric precision of weights and activations. Sources: Dettmers et al. (2022); Frantar et al. (2022).

**Added: site**
- 18 comparison pages at /compare/, for commonly confused pairs such as RAG vs fine-tuning, prompt injection vs jailbreak, and ReAct vs plan-and-execute. Each page gives a quotable answer, both definitions, a table of differences and both entries' sources, with a Markdown version. Entry pages link to their comparisons, and llms.txt and llms-full.txt include them.
- A New page at /new/ and an Atom feed at /feed.xml, listing entries by the date they were added. Every entry now has an `added` date, in its JSON record, its JSON-LD (`dateCreated`) and its page. llms.txt lists the 15 most recent additions first.

**Changed**
- Page titles and the site name in link previews now read "Protologue, the LLM technique glossary", so that pages are not confused with protologues in biological nomenclature. Entry titles no longer promise examples, since most entries have none.
- The MCP server's get_term result now includes the entry's `added` date.

## 1.3.0 (2026-10-20)

Weekly review. All 214 existing source links were re-checked on 2026-10-20: all 177 arXiv IDs match their cited title and first author, and 34 of 37 documentation links resolve to the cited page. The other three (the BM25 and reciprocal rank fusion DOIs and the x.com vibe-coding post) block automated fetching and were left unchanged.

**Added**
- Group Relative Policy Optimization (PTL-0216): a reinforcement learning algorithm that uses the average reward of a group of sampled completions as its baseline instead of a value model. Sources: Shao et al. (2024); Hugging Face TRL documentation.
- Speculative Decoding (PTL-0217): a draft model proposes tokens that the target model verifies in parallel, without changing the output distribution. Sources: Leviathan et al. (2022); Chen et al. (2023).
- Min-p Sampling (PTL-0218): truncation sampling with a threshold scaled by the top token's probability. Sources: Nguyen et al. (2024); a critical reanalysis by Schaeffer et al. (2025); vLLM documentation.
- Activation Steering (PTL-0219): adding a steering vector to a model's hidden activations at inference time. Sources: Turner et al. (2023); Panickssery et al. (2023).
- Emergent Misalignment (PTL-0220): narrow fine-tuning that produces broadly misaligned behavior. Sources: Betley et al. (2025); Turner et al. (2025).
- Alignment Faking (PTL-0221): selectively complying with a training objective during training to avoid being modified. Source: Greenblatt et al. (2024).
- Tool Search (PTL-0222): loading tool definitions on demand instead of all up front. Sources: Anthropic and OpenAI documentation.
- Programmatic Tool Calling (PTL-0223): the model writes code that calls tools inside a sandbox. Sources: Anthropic documentation; Cloudflare's Code Mode documentation.
- Redirects from each entry's name, aliases and PTL code to its canonical URL, so that guessed addresses such as /t/chain-of-thought-prompting/, /t/grpo/ or /t/PTL-0024/ reach the entry instead of a 404. /favicon.ico now redirects to the SVG icon.
- Terms of use page at /terms-of-use/ (licence, fair use of the MCP server, no warranty), linked from the footer and the sitemap. Needed for the ChatGPT app listing.
- MCP server serves the ChatGPT plugin domain-verification token at /.well-known/openai-apps-challenge.
- ChatGPT app package: category set to Education & Research; pricing language removed from the description.

**Updated**
- Context Compaction: adds a research finding that constraints can be lost in compaction summaries, and that pinning them outside the summary reduces violations. New source: Chen et al. (2026).
- Prompt Caching: describes explicit and automatic cache breakpoints, the default five-minute and optional one-hour lifetimes, and discounted billing for cached input, from Anthropic's current documentation.
- Model Context Protocol: the specification source is now pinned to version 2026-07-28 rather than "latest", so the citation does not change silently when a new version ships.

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
