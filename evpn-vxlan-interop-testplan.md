# EVPN/VXLAN Interop Lab — Test Plan

Source topology: [evpn-vxlan-interop.md](evpn-vxlan-interop.md) | Manifest: [evpn-vxlan-interop.toml](evpn-vxlan-interop.toml)

---

## 1 — Physical / Link Layer

### 1.1 Interface state verification

| # | Device | Interface | Expected State | Verify Command |
|---|--------|-----------|----------------|----------------|
| 1.1.1 | core-01 | GigabitEthernet2 | up/up | `show ip interface brief` |
| 1.1.2 | agg-01 | GigabitEthernet5 | up/up | `show ip interface brief` |
| 1.1.3 | agg-01 | GigabitEthernet2 | up/up | `show ip interface brief` |
| 1.1.4 | agg-01 | GigabitEthernet3 | up/up | `show ip interface brief` |
| 1.1.5 | twr-01 | ether2 | running | `/interface print where name=ether2` |
| 1.1.6 | twr-01 | ether3 | running | `/interface print where name=ether3` |
| 1.1.7 | twr-02 | ether2 | running | `/interface print where name=ether2` |
| 1.1.8 | twr-02 | ether3 | running | `/interface print where name=ether3` |
| 1.1.9 | twr-03 | ether2 | running | `/interface print where name=ether2` |
| 1.1.10 | twr-03 | ether3 | running | `/interface print where name=ether3` |

### 1.2 MTU verification

| # | Device | Interface(s) | Expected MTU | Notes |
|---|--------|-------------|--------------|-------|
| 1.2.1 | core-01 | Gig2 | 9000+ | Jumbo required for VXLAN overhead |
| 1.2.2 | agg-01 | Gig2, Gig3, Gig5 | 9000+ | Jumbo required for VXLAN overhead |
| 1.2.3 | twr-01 | ether2, ether3 | 9000+ | Verify `/interface ethernet print` |
| 1.2.4 | twr-02 | ether2, ether3 | 9000+ | Verify `/interface ethernet print` |
| 1.2.5 | twr-03 | ether2, ether3 | 9000+ | Verify `/interface ethernet print` |

---

## 2 — IP Addressing

### 2.1 IPv4 point-to-point link addressing

| # | Device | Interface | Expected Address | Verify Command |
|---|--------|-----------|------------------|----------------|
| 2.1.1 | core-01 | Gig2 | 100.126.1.49/29 | `show ip interface brief` |
| 2.1.2 | agg-01 | Gig5 | 100.126.1.50/29 | `show ip interface brief` |
| 2.1.3 | agg-01 | Gig2 | 100.126.50.1/29 | `show ip interface brief` |
| 2.1.4 | agg-01 | Gig3 | 100.126.50.17/29 | `show ip interface brief` |
| 2.1.5 | twr-01 | ether2 | 100.126.50.2/29 | `/ip address print where interface=ether2` |
| 2.1.6 | twr-01 | ether3 | 100.126.50.9/29 | `/ip address print where interface=ether3` |
| 2.1.7 | twr-02 | ether2 | 100.126.50.18/29 | `/ip address print where interface=ether2` |
| 2.1.8 | twr-02 | ether3 | 100.126.50.25/29 | `/ip address print where interface=ether3` |
| 2.1.9 | twr-03 | ether2 | 100.126.50.10/29 | `/ip address print where interface=ether2` |
| 2.1.10 | twr-03 | ether3 | 100.126.50.26/29 | `/ip address print where interface=ether3` |

### 2.2 IPv6 point-to-point link addressing

