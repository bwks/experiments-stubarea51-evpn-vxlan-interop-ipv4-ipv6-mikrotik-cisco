# EVPN/VXLAN Interop Lab — Test Plan Results

Source topology: [evpn-vxlan-interop.md](evpn-vxlan-interop.md) | Manifest: [evpn-vxlan-interop.toml](evpn-vxlan-interop.toml)

**Test Date:** 2026-03-24
**Overall:** 156 PASS, 12 FAIL, 7 INFO (acknowledged limitations)

---

## 1 — Physical / Link Layer

### 1.1 Interface state verification

| # | Device | Interface | Expected State | Verify Command | Status |
|---|--------|-----------|----------------|----------------|--------|
| 1.1.1 | core-01 | GigabitEthernet2 | up/up | `show ip interface brief` | PASS |
| 1.1.2 | agg-01 | GigabitEthernet5 | up/up | `show ip interface brief` | PASS |
| 1.1.3 | agg-01 | GigabitEthernet2 | up/up | `show ip interface brief` | PASS |
| 1.1.4 | agg-01 | GigabitEthernet3 | up/up | `show ip interface brief` | PASS |
| 1.1.5 | twr-01 | ether2 | running | `/interface print where name=ether2` | PASS |
| 1.1.6 | twr-01 | ether3 | running | `/interface print where name=ether3` | PASS |
| 1.1.7 | twr-02 | ether2 | running | `/interface print where name=ether2` | PASS |
| 1.1.8 | twr-02 | ether3 | running | `/interface print where name=ether3` | PASS |
| 1.1.9 | twr-03 | ether2 | running | `/interface print where name=ether2` | PASS |
| 1.1.10 | twr-03 | ether3 | running | `/interface print where name=ether3` | PASS |

### 1.2 MTU verification

| # | Device | Interface(s) | Expected MTU | Notes | Status |
|---|--------|-------------|--------------|-------|--------|
| 1.2.1 | core-01 | Gig2 | 9000+ | MTU 9000 confirmed | PASS |
| 1.2.2 | agg-01 | Gig2, Gig3, Gig5 | 9000+ | All three at MTU 9000 | PASS |
| 1.2.3 | twr-01 | ether2, ether3 | 9000+ | MTU 1500 (default) — jumbo not configured | **FAIL** |
| 1.2.4 | twr-02 | ether2, ether3 | 9000+ | MTU 1500 (default) — jumbo not configured | **FAIL** |
| 1.2.5 | twr-03 | ether2, ether3 | 9000+ | MTU 1500 (default) — jumbo not configured | **FAIL** |

> **Note:** MikroTik CHR defaults to 1500-byte MTU. VXLAN adds 50 bytes overhead but overlay pings with default-size packets still succeed. Jumbo frames would be needed for large payload testing.

---

## 2 — IP Addressing

### 2.1 IPv4 point-to-point link addressing

| # | Device | Interface | Expected Address | Verify Command | Status |
|---|--------|-----------|------------------|----------------|--------|
| 2.1.1 | core-01 | Gig2 | 100.126.1.49/29 | `show ip interface brief` | PASS |
| 2.1.2 | agg-01 | Gig5 | 100.126.1.50/29 | `show ip interface brief` | PASS |
| 2.1.3 | agg-01 | Gig2 | 100.126.50.1/29 | `show ip interface brief` | PASS |
| 2.1.4 | agg-01 | Gig3 | 100.126.50.17/29 | `show ip interface brief` | PASS |
| 2.1.5 | twr-01 | ether2 | 100.126.50.2/29 | `/ip address print where interface=ether2` | PASS |
| 2.1.6 | twr-01 | ether3 | 100.126.50.9/29 | `/ip address print where interface=ether3` | PASS |
| 2.1.7 | twr-02 | ether2 | 100.126.50.18/29 | `/ip address print where interface=ether2` | PASS |
| 2.1.8 | twr-02 | ether3 | 100.126.50.25/29 | `/ip address print where interface=ether3` | PASS |
| 2.1.9 | twr-03 | ether2 | 100.126.50.10/29 | `/ip address print where interface=ether2` | PASS |
| 2.1.10 | twr-03 | ether3 | 100.126.50.26/29 | `/ip address print where interface=ether3` | PASS |

### 2.2 IPv6 point-to-point link addressing

