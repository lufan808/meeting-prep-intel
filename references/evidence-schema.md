# Evidence Schema

Use one record for every material signal before synthesis. The record can live in notes, a spreadsheet, or an intermediate Markdown section; the Skill does not require a database or a specific runtime.

## Record fields

| Field | Required | Meaning |
|---|---:|---|
| `id` | yes | Stable local identifier, such as `A-01` or `D-02` |
| `stream` | yes | `A` own voice, `B` community reaction, `C` third-party framing, or `D` official baseline |
| `date` | yes when available | Publication, event, or update date; mark an undated item explicitly |
| `source_url` | yes | URL actually opened during research |
| `source_type` | yes | Official, personal, media, community, user-provided, or other |
| `speaker` | yes | Who made the statement or performed the action |
| `claim` | yes | The concrete fact, action, or statement supported by the source |
| `quote_or_paraphrase` | yes | Short quote or faithful paraphrase; do not reproduce long source text |
| `framing` | yes | How the source presents or interprets the signal |
| `identity_status` | yes for identity claims | `official`, `self-reported`, `externally-described`, or `user-provided` |
| `confidence` | yes | `HIGH`, `MEDIUM`, or `LOW`; strength of support, not recency |
| `freshness` | yes | `BREAKING`, `RECENT`, or `OLDER`; timing, not truthfulness |
| `window` | yes | `initial-90d`, `expanded-180d`, or the user's specified window |
| `verification_status` | yes | `opened`, `homepage-only`, `blocked`, `user-provided`, or `needs-follow-up` |
| `underlying_event_id` | yes for repeated reports | Shared identifier for articles repeating the same announcement; count as one event |
| `conflicts_with` | when applicable | IDs of records making incompatible claims |

## Module hand-offs

The workflow has six logical modules. They are boundaries for reasoning, not required services or packages:

1. **Collector** — gathers dated signals into evidence records.
2. **Calibrator** — checks identity, source type, date, attribution, and confidence.
3. **Comparator** — groups the records by own voice, external framing, and community reaction.
4. **Synthesizer** — turns calibrated records into the current narrative and talking points.
5. **Renderer** — writes the Markdown or document output using the public template.
6. **Auditor** — checks provenance, time window, uncertainty, and information boundaries.

If the runtime cannot run parallel tasks or a source-enrichment layer, keep the same record fields and run the modules sequentially. Do not replace a missing tool with guessed URLs or invented evidence.

## Classification rules

- A supplier, production agency, customer, partner, or vendor case study can support project participation, but not primary proof of a current job title.
- A user-provided document is a separate evidence layer. It can supply project facts and questions to verify, but it is not public verification.
- An assistant inference must be marked as an inference and linked to the records that support it.
- A third-party post must never be attributed to the target person merely because it mentions them.
- Do not treat a source's date as evidence of accuracy. A new report can have low confidence; an older official biography can establish background but not a current role.
- Preserve an evidence ledger while researching, even if it remains an intermediate artifact. Report material gaps and conflicts in the brief.