| # | Device | Interface | Expected Address | Verify Command |
|---|--------|-----------|------------------|----------------|
| 2.2.1 | core-01 | Gig2 | 3fff:1ab:d1:d48::49/64 | `show ipv6 interface brief` |
| 2.2.2 | agg-01 | Gig5 | 3fff:1ab:d1:d48::50/64 | `show ipv6 interface brief` |
| 2.2.3 | agg-01 | Gig2 | 3fff:1ab:d50:d0::1/64 | `show ipv6 interface brief` |
| 2.2.4 | agg-01 | Gig3 | 3fff:1ab:d50:d16::17/64 | `show ipv6 interface brief` |
| 2.2.5 | twr-01 | ether2 | 3fff:1ab:d50:d0::2/64 | `/ipv6 address print where interface=ether2` |
| 2.2.6 | twr-01 | ether3 | 3fff:1ab:d50:d8::9/64 | `/ipv6 address print where interface=ether3` |
| 2.2.7 | twr-02 | ether2 | 3fff:1ab:d50:d16::18/64 | `/ipv6 address print where interface=ether2` |
| 2.2.8 | twr-02 | ether3 | 3fff:1ab:d50:d24::25/64 | `/ipv6 address print where interface=ether3` |
| 2.2.9 | twr-03 | ether2 | 3fff:1ab:d50:d8::10/64 | `/ipv6 address print where interface=ether2` |
| 2.2.10 | twr-03 | ether3 | 3fff:1ab:d50:d24::26/64 | `/ipv6 address print where interface=ether3` |

### 2.3 Loopback addressing

| # | Device | Expected IPv4 | Expected IPv6 | Verify Command |
|---|--------|---------------|---------------|----------------|
| 2.3.1 | core-01 | 100.127.1.1/32 | 3fff:1ab:d127:d1::1/128 | `show ip interface Loopback0` |
| 2.3.2 | agg-01 | 100.127.1.21/32 | 3fff:1ab:d127:d1::21/128 | `show ip interface Loopback0` |
| 2.3.3 | twr-01 | 100.127.50.101/32 | 3fff:1ab:d127:d50::101/128 | `/ip address print where interface~"lo"` |
| 2.3.4 | twr-02 | 100.127.50.102/32 | 3fff:1ab:d127:d50::102/128 | `/ip address print where interface~"lo"` |
| 2.3.5 | twr-03 | 100.127.50.103/32 | 3fff:1ab:d127:d50::103/128 | `/ip address print where interface~"lo"` |

### 2.4 Direct-link IPv4 ping tests

| # | From | To | Target IP | Expected |
|---|------|----|-----------|----------|
| 2.4.1 | core-01 | agg-01 | 100.126.1.50 | Success |
| 2.4.2 | agg-01 | core-01 | 100.126.1.49 | Success |
| 2.4.3 | agg-01 | twr-01 | 100.126.50.2 | Success |
| 2.4.4 | agg-01 | twr-02 | 100.126.50.18 | Success |
| 2.4.5 | twr-01 | twr-03 | 100.126.50.10 | Success |
| 2.4.6 | twr-02 | twr-03 | 100.126.50.26 | Success |

### 2.5 Direct-link IPv6 ping tests

| # | From | To | Target IP | Expected |
|---|------|----|-----------|----------|
| 2.5.1 | core-01 | agg-01 | 3fff:1ab:d1:d48::50 | Success |
| 2.5.2 | agg-01 | core-01 | 3fff:1ab:d1:d48::49 | Success |
| 2.5.3 | agg-01 | twr-01 | 3fff:1ab:d50:d0::2 | Success |
| 2.5.4 | agg-01 | twr-02 | 3fff:1ab:d50:d16::18 | Success |
| 2.5.5 | twr-01 | twr-03 | 3fff:1ab:d50:d8::10 | Success |
| 2.5.6 | twr-02 | twr-03 | 3fff:1ab:d50:d24::26 | Success |

---

## 3 — IS-IS Underlay

### 3.1 IS-IS adjacency verification