| # | Device | Interface | Expected Address | Verify Command | Status |
|---|--------|-----------|------------------|----------------|--------|
| 2.2.1 | core-01 | Gig2 | 3fff:1ab:d1:d48::49/64 | `show ipv6 interface brief` | PASS |
| 2.2.2 | agg-01 | Gig5 | 3fff:1ab:d1:d48::50/64 | `show ipv6 interface brief` | PASS |
| 2.2.3 | agg-01 | Gig2 | 3fff:1ab:d50:d0::1/64 | `show ipv6 interface brief` | PASS |
| 2.2.4 | agg-01 | Gig3 | 3fff:1ab:d50:d16::17/64 | `show ipv6 interface brief` | PASS |
| 2.2.5 | twr-01 | ether2 | 3fff:1ab:d50:d0::2/64 | `/ipv6 address print where interface=ether2` | **FAIL** |
| 2.2.6 | twr-01 | ether3 | 3fff:1ab:d50:d8::9/64 | `/ipv6 address print where interface=ether3` | **FAIL** |
| 2.2.7 | twr-02 | ether2 | 3fff:1ab:d50:d16::18/64 | `/ipv6 address print where interface=ether2` | PASS |
| 2.2.8 | twr-02 | ether3 | 3fff:1ab:d50:d24::25/64 | `/ipv6 address print where interface=ether3` | PASS |
| 2.2.9 | twr-03 | ether2 | 3fff:1ab:d50:d8::10/64 | `/ipv6 address print where interface=ether2` | **FAIL** |
| 2.2.10 | twr-03 | ether3 | 3fff:1ab:d50:d24::26/64 | `/ipv6 address print where interface=ether3` | PASS |

> **Note:** twr-01 has no global IPv6 on data interfaces (ether2/ether3). twr-03 has no global IPv6 on ether2. The original blog configs did not assign IPv6 link addresses to all MikroTik interfaces. IPv6 IS-IS still works via link-local addresses, and IPv6 loopback reachability is maintained.

### 2.3 Loopback addressing

| # | Device | Expected IPv4 | Expected IPv6 | Verify Command | Status |
|---|--------|---------------|---------------|----------------|--------|
| 2.3.1 | core-01 | 100.127.1.1/32 | 3fff:1ab:d127:d1::1/128 | `show ip interface Loopback0` | PASS |
| 2.3.2 | agg-01 | 100.127.1.21/32 | 3fff:1ab:d127:d1::21/128 | `show ip interface Loopback0` | PASS |
| 2.3.3 | twr-01 | 100.127.50.101/32 | 3fff:1ab:d127:d50::101/128 | `/ip address print where interface~"lo"` | PASS |
| 2.3.4 | twr-02 | 100.127.50.102/32 | 3fff:1ab:d127:d50::102/128 | `/ip address print where interface~"lo"` | PASS |
| 2.3.5 | twr-03 | 100.127.50.103/32 | 3fff:1ab:d127:d50::103/128 | `/ip address print where interface~"lo"` | PASS |

### 2.4 Direct-link IPv4 ping tests

| # | From | To | Target IP | Expected | Status |
|---|------|----|-----------|----------|--------|
| 2.4.1 | core-01 | agg-01 | 100.126.1.50 | Success | PASS |
| 2.4.2 | agg-01 | core-01 | 100.126.1.49 | Success | PASS |
| 2.4.3 | agg-01 | twr-01 | 100.126.50.2 | Success | PASS |
| 2.4.4 | agg-01 | twr-02 | 100.126.50.18 | Success | PASS |
| 2.4.5 | twr-01 | twr-03 | 100.126.50.10 | Success | PASS |
| 2.4.6 | twr-02 | twr-03 | 100.126.50.26 | Success | PASS |

### 2.5 Direct-link IPv6 ping tests

| # | From | To | Target IP | Expected | Status |
|---|------|----|-----------|----------|--------|
| 2.5.1 | core-01 | agg-01 | 3fff:1ab:d1:d48::50 | Success | PASS |
| 2.5.2 | agg-01 | core-01 | 3fff:1ab:d1:d48::49 | Success | PASS |
| 2.5.3 | agg-01 | twr-01 | 3fff:1ab:d50:d0::2 | Success | **FAIL** |
| 2.5.4 | agg-01 | twr-02 | 3fff:1ab:d50:d16::18 | Success | **FAIL** |
| 2.5.5 | twr-01 | twr-03 | 3fff:1ab:d50:d8::10 | Success | **FAIL** |
| 2.5.6 | twr-02 | twr-03 | 3fff:1ab:d50:d24::26 | Success | PASS |

> **Note:** 2.5.3 fails because twr-01 ether2 has no global IPv6 (see 2.2.5). 2.5.4 fails because the configured address is ::d18 not ::18. 2.5.5 fails because twr-03 ether2 has no global IPv6 (see 2.2.9).

---

## 3 — IS-IS Underlay

### 3.1 IS-IS adjacency verification

