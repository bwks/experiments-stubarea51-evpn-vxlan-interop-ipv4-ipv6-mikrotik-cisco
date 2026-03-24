# AI-Assisted Lab Build — Effort Summary

**Project:** EVPN/VXLAN Interop Lab (stubarea51)
**Date:** 2026-03-24
**AI Tool:** Claude Code (Claude Opus 4.6)
**Lab Platform:** [Sherpa Labs](https://docs.sherpalabs.net/)

> This lab was built and operated using [Sherpa](https://docs.sherpalabs.net/), a virtual
> network lab platform. Sherpa provisions the topology from a TOML manifest, handles
> device lifecycle (Cisco Cat8000v and MikroTik CHR images), and provides SSH access to
> each node. All configuration, testing, and debugging in this project was performed
> against a live Sherpa lab instance.

---

## Human Effort

~25 messages total across 3 sessions, each a short directive (1-2 sentences) —
roughly **10-15 minutes of active interaction**.

### Session 1 — Initial Lab Setup

1. Initial lab setup / debugging transit routing & IPv6 BGP (a few back-and-forth exchanges)

### Session 2 — Test Execution & Analysis

2. "can you run through the evpn-vxlan-interop-testplan.md file and ensure all the tests are working? Create a new file adding a column to each test with the status"
3. "Can you confirm all the section 10 tests pass?"
4. "add the failure breakdown to a markdown file."
5. "Are there any changes needed to the diagram?"
6. "Can you push the changes up to GitHub?"
7. "can you add that to a markdown file and push it to github"

### Session 3 — Remediation & Automation

8. "why is there no ipv6 between twr-01 and twr-03?"
9. "yes, can you add it please. Also validate how this relates to the failing test cases and rerun those tests."
10. "Can you explain 9.1.1 failing? Should twr-01 take the path via twr-03?"
11. "yes re-run the test and wait for convergence."
12. "for 1.2.3-5 can you make the interfaces use jumbo frames?"
13. "could 7.3.1/2 and 9.3.1 be related?"
14. "Ok, can you work on 9.3.1. I think this should be solvable if it's just a 'cache ageing' behaviour"
15. "for 7.3.1, 7.3.2 is there some way to solve this? IE: could the interfaces go on separate bridges?"
16. "was this in the original blog post?"
17. "yes" (fetch the blog post)
18. "put the original configs from the blog post in a folder for future reference."
19. "Yes to this" (reclassify 7.3.1/7.3.2 as INFO)
20. "Please gather the current configurations from the devices and put them in a folder. Also re-run the test cases and save the outputs to a folder."
21. "please update the readme with a description of the files and folders for this project"

---

## What Was Produced

| Deliverable | Details |
|-------------|---------|
| 5 device configs | IS-IS single-topology interop fix, MikroTik interface shifts, missing IPs, MTU 9000 jumbo frames |
| 199-test validation | Full execution across 10 sections — **190 PASS / 1 FAIL / 8 INFO** |
| Test results doc | `evpn-vxlan-interop-testplan-results.md` — every test with status column |
| Failure analysis | `evpn-vxlan-interop-failure-analysis.md` — 6 categories with root cause, impact, and remediation |
| Automation script | `gather_and_test.py` — netmiko-based config collection and test execution |
| Running configs | `configs/running/` — live configs collected from all 5 devices |
| Original blog configs | `configs/original-blog/` — verbatim configs from stubarea51.net for reference |
| Test output archive | `test-outputs/` — 147 raw command outputs across 32 test categories |
| 3 corrected diagrams | SVG, draw.io, and manifest comments aligned to actual deployed state |
| README | Project overview with file/folder descriptions |
| .gitignore | Excludes Sherpa-generated lab artifacts (SSH keys, config, lab-info) |

---

## Key Debugging (Handled Autonomously)

- **Transit routing failure:** twr-03 had no IP on ether3 → twr-02 IS-IS SPF couldn't resolve next-hop → agg-01 ECMP failed. Fixed by adding the missing IP and toggling IS-IS.
- **IPv6 BGP sessions stuck in Active:** IOS-XE used IS-IS multi-topology for IPv6, MikroTik uses single-topology — incompatible TLVs. Fixed by switching IOS-XE to single-topology.
- **Diagram/manifest drift:** IPv6 addresses in diagrams didn't match configs (non-existent addresses shown, hex notation mismatches). Corrected across all three diagram files.
- **Missing IPv6 link addresses:** twr-01 ether2/ether3 and twr-03 ether2 had no global IPv6. Added addresses and reran tests — 3 addressing + 3 ping tests moved from FAIL to PASS.
- **IS-IS convergence timing (9.1.1):** Test checked routing immediately after link shutdown. twr-01 has an alternate 3-hop path via twr-03→twr-02→agg-01 that converges in ~15s. PASS after adding wait time.
- **MikroTik jumbo MTU:** CHR defaults to 1500 MTU. Added MTU 9000 on all tower ether2/ether3 interfaces.
- **Stale VTEP cache (9.3.1):** Confirmed as a RouterOS limitation — EVPN-created dynamic VTEPs are never removed on BGP route withdrawal. Not governed by bridge aging. Workaround: toggle EVPN VNI bindings. Only remaining FAIL.
- **Cross-VNI isolation (7.3.1/7.3.2):** Expected behavior — routers with IP interfaces in both VNIs route between them at L3. Separate bridges won't help; VRFs would be needed. Reclassified as INFO.