| # | Device | Expected Neighbor | Expected Level | Link | Verify Command |
|---|--------|-------------------|----------------|------|----------------|
| 3.1.1 | core-01 | agg-01 | L2 | Gig2 | `show isis neighbors` |
| 3.1.2 | agg-01 | core-01 | L2 | Gig5 | `show isis neighbors` |
| 3.1.3 | agg-01 | twr-01 | L2 | Gig2 | `show isis neighbors` |
| 3.1.4 | agg-01 | twr-02 | L2 | Gig3 | `show isis neighbors` |
| 3.1.5 | twr-01 | agg-01 | L2 | ether2 | `/routing isis neighbor print` |
| 3.1.6 | twr-01 | twr-03 | L2 | ether3 | `/routing isis neighbor print` |
| 3.1.7 | twr-02 | agg-01 | L2 | ether2 | `/routing isis neighbor print` |
| 3.1.8 | twr-02 | twr-03 | L2 | ether3 | `/routing isis neighbor print` |
| 3.1.9 | twr-03 | twr-01 | L2 | ether2 | `/routing isis neighbor print` |
| 3.1.10 | twr-03 | twr-02 | L2 | ether3 | `/routing isis neighbor print` |

### 3.2 IS-IS instance parameters

| # | Device | Parameter | Expected Value | Verify Command |
|---|--------|-----------|----------------|----------------|
| 3.2.1 | core-01 | Area | 49.0051 | `show isis summary` |
| 3.2.2 | core-01 | NET | 49.0051.1001.2700.1001.00 | `show isis summary` |
| 3.2.3 | core-01 | IS-Type | level-2-only | `show isis summary` |
| 3.2.4 | core-01 | Metric style | wide | `show isis summary` |
| 3.2.5 | agg-01 | NET | 49.0051.1001.2700.1021.00 | `show isis summary` |
| 3.2.6 | twr-01 | System ID | 1001.2705.0101 | `/routing isis instance print` |
| 3.2.7 | twr-02 | System ID | 1001.2705.0102 | `/routing isis instance print` |
| 3.2.8 | twr-03 | System ID | 1001.2705.0103 | `/routing isis instance print` |

### 3.3 IS-IS IPv4 route propagation

All loopbacks must be reachable via IS-IS from every device.

| # | Device | Expected Route | Expected Protocol |
|---|--------|---------------|-------------------|
| 3.3.1 | core-01 | 100.127.1.21/32 (agg-01) | isis |
| 3.3.2 | core-01 | 100.127.50.101/32 (twr-01) | isis |
| 3.3.3 | core-01 | 100.127.50.102/32 (twr-02) | isis |
| 3.3.4 | core-01 | 100.127.50.103/32 (twr-03) | isis |
| 3.3.5 | agg-01 | 100.127.1.1/32 (core-01) | isis |
| 3.3.6 | agg-01 | 100.127.50.101/32 (twr-01) | isis |
| 3.3.7 | agg-01 | 100.127.50.102/32 (twr-02) | isis |
| 3.3.8 | agg-01 | 100.127.50.103/32 (twr-03) | isis |
| 3.3.9 | twr-01 | 100.127.1.1/32 (core-01) | isis |
| 3.3.10 | twr-01 | 100.127.1.21/32 (agg-01) | isis |
| 3.3.11 | twr-01 | 100.127.50.102/32 (twr-02) | isis |
| 3.3.12 | twr-01 | 100.127.50.103/32 (twr-03) | isis |
| 3.3.13 | twr-02 | 100.127.1.1/32 (core-01) | isis |
| 3.3.14 | twr-02 | 100.127.1.21/32 (agg-01) | isis |
| 3.3.15 | twr-02 | 100.127.50.101/32 (twr-01) | isis |
| 3.3.16 | twr-02 | 100.127.50.103/32 (twr-03) | isis |
| 3.3.17 | twr-03 | 100.127.1.1/32 (core-01) | isis |
| 3.3.18 | twr-03 | 100.127.1.21/32 (agg-01) | isis |
| 3.3.19 | twr-03 | 100.127.50.101/32 (twr-01) | isis |
| 3.3.20 | twr-03 | 100.127.50.102/32 (twr-02) | isis |

### 3.4 IS-IS IPv6 route propagation

All IPv6 loopbacks must be reachable via IS-IS from every device.