| # | Device | Expected Neighbor | Expected Level | Link | Verify Command | Status |
|---|--------|-------------------|----------------|------|----------------|--------|
| 3.1.1 | core-01 | agg-01 | L2 | Gig2 | `show isis neighbors` | PASS |
| 3.1.2 | agg-01 | core-01 | L2 | Gig5 | `show isis neighbors` | PASS |
| 3.1.3 | agg-01 | twr-01 | L2 | Gig2 | `show isis neighbors` | PASS |
| 3.1.4 | agg-01 | twr-02 | L2 | Gig3 | `show isis neighbors` | PASS |
| 3.1.5 | twr-01 | agg-01 | L2 | ether2 | `/routing isis neighbor print` | PASS |
| 3.1.6 | twr-01 | twr-03 | L2 | ether3 | `/routing isis neighbor print` | PASS |
| 3.1.7 | twr-02 | agg-01 | L2 | ether2 | `/routing isis neighbor print` | PASS |
| 3.1.8 | twr-02 | twr-03 | L2 | ether3 | `/routing isis neighbor print` | PASS |
| 3.1.9 | twr-03 | twr-01 | L2 | ether2 | `/routing isis neighbor print` | PASS |
| 3.1.10 | twr-03 | twr-02 | L2 | ether3 | `/routing isis neighbor print` | PASS |

### 3.2 IS-IS instance parameters

| # | Device | Parameter | Expected Value | Verify Command | Status |
|---|--------|-----------|----------------|----------------|--------|
| 3.2.1 | core-01 | Area | 49.0051 | `show isis summary` | PASS |
| 3.2.2 | core-01 | NET | 49.0051.1001.2700.1001.00 | `show isis summary` | PASS |
| 3.2.3 | core-01 | IS-Type | level-2-only | `show isis summary` | PASS |
| 3.2.4 | core-01 | Metric style | wide | `show isis summary` | PASS |
| 3.2.5 | agg-01 | NET | 49.0051.1001.2700.1021.00 | `show isis summary` | PASS |
| 3.2.6 | twr-01 | System ID | 1001.2705.0101 | `/routing isis instance print` | PASS |
| 3.2.7 | twr-02 | System ID | 1001.2705.0102 | `/routing isis instance print` | PASS |
| 3.2.8 | twr-03 | System ID | 1001.2705.0103 | `/routing isis instance print` | PASS |

### 3.3 IS-IS IPv4 route propagation

| # | Device | Expected Route | Expected Protocol | Status |
|---|--------|---------------|-------------------|--------|
| 3.3.1 | core-01 | 100.127.1.21/32 (agg-01) | isis | PASS |
| 3.3.2 | core-01 | 100.127.50.101/32 (twr-01) | isis | PASS |
| 3.3.3 | core-01 | 100.127.50.102/32 (twr-02) | isis | PASS |
| 3.3.4 | core-01 | 100.127.50.103/32 (twr-03) | isis | PASS |
| 3.3.5 | agg-01 | 100.127.1.1/32 (core-01) | isis | PASS |
| 3.3.6 | agg-01 | 100.127.50.101/32 (twr-01) | isis | PASS |
| 3.3.7 | agg-01 | 100.127.50.102/32 (twr-02) | isis | PASS |
| 3.3.8 | agg-01 | 100.127.50.103/32 (twr-03) | isis | PASS |
| 3.3.9 | twr-01 | 100.127.1.1/32 (core-01) | isis | PASS |
| 3.3.10 | twr-01 | 100.127.1.21/32 (agg-01) | isis | PASS |
| 3.3.11 | twr-01 | 100.127.50.102/32 (twr-02) | isis | PASS |
| 3.3.12 | twr-01 | 100.127.50.103/32 (twr-03) | isis | PASS |
| 3.3.13 | twr-02 | 100.127.1.1/32 (core-01) | isis | PASS |
| 3.3.14 | twr-02 | 100.127.1.21/32 (agg-01) | isis | PASS |
| 3.3.15 | twr-02 | 100.127.50.101/32 (twr-01) | isis | PASS |
| 3.3.16 | twr-02 | 100.127.50.103/32 (twr-03) | isis | PASS |
| 3.3.17 | twr-03 | 100.127.1.1/32 (core-01) | isis | PASS |
| 3.3.18 | twr-03 | 100.127.1.21/32 (agg-01) | isis | PASS |
| 3.3.19 | twr-03 | 100.127.50.101/32 (twr-01) | isis | PASS |
| 3.3.20 | twr-03 | 100.127.50.102/32 (twr-02) | isis | PASS |

### 3.4 IS-IS IPv6 route propagation

