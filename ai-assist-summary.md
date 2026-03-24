# AI-Assisted Lab Build — Effort Summary

**Project:** EVPN/VXLAN Interop Lab (stubarea51)
**Date:** 2026-03-24
**AI Tool:** Claude Code (Claude Opus 4.6)

---

## Human Effort

~15-20 messages total across all sessions, each a short directive — roughly
**5-10 minutes of active interaction**.

### Messages

1. Initial lab setup / debugging transit routing & IPv6 BGP (previous session — a few back-and-forth exchanges)
2. "can you run through the evpn-vxlan-interop-testplan.md file and ensure all the tests are working? Create a new file adding a column to each test with the status"
3. "Can you confirm all the section 10 tests pass?"
4. "add the failure breakdown to a markdown file."
5. "Are there any changes needed to the diagram?"
6. "Can you push the changes up to GitHub?"
7. "can you add that to a markdown file and push it to github"

---

## What Was Produced

| Deliverable | Details |
|-------------|---------|
| 5 fixed device configs | IS-IS single-topology interop fix, MikroTik interface shifts (ether1→ether2 for Sherpa mgmt), missing twr-03 ether3 IP for transit routing |
| 199-test validation | Full execution of test plan across 10 sections — 179 PASS / 14 FAIL / 6 INFO |
| Test results doc | `evpn-vxlan-interop-testplan-results.md` — every test with status column |
| Failure analysis | `evpn-vxlan-interop-failure-analysis.md` — 6 categories with root cause, impact, and remediation |
| 3 corrected diagrams | SVG, draw.io, and manifest comments aligned to actual deployed state |
| .gitignore | Excludes Sherpa-generated lab artifacts (SSH keys, config, lab-info) |

---

## Key Debugging (Handled Autonomously)

- **Transit routing failure:** twr-03 had no IP on ether3 → twr-02 IS-IS SPF couldn't resolve next-hop → agg-01 ECMP failed. Fixed by adding the missing IP and toggling IS-IS.
- **IPv6 BGP sessions stuck in Active:** IOS-XE used IS-IS multi-topology for IPv6, MikroTik uses single-topology — incompatible TLVs. Fixed by switching IOS-XE to single-topology.
- **Diagram/manifest drift:** IPv6 addresses in diagrams didn't match configs (non-existent addresses shown, hex notation mismatches). Corrected across all three diagram files.
