# EVPN/VXLAN Interop Lab — Failure Analysis

**Test Date:** 2026-03-24
**Overall:** 186 PASS / 7 FAIL / 6 INFO out of 199 tests

---

## Summary by Section

| Section | Tests | Pass | Fail | Info |
|---------|-------|------|------|------|
| 1 — Physical / Link Layer | 15 | 12 | 3 | 0 |
| 2 — IP Addressing | 31 | 31 | 0 | 0 |
| 3 — IS-IS Underlay | 53 | 53 | 0 | 0 |
| 4 — BGP Control Plane | 25 | 25 | 0 | 0 |
| 5 — EVPN Control Plane | 17 | 17 | 0 | 0 |
| 6 — VXLAN Data Plane | 18 | 18 | 0 | 0 |
| 7 — Overlay Connectivity | 14 | 12 | 2 | 0 |
| 8 — MAC Learning | 3 | 3 | 0 | 0 |
| 9 — Convergence & Resilience | 8 | 6 | 2 | 0 |
| 10 — Interop-Specific | 15 | 9 | 0 | 6 |
| **Total** | **199** | **185** | **8** | **6** |

---

## Failure Breakdown

### 1. MikroTik MTU 1500 (3 failures)

| Test | Device | Expected | Actual |
|------|--------|----------|--------|
| 1.2.3 | twr-01 ether2, ether3 | 9000+ | 1500 |
| 1.2.4 | twr-02 ether2, ether3 | 9000+ | 1500 |
| 1.2.5 | twr-03 ether2, ether3 | 9000+ | 1500 |

**Root Cause:** MikroTik CHR defaults to 1500-byte MTU on Ethernet interfaces. The original blog configs did not set jumbo frames on MikroTik devices.

**Impact:** VXLAN adds 50 bytes of encapsulation overhead. With a 1500 MTU underlay, the effective overlay MTU is ~1450 bytes. Default-sized pings (56 bytes) succeed, but large payloads will fragment or fail. IOS-XE devices (core-01, agg-01) are correctly set to MTU 9000.

**Remediation:** Add `/interface ethernet set ether2 mtu=9000` and same for ether3 on all three MikroTik towers. Note: MikroTik CHR virtual interfaces may not support jumbo MTU depending on the hypervisor/virtio configuration.

---

### 2. ~~Missing IPv6 Link Addresses (3 failures)~~ — RESOLVED

| Test | Device | Interface | Expected Address | Actual |
|------|--------|-----------|------------------|--------|
| 2.2.5 | twr-01 | ether2 | 3fff:1ab:d50:d0::2/64 | No global IPv6 — link-local only |
| 2.2.6 | twr-01 | ether3 | 3fff:1ab:d50:d8::9/64 | No global IPv6 — link-local only |
| 2.2.9 | twr-03 | ether2 | 3fff:1ab:d50:d8::10/64 | No global IPv6 — link-local only |

**Root Cause:** The original blog configs for twr-01 and twr-03 did not assign global IPv6 addresses to all data-plane interfaces. twr-02 has IPv6 on both ether2 and ether3; twr-03 has IPv6 on ether3 only (added during deployment).

**Impact:** Minimal. IS-IS runs over link-local addresses and forms adjacencies regardless of global IPv6. IPv6 loopback-to-loopback reachability works because IS-IS distributes /128 routes via the link-local next-hops. The only impact is inability to ping these specific link addresses.

**Remediation:** Add the missing addresses:
```
# twr-01
/ipv6 address add address=3fff:1ab:d50:d0::2/64 advertise=no interface=ether2
/ipv6 address add address=3fff:1ab:d50:d8::9/64 advertise=no interface=ether3

# twr-03
/ipv6 address add address=3fff:1ab:d50:d8::10/64 advertise=no interface=ether2
```

---

### 3. ~~IPv6 Link Ping Failures (3 failures)~~ — RESOLVED