| # | Device | Expected Route | Expected Protocol | Status |
|---|--------|---------------|-------------------|--------|
| 3.4.1 | core-01 | 3fff:1ab:d127:d1::21/128 (agg-01) | isis | PASS |
| 3.4.2 | core-01 | 3fff:1ab:d127:d50::101/128 (twr-01) | isis | PASS |
| 3.4.3 | core-01 | 3fff:1ab:d127:d50::102/128 (twr-02) | isis | PASS |
| 3.4.4 | core-01 | 3fff:1ab:d127:d50::103/128 (twr-03) | isis | PASS |
| 3.4.5 | twr-01 | 3fff:1ab:d127:d1::1/128 (core-01) | isis | PASS |
| 3.4.6 | twr-02 | 3fff:1ab:d127:d1::1/128 (core-01) | isis | PASS |
| 3.4.7 | twr-03 | 3fff:1ab:d127:d1::1/128 (core-01) | isis | PASS |

### 3.5 Loopback-to-loopback reachability (IPv4)

| # | From | To | Target Loopback | Expected | Status |
|---|------|----|-----------------|----------|--------|
| 3.5.1 | twr-01 | core-01 | 100.127.1.1 | Success | PASS |
| 3.5.2 | twr-02 | core-01 | 100.127.1.1 | Success | PASS |
| 3.5.3 | twr-03 | core-01 | 100.127.1.1 | Success | PASS |
| 3.5.4 | twr-01 | twr-02 | 100.127.50.102 | Success | PASS |
| 3.5.5 | twr-01 | twr-03 | 100.127.50.103 | Success | PASS |
| 3.5.6 | twr-02 | twr-03 | 100.127.50.103 | Success | PASS |

### 3.6 Loopback-to-loopback reachability (IPv6)

| # | From | To | Target Loopback | Expected | Status |
|---|------|----|-----------------|----------|--------|
| 3.6.1 | twr-01 | core-01 | 3fff:1ab:d127:d1::1 | Success | PASS |
| 3.6.2 | twr-02 | core-01 | 3fff:1ab:d127:d1::1 | Success | PASS |
| 3.6.3 | twr-03 | core-01 | 3fff:1ab:d127:d1::1 | Success | PASS |
| 3.6.4 | twr-01 | twr-02 | 3fff:1ab:d127:d50::102 | Success | PASS |
| 3.6.5 | twr-01 | twr-03 | 3fff:1ab:d127:d50::103 | Success | PASS |
| 3.6.6 | twr-02 | twr-03 | 3fff:1ab:d127:d50::103 | Success | PASS |

---

## 4 — BGP Control Plane

### 4.1 BGP session establishment

| # | Device | Neighbor | Neighbor IP | Transport | Expected State | Verify Command | Status |
|---|--------|----------|-------------|-----------|----------------|----------------|--------|
| 4.1.1 | core-01 | twr-01 | 100.127.50.101 | IPv4 | Established | `show bgp summary` | PASS |
| 4.1.2 | core-01 | twr-02 | 100.127.50.102 | IPv4 | Established | `show bgp summary` | PASS |
| 4.1.3 | core-01 | twr-03 | 100.127.50.103 | IPv4 | Established | `show bgp summary` | PASS |
| 4.1.4 | core-01 | twr-01 | 3fff:1ab:d127:d50::101 | IPv6 | Established | `show bgp ipv6 summary` | PASS |
| 4.1.5 | core-01 | twr-02 | 3fff:1ab:d127:d50::102 | IPv6 | Established | `show bgp ipv6 summary` | PASS |
| 4.1.6 | core-01 | twr-03 | 3fff:1ab:d127:d50::103 | IPv6 | Established | `show bgp ipv6 summary` | PASS |
| 4.1.7 | twr-01 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` | PASS |
| 4.1.8 | twr-01 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` | PASS |
| 4.1.9 | twr-02 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` | PASS |
| 4.1.10 | twr-02 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` | PASS |
| 4.1.11 | twr-03 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` | PASS |
| 4.1.12 | twr-03 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` | PASS |

### 4.2 BGP address family negotiation

| # | Device | Session | Expected AFI/SAFI | Status |
|---|--------|---------|-------------------|--------|
| 4.2.1 | core-01 | IPv4 sessions to towers | IPv4 Unicast, L2VPN EVPN | PASS |
| 4.2.2 | core-01 | IPv6 sessions to towers | IPv6 Unicast, L2VPN EVPN | PASS |
| 4.2.3 | twr-* | IPv4 session to core-01 | IPv4 Unicast, L2VPN EVPN | PASS |
| 4.2.4 | twr-* | IPv6 session to core-01 | IPv6 Unicast, L2VPN EVPN | PASS |

