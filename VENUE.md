# Venue recommendation (Fable, 2026-08-29)

## Strategy
1. **Do the major revision first** (trim-corrected re-analysis, semi-synthetic attribution-accuracy
   experiment, CIs, related work, retitle) — highest leverage regardless of venue. See REVIEW.md.
2. **Primary target: Transportation Research Part C** (methodology framing) — or **TR-D** if leaning
   on the emissions story (convert excess fuel to CO2, fleet-level intervention decomposition).
3. **Backup 1: Engineering Applications of AI (EAAI)** — applied-ML framing, faster, Elsevier-to-Elsevier.
4. **Backup 2: IEEE T-ITS** (fleet-management framing; slow, 3-6mo first decision).
5. **Floor / submit-now: IEEE Access** — the paper as-is is ~Access quality; ~2-3mo to publish.
6. Post arXiv preprint (eess.SY / cs.LG) at first submission to timestamp the claim.

## Ranked venues
| Venue | Fit | Bar | OA/APC (approx, verify) | 1st decision |
|---|---|---|---|---|
| TR-C (Elsevier) | Strong (VED home turf) | High (~15-20%) | Hybrid; gold ~$3.5-4k | 8-14 wk |
| TR-D (Elsevier) | Good IF reframed to emissions | High | Hybrid ~$3.5-4k | 8-12 wk |
| EAAI (Elsevier) | Very good (applied ML) | Mod-high, attainable | Hybrid ~$3.2-3.7k | 6-10 wk (fast) |
| IEEE T-ITS | Good (malfunction arm reads as diagnostics risk) | High | Hybrid; OA ~$2.6k | 3-6 mo (slow) |
| IEEE T-VT | Moderate (dominated) | High | IEEE terms | 2-4 mo |
| IEEE Sensors / Sensors MDPI | Marginal (no sensing contribution) | Mod | ~$2.6-2.7k | 4-8 wk |
| ESWA (Elsevier) | Good (general applied ML) | Mod, high desk-reject | gold ~$2.8-3.5k | 8-16 wk |
| IEEE Access | Everything in scope (mega-journal) | Low-mod (~30%+) | gold ~$2.0k | 4-7 wk |

## Avoid
- **Applied Energy**: wants energy-system-level impact; likely desk-reject for a per-vehicle ICE study.
- **IEEE Sensors / Sensors (MDPI)**: no sensing contribution; reviewers will flag it.
- **T-VT**: dominated by T-ITS (ITS framing) and EAAI (ML framing).
- Special-issue solicitation emails on these popular datasets (bait from lower-tier venues).

## Tradeoff
IEEE Access now = permanent, wastes a genuinely novel design. Revision is bounded (a few analysis
sessions + minutes-to-hours compute); the real delay is TR-C/TR-D review (6-10 mo to accept). Do the
revision unless an external deadline forces a fast record.