| # | Device | Expected Route | Expected Protocol |
|---|--------|---------------|-------------------|
| 3.4.1 | core-01 | 3fff:1ab:d127:d1::21/128 (agg-01) | isis |
| 3.4.2 | core-01 | 3fff:1ab:d127:d50::101/128 (twr-01) | isis |
| 3.4.3 | core-01 | 3fff:1ab:d127:d50::102/128 (twr-02) | isis |
| 3.4.4 | core-01 | 3fff:1ab:d127:d50::103/128 (twr-03) | isis |
| 3.4.5 | twr-01 | 3fff:1ab:d127:d1::1/128 (core-01) | isis |
| 3.4.6 | twr-02 | 3fff:1ab:d127:d1::1/128 (core-01) | isis |
| 3.4.7 | twr-03 | 3fff:1ab:d127:d1::1/128 (core-01) | isis |

### 3.5 Loopback-to-loopback reachability (IPv4)

| # | From | To | Target Loopback | Expected |
|---|------|----|-----------------|----------|
| 3.5.1 | twr-01 | core-01 | 100.127.1.1 | Success |
| 3.5.2 | twr-02 | core-01 | 100.127.1.1 | Success |
| 3.5.3 | twr-03 | core-01 | 100.127.1.1 | Success |
| 3.5.4 | twr-01 | twr-02 | 100.127.50.102 | Success |
| 3.5.5 | twr-01 | twr-03 | 100.127.50.103 | Success |
| 3.5.6 | twr-02 | twr-03 | 100.127.50.103 | Success |

### 3.6 Loopback-to-loopback reachability (IPv6)

| # | From | To | Target Loopback | Expected |
|---|------|----|-----------------|----------|
| 3.6.1 | twr-01 | core-01 | 3fff:1ab:d127:d1::1 | Success |
| 3.6.2 | twr-02 | core-01 | 3fff:1ab:d127:d1::1 | Success |
| 3.6.3 | twr-03 | core-01 | 3fff:1ab:d127:d1::1 | Success |
| 3.6.4 | twr-01 | twr-02 | 3fff:1ab:d127:d50::102 | Success |
| 3.6.5 | twr-01 | twr-03 | 3fff:1ab:d127:d50::103 | Success |
| 3.6.6 | twr-02 | twr-03 | 3fff:1ab:d127:d50::103 | Success |

---

## 4 — BGP Control Plane

### 4.1 BGP session establishment

core-01 acts as route reflector. Each tower peers to core-01 over both IPv4 and IPv6 transport.

| # | Device | Neighbor | Neighbor IP | Transport | Expected State | Verify Command |
|---|--------|----------|-------------|-----------|----------------|----------------|
| 4.1.1 | core-01 | twr-01 | 100.127.50.101 | IPv4 | Established | `show bgp summary` |
| 4.1.2 | core-01 | twr-02 | 100.127.50.102 | IPv4 | Established | `show bgp summary` |
| 4.1.3 | core-01 | twr-03 | 100.127.50.103 | IPv4 | Established | `show bgp summary` |
| 4.1.4 | core-01 | twr-01 | 3fff:1ab:d127:d50::101 | IPv6 | Established | `show bgp ipv6 summary` |
| 4.1.5 | core-01 | twr-02 | 3fff:1ab:d127:d50::102 | IPv6 | Established | `show bgp ipv6 summary` |
| 4.1.6 | core-01 | twr-03 | 3fff:1ab:d127:d50::103 | IPv6 | Established | `show bgp ipv6 summary` |
| 4.1.7 | twr-01 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` |
| 4.1.8 | twr-01 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` |
| 4.1.9 | twr-02 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` |
| 4.1.10 | twr-02 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` |
| 4.1.11 | twr-03 | core-01 | 100.127.1.1 | IPv4 | established | `/routing bgp session print` |
| 4.1.12 | twr-03 | core-01 | 3fff:1ab:d127:d1::1 | IPv6 | established | `/routing bgp session print` |

### 4.2 BGP address family negotiation

Each session must negotiate the correct address families.

