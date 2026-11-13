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
| `confidence` | yes | `HIGH ✓`, `BREAKING ⚠`, or `LOW` |
| `window` | yes | `initial-90d`, `expanded-180d`, or the user's specified window |
| `verification_status` | yes | `opened`, `homepage-only`, `user-provided`, or `needs-follow-up` |

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