| Test | From | To | Target IP | Result |
|------|------|----|-----------|--------|
| 2.5.3 | agg-01 | twr-01 | 3fff:1ab:d50:d0::2 | Timeout — address does not exist |
| 2.5.4 | agg-01 | twr-02 | 3fff:1ab:d50:d16::18 | Host unreachable — configured as ::d18 not ::18 |
| 2.5.5 | twr-01 | twr-03 | 3fff:1ab:d50:d8::10 | Timeout — address does not exist |

**Root Cause:** Direct consequence of the missing IPv6 link addresses in category 2 above. Test 2.5.4 is an address notation mismatch — the config uses `::d18` (hex 0xd18 = 3352 decimal) while the test plan expected `::18` (decimal 24).

**Impact:** None on lab functionality. All IPv6 loopback-to-loopback connectivity works.

**Remediation:** Same as category 2. For test 2.5.4, the test plan expectation should be updated to match the actual address `3fff:1ab:d50:d16::d18`.

---

### 4. Cross-VNI Isolation Not Enforced (2 failures)

| Test | Ping Path | Expected | Actual |
|------|-----------|----------|--------|
| 7.3.1 | twr-01 198.18.104.101 → 198.18.106.101 (same device) | Fail | Success |
| 7.3.2 | twr-01 198.18.104.101 → twr-02 198.18.106.102 (cross-device) | Fail | Success |

**Root Cause:** Both VLAN interfaces (v1104 and v1106) are configured as L3 IP interfaces on the same bridge (`br-router`) in the global routing table. MikroTik's IP stack routes between them at L3. This is standard router behavior — the device has IP addresses in both subnets and performs inter-VLAN routing.

**Impact:** The two VNIs are not L2-isolated from each other when the same router has IP interfaces in both. This is by design for this topology where each tower participates in both VNIs. True L2 isolation would require separate VRFs or removing the IP addresses from the VLAN interfaces.

**Remediation:** Not required — this is expected behavior for this topology. The test expectation is technically incorrect for routers that participate in both VNIs as L3 endpoints. If isolation were needed, each VNI's VLAN interface would need to be placed in a separate VRF.

---

### 5. ~~No Alternate IS-IS Path for twr-01 (1 failure)~~ — RESOLVED

| Test | Action | Expected | Actual |
|------|--------|----------|--------|
| 9.1.1 | Shut agg-01 Gig2 (to twr-01) | IS-IS reconverges via alternate path | No route to twr-01 — `% Subnet not in table` |

**Root Cause:** The original automated test checked routing immediately after shutting the link, before IS-IS SPF had time to reconverge across 3 hops (twr-01 → twr-03 → twr-02 → agg-01).

**Resolution:** With ~15 seconds of convergence time, twr-01 correctly installs an IS-IS route to core-01 via `100.126.50.10%ether3` (twr-03). Both directions (twr-01→core-01 and agg-01→twr-01) work over the alternate path. twr-03 routes through twr-02, not back through twr-01.

**Remediation:** None required — the alternate path works. The test harness should allow sufficient convergence time (~15s) for multi-hop IS-IS SPF recalculation.

---

### 6. Stale VTEP Cache on MikroTik (1 failure)

| Test | Action | Expected | Actual |
|------|--------|----------|--------|
| 9.3.1 | Disable twr-03 BGP | twr-01/twr-02 remove twr-03 VTEPs | core-01 withdrew routes, but twr-01 retained stale VTEP entries |

**Root Cause:** After twr-03's BGP sessions were disabled and core-01 confirmed route withdrawal (EVPN prefix count dropped from 6 to 4), MikroTik twr-01 did not immediately remove the corresponding dynamic VTEP entries from its VXLAN VTEP table. This suggests MikroTik maintains a VTEP cache with a longer timeout than the BGP hold-time.

**Impact:** Low. Stale VTEP entries would cause traffic to be sent to a non-existent peer, which would be silently dropped. The entries should eventually age out. Overlay between twr-01↔twr-02 continued to work normally (test 9.3.2 passed).

**Remediation:** This is a MikroTik RouterOS behavior characteristic. The VTEP entries did eventually clear and were correctly restored when twr-03's BGP was re-enabled (test 9.3.3 passed). No action required unless faster failover is critical.