| # | Device | Session | Expected AFI/SAFI |
|---|--------|---------|-------------------|
| 4.2.1 | core-01 | IPv4 sessions to towers | IPv4 Unicast, L2VPN EVPN |
| 4.2.2 | core-01 | IPv6 sessions to towers | IPv6 Unicast, L2VPN EVPN |
| 4.2.3 | twr-* | IPv4 session to core-01 | IPv4 Unicast, L2VPN EVPN |
| 4.2.4 | twr-* | IPv6 session to core-01 | IPv6 Unicast, L2VPN EVPN |

### 4.3 Route reflector behavior

| # | Test | Expected Behavior | Verify Command |
|---|------|-------------------|----------------|
| 4.3.1 | twr-01 EVPN routes visible on twr-02 | core-01 reflects Type 3 routes from twr-01 to twr-02 | `/routing bgp advertisements print` on twr-02 |
| 4.3.2 | twr-02 EVPN routes visible on twr-01 | core-01 reflects Type 3 routes from twr-02 to twr-01 | `/routing bgp advertisements print` on twr-01 |
| 4.3.3 | twr-03 EVPN routes visible on twr-01 | core-01 reflects Type 3 routes from twr-03 to twr-01 | `/routing bgp advertisements print` on twr-01 |
| 4.3.4 | Originator-ID set on reflected routes | core-01 sets originator-id to source tower loopback | `show bgp l2vpn evpn` on core-01 |
| 4.3.5 | Cluster-list present on reflected routes | core-01 adds its own router-id to cluster-list | `show bgp l2vpn evpn detail` on core-01 |

### 4.4 BGP timers

| # | Device | Keepalive | Hold Time | Verify Command |
|---|--------|-----------|-----------|----------------|
| 4.4.1 | core-01 | 5s | 15s | `show bgp neighbors \| include timer` |
| 4.4.2 | twr-01 | 5s | 15s | `/routing bgp connection print` |
| 4.4.3 | twr-02 | 5s | 15s | `/routing bgp connection print` |
| 4.4.4 | twr-03 | 5s | 15s | `/routing bgp connection print` |

---

## 5 — EVPN Control Plane

### 5.1 EVPN Type 3 (IMET) route origination

Each tower must originate Type 3 routes for both VNI 1104 and VNI 1106.

| # | Originator | VNI | VTEP Address | Route Target | Expected |
|---|-----------|-----|-------------|--------------|----------|
| 5.1.1 | twr-01 | 1104 | 100.127.50.101 | 1104:1104 | Originated |
| 5.1.2 | twr-01 | 1106 | 3fff:1ab:d127:d50::101 | 1106:1106 | Originated |
| 5.1.3 | twr-02 | 1104 | 100.127.50.102 | 1104:1104 | Originated |
| 5.1.4 | twr-02 | 1106 | 3fff:1ab:d127:d50::102 | 1106:1106 | Originated |
| 5.1.5 | twr-03 | 1104 | 100.127.50.103 | 1104:1104 | Originated |
| 5.1.6 | twr-03 | 1106 | 3fff:1ab:d127:d50::103 | 1106:1106 | Originated |

### 5.2 EVPN Type 3 route reflection via core-01

| # | Test | Verify On | Expected Routes From | Verify Command |
|---|------|-----------|---------------------|----------------|
| 5.2.1 | VNI 1104 Type 3 from twr-02, twr-03 | twr-01 | 100.127.50.102, 100.127.50.103 | `/routing bgp advertisements print` |
| 5.2.2 | VNI 1104 Type 3 from twr-01, twr-03 | twr-02 | 100.127.50.101, 100.127.50.103 | `/routing bgp advertisements print` |
| 5.2.3 | VNI 1104 Type 3 from twr-01, twr-02 | twr-03 | 100.127.50.101, 100.127.50.102 | `/routing bgp advertisements print` |
| 5.2.4 | VNI 1106 Type 3 from twr-02, twr-03 | twr-01 | 3fff:1ab:d127:d50::102, ::103 | `/routing bgp advertisements print` |
| 5.2.5 | VNI 1106 Type 3 from twr-01, twr-03 | twr-02 | 3fff:1ab:d127:d50::101, ::103 | `/routing bgp advertisements print` |
| 5.2.6 | VNI 1106 Type 3 from twr-01, twr-02 | twr-03 | 3fff:1ab:d127:d50::101, ::102 | `/routing bgp advertisements print` |