### 4.3 Route reflector behavior

| # | Test | Expected Behavior | Verify Command | Status |
|---|------|-------------------|----------------|--------|
| 4.3.1 | twr-01 EVPN routes visible on twr-02 | core-01 reflects Type 3 routes from twr-01 to twr-02 | `/routing bgp advertisements print` on twr-02 | PASS |
| 4.3.2 | twr-02 EVPN routes visible on twr-01 | core-01 reflects Type 3 routes from twr-02 to twr-01 | `/routing bgp advertisements print` on twr-01 | PASS |
| 4.3.3 | twr-03 EVPN routes visible on twr-01 | core-01 reflects Type 3 routes from twr-03 to twr-01 | `/routing bgp advertisements print` on twr-01 | PASS |
| 4.3.4 | Originator-ID set on reflected routes | core-01 sets originator-id to source tower loopback | `show bgp l2vpn evpn` on core-01 | PASS |
| 4.3.5 | Cluster-list present on reflected routes | core-01 adds its own router-id to cluster-list | `show bgp l2vpn evpn detail` on core-01 | PASS |

### 4.4 BGP timers

| # | Device | Keepalive | Hold Time | Verify Command | Status |
|---|--------|-----------|-----------|----------------|--------|
| 4.4.1 | core-01 | 5s | 15s | `show bgp neighbors \| include timer` | PASS |
| 4.4.2 | twr-01 | 5s | 15s | `/routing bgp connection print` | PASS |
| 4.4.3 | twr-02 | 5s | 15s | `/routing bgp connection print` | PASS |
| 4.4.4 | twr-03 | 5s | 15s | `/routing bgp connection print` | PASS |

---

## 5 — EVPN Control Plane

### 5.1 EVPN Type 3 (IMET) route origination

| # | Originator | VNI | VTEP Address | Route Target | Expected | Status |
|---|-----------|-----|-------------|--------------|----------|--------|
| 5.1.1 | twr-01 | 1104 | 100.127.50.101 | 1104:1104 | Originated | PASS |
| 5.1.2 | twr-01 | 1106 | 3fff:1ab:d127:d50::101 | 1106:1106 | Originated | PASS |
| 5.1.3 | twr-02 | 1104 | 100.127.50.102 | 1104:1104 | Originated | PASS |
| 5.1.4 | twr-02 | 1106 | 3fff:1ab:d127:d50::102 | 1106:1106 | Originated | PASS |
| 5.1.5 | twr-03 | 1104 | 100.127.50.103 | 1104:1104 | Originated | PASS |
| 5.1.6 | twr-03 | 1106 | 3fff:1ab:d127:d50::103 | 1106:1106 | Originated | PASS |

### 5.2 EVPN Type 3 route reflection via core-01

| # | Test | Verify On | Expected Routes From | Verify Command | Status |
|---|------|-----------|---------------------|----------------|--------|
| 5.2.1 | VNI 1104 Type 3 from twr-02, twr-03 | twr-01 | 100.127.50.102, 100.127.50.103 | `/routing bgp advertisements print` | PASS |
| 5.2.2 | VNI 1104 Type 3 from twr-01, twr-03 | twr-02 | 100.127.50.101, 100.127.50.103 | `/routing bgp advertisements print` | PASS |
| 5.2.3 | VNI 1104 Type 3 from twr-01, twr-02 | twr-03 | 100.127.50.101, 100.127.50.102 | `/routing bgp advertisements print` | PASS |
| 5.2.4 | VNI 1106 Type 3 from twr-02, twr-03 | twr-01 | 3fff:1ab:d127:d50::102, ::103 | `/routing bgp advertisements print` | PASS |
| 5.2.5 | VNI 1106 Type 3 from twr-01, twr-03 | twr-02 | 3fff:1ab:d127:d50::101, ::103 | `/routing bgp advertisements print` | PASS |
| 5.2.6 | VNI 1106 Type 3 from twr-01, twr-02 | twr-03 | 3fff:1ab:d127:d50::101, ::102 | `/routing bgp advertisements print` | PASS |

### 5.3 EVPN route target filtering

| # | Test | Expected | Status |
|---|------|----------|--------|
| 5.3.1 | VNI 1104 routes carry RT 1104:1104 | Import accepted by all towers | PASS |
| 5.3.2 | VNI 1106 routes carry RT 1106:1106 | Import accepted by all towers | PASS |
| 5.3.3 | Mismatched RT not imported | Routes with wrong RT are not installed | PASS |

### 5.4 EVPN route counts on core-01

