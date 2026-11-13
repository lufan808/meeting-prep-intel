# Input and workflow states

Record the user's request before research. A note or Markdown front matter is enough; no workflow platform is required.

| Field | Rule |
|---|---|
| `raw_request` | Keep the user's wording when available, especially for a document output. |
| `person` | Required. Resolve ambiguous names before attributing claims. |
| `organization_or_role` | Optional identity clue; verify the current role independently. |
| `meeting_goal` | Keep the user's question or decision as the research focus. If absent, prepare a general first-meeting brief. |
| `initial_window` | User-specified range, otherwise the last 90 days. |
| `effective_window` | Start equal to initial; expand from 90 to 180 days only when evidence for the meeting goal is insufficient. |
| `provided_materials` | Optional; list each supplied file or link and its separate evidence status. |
| `output_destination` | Markdown by default; use a document when requested and supported. |

## State transitions

`intake → identity → collecting → calibrating → synthesizing → auditing → delivered`

- At `identity`, proceed only with a resolved person. If two people remain plausible, ask for an identity clue and pause research.
- At `collecting`, search each of the four lines. Mark a line `found`, `searched-no-signal`, or `blocked`; don't silently omit a line. A lack of community response is a valid finding.
- At `calibrating`, keep a source ledger with dates and attribution. Repeated reports of one original announcement count as one underlying signal.
- At `synthesizing`, distinguish what the person said, what outsiders said, and what the assistant infers. If the evidence is too thin for a confident narrative, write a shorter brief with explicit gaps.
- At `auditing`, check every material claim against the ledger and run the optional structural validator. A validator pass never proves a source was opened.
- At `delivered`, verify any requested document was actually written and return its link. If document writing fails, give the Markdown result and state what failed.

If a source is inaccessible, try another appropriate source once, then mark the blocked item and continue. If a user's material conflicts with a public source, show both claims and their provenance; ask the user only if the conflict changes the meeting goal or desired output.