### 5.3 EVPN route target filtering

| # | Test | Expected |
|---|------|----------|
| 5.3.1 | VNI 1104 routes carry RT 1104:1104 | Import accepted by all towers |
| 5.3.2 | VNI 1106 routes carry RT 1106:1106 | Import accepted by all towers |
| 5.3.3 | Mismatched RT not imported | Routes with wrong RT are not installed |

### 5.4 EVPN route counts on core-01

| # | Address Family | Expected Min Routes | Verify Command |
|---|---------------|---------------------|----------------|
| 5.4.1 | L2VPN EVPN (via IPv4 sessions) | 6 Type 3 (3 towers x 2 VNIs) | `show bgp l2vpn evpn summary` |
| 5.4.2 | L2VPN EVPN (via IPv6 sessions) | 6 Type 3 (3 towers x 2 VNIs) | `show bgp l2vpn evpn summary` |

---

## 6 — VXLAN Data Plane

### 6.1 VXLAN interface verification

| # | Device | VXLAN Interface | VNI | VLAN | Local Address | Transport | Learning |
|---|--------|----------------|-----|------|---------------|-----------|----------|
| 6.1.1 | twr-01 | vxlan-1104 | 1104 | 1104 | 100.127.50.101 | IPv4 | no |
| 6.1.2 | twr-01 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::101 | IPv6 | no |
| 6.1.3 | twr-02 | vxlan-1104 | 1104 | 1104 | 100.127.50.102 | IPv4 | no |
| 6.1.4 | twr-02 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::102 | IPv6 | no |
| 6.1.5 | twr-03 | vxlan-1104 | 1104 | 1104 | 100.127.50.103 | IPv4 | no |
| 6.1.6 | twr-03 | vxlan-1106 | 1106 | 1106 | 3fff:1ab:d127:d50::103 | IPv6 | no |

**Verify:** `/interface vxlan print detail`

### 6.2 Dynamic VTEP discovery

After EVPN Type 3 routes are exchanged, remote VTEPs must be dynamically created.

| # | Device | VNI | Expected Remote VTEPs | Verify Command |
|---|--------|-----|-----------------------|----------------|
| 6.2.1 | twr-01 | 1104 | 100.127.50.102, 100.127.50.103 | `/interface vxlan vteps print` |
| 6.2.2 | twr-01 | 1106 | 3fff:1ab:d127:d50::102, ::103 | `/interface vxlan vteps print` |
| 6.2.3 | twr-02 | 1104 | 100.127.50.101, 100.127.50.103 | `/interface vxlan vteps print` |
| 6.2.4 | twr-02 | 1106 | 3fff:1ab:d127:d50::101, ::103 | `/interface vxlan vteps print` |
| 6.2.5 | twr-03 | 1104 | 100.127.50.101, 100.127.50.102 | `/interface vxlan vteps print` |
| 6.2.6 | twr-03 | 1106 | 3fff:1ab:d127:d50::101, ::102 | `/interface vxlan vteps print` |

### 6.3 VLAN-to-VNI bridge binding

| # | Device | Bridge Port | VLAN | Expected VNI Binding |
|---|--------|-------------|------|----------------------|
| 6.3.1 | twr-01 | vxlan-1104 | 1104 | bridge-pvid=1104 |
| 6.3.2 | twr-01 | vxlan-1106 | 1106 | bridge-pvid=1106 |
| 6.3.3 | twr-02 | vxlan-1104 | 1104 | bridge-pvid=1104 |
| 6.3.4 | twr-02 | vxlan-1106 | 1106 | bridge-pvid=1106 |
| 6.3.5 | twr-03 | vxlan-1104 | 1104 | bridge-pvid=1104 |
| 6.3.6 | twr-03 | vxlan-1106 | 1106 | bridge-pvid=1106 |

**Verify:** `/interface bridge port print`

---

## 7 — Overlay Connectivity (End-to-End)

### 7.1 VNI 1104 — IPv4 over IPv4 VXLAN