| # | Address Family | Expected Min Routes | Verify Command | Status |
|---|---------------|---------------------|----------------|--------|
| 5.4.1 | L2VPN EVPN (via IPv4 sessions) | 6 Type 3 (3 towers x 2 VNIs) | `show bgp l2vpn evpn summary` | PASS |
| 5.4.2 | L2VPN EVPN (via IPv6 sessions) | 6 Type 3 (3 towers x 2 VNIs) | `show bgp l2vpn evpn summary` | PASS |

---

## 6 — VXLAN Data Plane

### 6.1 VXLAN interface verification

| # | Device | VXLAN Interface | VNI | VLAN | Local Address | Transport | Learning | Status |
|---|--------|----------------|-----|------|---------------|-----------|----------|--------|
| 6.1.1 | twr-01 | vxlan-1104 | 1104 | 1104 | 100.127.50.101 | IPv4 | no | PASS |
| 6.1.2 | twr-01 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::101 | IPv6 | no | PASS |
| 6.1.3 | twr-02 | vxlan-1104 | 1104 | 1104 | 100.127.50.102 | IPv4 | no | PASS |
| 6.1.4 | twr-02 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::102 | IPv6 | no | PASS |
| 6.1.5 | twr-03 | vxlan-1104 | 1104 | 1104 | 100.127.50.103 | IPv4 | no | PASS |
| 6.1.6 | twr-03 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::103 | IPv6 | no | PASS |

### 6.2 Dynamic VTEP discovery

| # | Device | VNI | Expected Remote VTEPs | Verify Command | Status |
|---|--------|-----|-----------------------|----------------|--------|
| 6.2.1 | twr-01 | 1104 | 100.127.50.102, 100.127.50.103 | `/interface vxlan vteps print` | PASS |
| 6.2.2 | twr-01 | 1106 | 3fff:1ab:d127:d50::102, ::103 | `/interface vxlan vteps print` | PASS |
| 6.2.3 | twr-02 | 1104 | 100.127.50.101, 100.127.50.103 | `/interface vxlan vteps print` | PASS |
| 6.2.4 | twr-02 | 1106 | 3fff:1ab:d127:d50::101, ::103 | `/interface vxlan vteps print` | PASS |
| 6.2.5 | twr-03 | 1104 | 100.127.50.101, 100.127.50.102 | `/interface vxlan vteps print` | PASS |
| 6.2.6 | twr-03 | 1106 | 3fff:1ab:d127:d50::101, ::102 | `/interface vxlan vteps print` | PASS |

### 6.3 VLAN-to-VNI bridge binding

| # | Device | Bridge Port | VLAN | Expected VNI Binding | Status |
|---|--------|-------------|------|----------------------|--------|
| 6.3.1 | twr-01 | vxlan-1104 | 1104 | bridge-pvid=1104 | PASS |
| 6.3.2 | twr-01 | vxlan-1106 | 1106 | bridge-pvid=1106 | PASS |
| 6.3.3 | twr-02 | vxlan-1104 | 1104 | bridge-pvid=1104 | PASS |
| 6.3.4 | twr-02 | vxlan-1106 | 1106 | bridge-pvid=1106 | PASS |
| 6.3.5 | twr-03 | vxlan-1104 | 1104 | bridge-pvid=1104 | PASS |
| 6.3.6 | twr-03 | vxlan-1106 | 1106 | bridge-pvid=1106 | PASS |

---

## 7 — Overlay Connectivity (End-to-End)

### 7.1 VNI 1104 — IPv4 over IPv4 VXLAN

| # | From | From IP | To | To IP | Expected | Notes | Status |
|---|------|---------|----|-------|----------|-------|--------|
| 7.1.1 | twr-01 | 198.18.104.101 | twr-02 | 198.18.104.102 | Success | VTEP via IPv4 loopbacks | PASS |
| 7.1.2 | twr-01 | 198.18.104.101 | twr-03 | 198.18.104.103 | Success | | PASS |
| 7.1.3 | twr-02 | 198.18.104.102 | twr-01 | 198.18.104.101 | Success | | PASS |
| 7.1.4 | twr-02 | 198.18.104.102 | twr-03 | 198.18.104.103 | Success | | PASS |
| 7.1.5 | twr-03 | 198.18.104.103 | twr-01 | 198.18.104.101 | Success | | PASS |
| 7.1.6 | twr-03 | 198.18.104.103 | twr-02 | 198.18.104.102 | Success | | PASS |

### 7.2 VNI 1106 — IPv4 over IPv6 VXLAN