| # | From | From IP | To | To IP | Expected | Notes |
|---|------|---------|----|-------|----------|-------|
| 7.1.1 | twr-01 | 198.18.104.101 | twr-02 | 198.18.104.102 | Success | VTEP via IPv4 loopbacks |
| 7.1.2 | twr-01 | 198.18.104.101 | twr-03 | 198.18.104.103 | Success | |
| 7.1.3 | twr-02 | 198.18.104.102 | twr-01 | 198.18.104.101 | Success | |
| 7.1.4 | twr-02 | 198.18.104.102 | twr-03 | 198.18.104.103 | Success | |
| 7.1.5 | twr-03 | 198.18.104.103 | twr-01 | 198.18.104.101 | Success | |
| 7.1.6 | twr-03 | 198.18.104.103 | twr-02 | 198.18.104.102 | Success | |

**Verify (MikroTik):** `/ping 198.18.104.x src-address=198.18.104.y`

### 7.2 VNI 1106 — IPv4 over IPv6 VXLAN

| # | From | From IP | To | To IP | Expected | Notes |
|---|------|---------|----|-------|----------|-------|
| 7.2.1 | twr-01 | 198.18.106.101 | twr-02 | 198.18.106.102 | Success | VTEP via IPv6 loopbacks |
| 7.2.2 | twr-01 | 198.18.106.101 | twr-03 | 198.18.106.103 | Success | |
| 7.2.3 | twr-02 | 198.18.106.102 | twr-01 | 198.18.106.101 | Success | |
| 7.2.4 | twr-02 | 198.18.106.102 | twr-03 | 198.18.106.103 | Success | |
| 7.2.5 | twr-03 | 198.18.106.103 | twr-01 | 198.18.106.101 | Success | |
| 7.2.6 | twr-03 | 198.18.106.103 | twr-02 | 198.18.106.102 | Success | |

**Verify (MikroTik):** `/ping 198.18.106.x src-address=198.18.106.y`

### 7.3 Overlay isolation verification

| # | Test | Expected |
|---|------|----------|
| 7.3.1 | Ping from VNI 1104 address to VNI 1106 address on same device | Fail (different broadcast domains) |
| 7.3.2 | twr-01 198.18.104.101 → twr-02 198.18.106.102 | Fail (cross-VNI) |

---

## 8 — MAC Learning & Forwarding

### 8.1 Control-plane MAC learning

Learning is disabled on VXLAN interfaces — MACs must be distributed via EVPN Type 2.

| # | Test | Expected | Verify Command |
|---|------|----------|----------------|
| 8.1.1 | After ping 7.1.1, twr-02 MAC visible on twr-01 bridge table | MAC learned via EVPN, not data-plane | `/interface bridge host print where bridge=bridge1` |
| 8.1.2 | After ping 7.1.1, twr-01 MAC visible on twr-02 bridge table | MAC learned via EVPN, not data-plane | `/interface bridge host print where bridge=bridge1` |
| 8.1.3 | VXLAN interface shows `learning=no` | Confirmed disabled | `/interface vxlan print detail` |

---

## 9 — Convergence & Resilience

### 9.1 IS-IS convergence on link failure

| # | Test | Action | Expected Behavior | Recovery Verify |
|---|------|--------|-------------------|-----------------|
| 9.1.1 | Disable agg-01 Gig2 (to twr-01) | Shut interface | twr-01 loses direct path to agg-01; traffic via twr-03→twr-02→agg-01 (if alternate path exists via IS-IS) | `show isis route` / `/routing isis route print` |
| 9.1.2 | Re-enable agg-01 Gig2 | Unshut interface | IS-IS adjacency re-forms; loopback reachability restored | Ping twr-01 loopback from core-01 |

### 9.2 BGP session failover