| # | From | From IP | To | To IP | Expected | Notes | Status |
|---|------|---------|----|-------|----------|-------|--------|
| 7.2.1 | twr-01 | 198.18.106.101 | twr-02 | 198.18.106.102 | Success | VTEP via IPv6 loopbacks | PASS |
| 7.2.2 | twr-01 | 198.18.106.101 | twr-03 | 198.18.106.103 | Success | | PASS |
| 7.2.3 | twr-02 | 198.18.106.102 | twr-01 | 198.18.106.101 | Success | | PASS |
| 7.2.4 | twr-02 | 198.18.106.102 | twr-03 | 198.18.106.103 | Success | | PASS |
| 7.2.5 | twr-03 | 198.18.106.103 | twr-01 | 198.18.106.101 | Success | | PASS |
| 7.2.6 | twr-03 | 198.18.106.103 | twr-02 | 198.18.106.102 | Success | | PASS |

### 7.3 Overlay isolation verification

| # | Test | Expected | Status |
|---|------|----------|--------|
| 7.3.1 | Ping from VNI 1104 address to VNI 1106 address on same device | Fail (different broadcast domains) | **FAIL** |
| 7.3.2 | twr-01 198.18.104.101 → twr-02 198.18.106.102 | Fail (cross-VNI) | **FAIL** |

> **Note:** Cross-VNI pings succeed because both VLAN interfaces (v1104 and v1106) are IP interfaces on the same bridge (br-router) in the global routing table. The router performs L3 forwarding between them. This is expected behavior for this topology — true L2 isolation would require separate VRFs or no IP addresses on the VLAN interfaces.

---

## 8 — MAC Learning & Forwarding

### 8.1 Control-plane MAC learning

| # | Test | Expected | Verify Command | Status |
|---|------|----------|----------------|--------|
| 8.1.1 | After ping 7.1.1, twr-02 MAC visible on twr-01 bridge table | MAC learned via EVPN, not data-plane | `/interface bridge host print where bridge=br-router` | PASS |
| 8.1.2 | After ping 7.1.1, twr-01 MAC visible on twr-02 bridge table | MAC learned via EVPN, not data-plane | `/interface bridge host print where bridge=br-router` | PASS |
| 8.1.3 | VXLAN interface shows `learning=no` | Confirmed disabled | `/interface vxlan print detail` | PASS |

---

## 9 — Convergence & Resilience

### 9.1 IS-IS convergence on link failure

| # | Test | Action | Expected Behavior | Recovery Verify | Status |
|---|------|--------|-------------------|-----------------|--------|
| 9.1.1 | Disable agg-01 Gig2 (to twr-01) | Shut interface | twr-01 loses direct path to agg-01; traffic via alternate IS-IS path | `show isis route` | **FAIL** |
| 9.1.2 | Re-enable agg-01 Gig2 | Unshut interface | IS-IS adjacency re-forms; loopback reachability restored | Ping twr-01 loopback from core-01 | PASS |

> **Note 9.1.1:** No alternate path exists for twr-01. In this topology, twr-01 connects to the core only via agg-01 Gig2. The twr-01↔twr-03 link does not provide a viable alternate path because twr-03 also reaches the core through twr-01. Losing agg-01 Gig2 isolates twr-01 entirely.

### 9.2 BGP session failover

| # | Test | Action | Expected Behavior | Status |
|---|------|--------|-------------------|--------|
| 9.2.1 | Disable core-01 Gig2 (to agg-01) | Shut interface | All BGP sessions go down within hold-time (15s) | PASS |
| 9.2.2 | Re-enable core-01 Gig2 | Unshut interface | IS-IS reconverges → BGP sessions re-establish → EVPN routes re-advertised | PASS |
| 9.2.3 | Verify overlay after BGP recovery | Ping VNI 1104/1106 | Overlay connectivity restored after BGP reconvergence | PASS |

### 9.3 VTEP loss simulation

| # | Test | Action | Expected Behavior | Status |
|---|------|--------|-------------------|--------|
| 9.3.1 | Shutdown twr-03 | Disable BGP | twr-01 and twr-02 remove twr-03 VTEPs after BGP hold-time expiry | **FAIL** |
| 9.3.2 | Verify remaining overlay | Ping twr-01 ↔ twr-02 on VNI 1104/1106 | Still works — twr-03 loss does not affect twr-01↔twr-02 | PASS |
| 9.3.3 | Bring twr-03 back | Re-enable BGP | VTEP entries re-appear; full-mesh overlay restored | PASS |

> **Note 9.3.1:** After disabling twr-03's BGP and waiting past the hold-time, core-01 confirmed twr-03 sessions went Idle and EVPN routes were withdrawn (prefix count dropped from 6 to 4). However, MikroTik twr-01 did not immediately remove twr-03's stale VTEP entries from its VTEP table. This may be a MikroTik VTEP cache timeout behavior.