| # | Test | Action | Expected Behavior |
|---|------|--------|-------------------|
| 9.2.1 | Disable core-01 Gig2 (to agg-01) | Shut interface | All BGP sessions via IPv4 should go down within hold-time (15s); EVPN routes withdrawn |
| 9.2.2 | Re-enable core-01 Gig2 | Unshut interface | IS-IS reconverges → BGP sessions re-establish → EVPN routes re-advertised |
| 9.2.3 | Verify overlay after BGP recovery | Ping VNI 1104/1106 | Overlay connectivity restored after BGP reconvergence |

### 9.3 VTEP loss simulation

| # | Test | Action | Expected Behavior |
|---|------|--------|-------------------|
| 9.3.1 | Shutdown twr-03 | Power off node | twr-01 and twr-02 remove twr-03 VTEPs after BGP hold-time expiry |
| 9.3.2 | Verify remaining overlay | Ping twr-01 ↔ twr-02 on VNI 1104/1106 | Still works — twr-03 loss does not affect twr-01↔twr-02 |
| 9.3.3 | Bring twr-03 back | Power on node | VTEP entries re-appear; full-mesh overlay restored |

---

## 10 — Interop-Specific Checks

These tests specifically validate cross-vendor behavior between Cat8000v (replacing OcNOS) and MikroTik.

### 10.1 Cat8000v as BGP EVPN Route Reflector

| # | Test | Expected |
|---|------|----------|
| 10.1.1 | core-01 correctly reflects MikroTik-originated EVPN Type 3 routes | Routes appear on all remote towers with correct next-hop |
| 10.1.2 | core-01 preserves route targets during reflection | RT 1104:1104 and 1106:1106 unchanged |
| 10.1.3 | core-01 sets originator-id correctly | Set to originating tower's loopback, not core-01's |
| 10.1.4 | MikroTik accepts reflected routes from Cat8000v | No parsing errors, routes installed in EVPN table |

### 10.2 Dual-stack underlay interop

| # | Test | Expected |
|---|------|----------|
| 10.2.1 | IS-IS adjacency forms between Cat8000v and MikroTik over IPv4 link | L2 adjacency up |
| 10.2.2 | IS-IS distributes both IPv4 and IPv6 prefixes across vendor boundary | All loopbacks reachable |
| 10.2.3 | BGP session over IPv4 between MikroTik and Cat8000v | Established with L2VPN EVPN AFI |
| 10.2.4 | BGP session over IPv6 between MikroTik and Cat8000v | Established with L2VPN EVPN AFI |

### 10.3 Known limitations

| # | Limitation | Impact |
|---|-----------|--------|
| 10.3.1 | MikroTik supports only EVPN Type 3 (IMET) and ETREE leaf | No symmetric IRB / Type 5 routes |
| 10.3.2 | MikroTik VTEPs do not support ECMP | Single path to each remote VTEP |
| 10.3.3 | MikroTik VTEPs do not support bond/bridge/VLAN as VTEP source | Stand-alone routed Ethernet only |
| 10.3.4 | MikroTik VTEPs do not operate within VRFs | Overlay in global table only |
| 10.3.5 | MikroTik VXLAN does not support IGMP snooping when offloaded | Multicast may flood on bridged VXLAN |
| 10.3.6 | MikroTik bridged VXLAN not supported by MLAG | twr-03 MCLAG is legacy, not VXLAN-aware |
| 10.3.7 | MikroTik VTEPs not supported with IPv6 (underlay routing of encap) | VNI 1106 uses IPv6 VTEP — verify this actually works on current RouterOS |

---

## Test Execution Checklist

| Section | Description | Tests | Status |
|---------|-------------|-------|--------|
| 1 | Physical / Link Layer | 15 | ☐ |
| 2 | IP Addressing | 33 | ☐ |
| 3 | IS-IS Underlay | 40 | ☐ |
| 4 | BGP Control Plane | 17 | ☐ |
| 5 | EVPN Control Plane | 17 | ☐ |
| 6 | VXLAN Data Plane | 18 | ☐ |
| 7 | Overlay Connectivity | 14 | ☐ |
| 8 | MAC Learning & Forwarding | 3 | ☐ |
| 9 | Convergence & Resilience | 7 | ☐ |
| 10 | Interop-Specific Checks | 11 | ☐ |
| **Total** | | **175** | |