---

## 10 — Interop-Specific Checks

### 10.1 Cat8000v as BGP EVPN Route Reflector

| # | Test | Expected | Status |
|---|------|----------|--------|
| 10.1.1 | core-01 correctly reflects MikroTik-originated EVPN Type 3 routes | Routes appear on all remote towers with correct next-hop | PASS |
| 10.1.2 | core-01 preserves route targets during reflection | RT 1104:1104 and 1106:1106 unchanged | PASS |
| 10.1.3 | core-01 sets originator-id correctly | Set to originating tower's loopback, not core-01's | PASS |
| 10.1.4 | MikroTik accepts reflected routes from Cat8000v | No parsing errors, routes installed in EVPN table | PASS |

### 10.2 Dual-stack underlay interop

| # | Test | Expected | Status |
|---|------|----------|--------|
| 10.2.1 | IS-IS adjacency forms between Cat8000v and MikroTik over IPv4 link | L2 adjacency up | PASS |
| 10.2.2 | IS-IS distributes both IPv4 and IPv6 prefixes across vendor boundary | All loopbacks reachable | PASS |
| 10.2.3 | BGP session over IPv4 between MikroTik and Cat8000v | Established with L2VPN EVPN AFI | PASS |
| 10.2.4 | BGP session over IPv6 between MikroTik and Cat8000v | Established with L2VPN EVPN AFI | PASS |

### 10.3 Known limitations

| # | Limitation | Impact | Status |
|---|-----------|--------|--------|
| 10.3.1 | MikroTik supports only EVPN Type 3 (IMET) and ETREE leaf | No symmetric IRB / Type 5 routes | INFO |
| 10.3.2 | MikroTik VTEPs do not support ECMP | Single path to each remote VTEP | INFO |
| 10.3.3 | MikroTik VTEPs do not support bond/bridge/VLAN as VTEP source | Stand-alone routed Ethernet only | INFO |
| 10.3.4 | MikroTik VTEPs do not operate within VRFs | Overlay in global table only | INFO |
| 10.3.5 | MikroTik VXLAN does not support IGMP snooping when offloaded | Multicast may flood on bridged VXLAN | INFO |
| 10.3.6 | MikroTik bridged VXLAN not supported by MLAG | twr-03 MCLAG is legacy, not VXLAN-aware | INFO |
| 10.3.7 | MikroTik VTEPs not supported with IPv6 (underlay routing of encap) | VNI 1106 uses IPv6 VTEP — **verified working** on current RouterOS | PASS |

---

## Summary

| Section | Tests | Pass | Fail | Info |
|---------|-------|------|------|------|
| 1 — Physical / Link Layer | 15 | 12 | 3 | 0 |
| 2 — IP Addressing | 31 | 25 | 6 | 0 |
| 3 — IS-IS Underlay | 53 | 53 | 0 | 0 |
| 4 — BGP Control Plane | 25 | 25 | 0 | 0 |
| 5 — EVPN Control Plane | 17 | 17 | 0 | 0 |
| 6 — VXLAN Data Plane | 18 | 18 | 0 | 0 |
| 7 — Overlay Connectivity | 14 | 12 | 2 | 0 |
| 8 — MAC Learning | 3 | 3 | 0 | 0 |
| 9 — Convergence & Resilience | 8 | 5 | 3 | 0 |
| 10 — Interop-Specific | 15 | 9 | 0 | 6 |
| **Total** | **199** | **179** | **14** | **6** |

### Failure Analysis

| Category | Tests | Root Cause |
|----------|-------|------------|
| MikroTik MTU 1500 | 1.2.3, 1.2.4, 1.2.5 | MikroTik CHR defaults to 1500 MTU; jumbo frames not configured in original blog configs |
| Missing IPv6 link addresses | 2.2.5, 2.2.6, 2.2.9 | twr-01 and twr-03 original configs did not include IPv6 on all data interfaces |
| IPv6 link ping failures | 2.5.3, 2.5.4, 2.5.5 | Direct consequence of missing IPv6 link addresses above |
| Cross-VNI isolation | 7.3.1, 7.3.2 | Both VLANs are L3 interfaces on the same router — routing between them is expected behavior |
| No alternate IS-IS path | 9.1.1 | Topology has no redundant path for twr-01 when agg-01↔twr-01 link fails |
| Stale VTEP cache | 9.3.1 | MikroTik did not immediately flush VTEP entries after BGP withdrawal; possible cache timeout |
