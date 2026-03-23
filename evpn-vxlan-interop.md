# EVPN/VXLAN Interop Lab — Device, Interface & IP Reference

Source: [stubarea51.net — EVPN/VXLAN Interop IPv4/IPv6 MikroTik & IP Infusion](https://stubarea51.net/2025/09/22/evpn-vxlan-interop-ipv4-ipv6-mikrotik-ip-infusion/)

> **Note:** IP Infusion OcNOS devices are not supported by Sherpa. The two OcNOS nodes
> (core-01 and agg-01) have been replaced with **Cisco Cat8000v** (`cisco_cat8000v`).

---

## Global Parameters

| Parameter | Value |
|-----------|-------|
| BGP AS | 4208675309 |
| IGP | IS-IS Level 2 |
| Overlay | EVPN/VXLAN |
| IPv4 Loopback Space | 100.127.0.0/16 |
| IPv6 Loopback Space | 3fff:1ab:d127::/48 |
| IPv4 P2P Link Space | 100.126.0.0/16 |
| IPv6 P2P Link Space | 3fff:1ab::/32 |
| Overlay Subnet Space | 198.18.0.0/16 |

---

## Devices

| Device | Role | Sherpa Model | Original Vendor | Router ID | IPv6 Loopback |
|--------|------|--------------|-----------------|-----------|---------------|
| core-01 | Route Reflector | `cisco_cat8000v` | IP Infusion OcNOS | 100.127.1.1 | 3fff:1ab:d127:d1::1/128 |
| agg-01 | Aggregation | `cisco_cat8000v` | IP Infusion OcNOS | 100.127.1.21 | 3fff:1ab:d127:d1::21/128 |
| twr-01 | Tower / Edge VTEP | `mikrotik_chr` | MikroTik CHR v7 | 100.127.50.101 | 3fff:1ab:d127:d50::101/128 |
| twr-02 | Tower / Edge VTEP | `mikrotik_chr` | MikroTik CHR v7 | 100.127.50.102 | 3fff:1ab:d127:d50::102/128 |
| twr-03 | Tower / Edge VTEP (Legacy MCLAG) | `mikrotik_chr` | MikroTik CHR v7 | 100.127.50.103 | 3fff:1ab:d127:d50::103/128 |

### IS-IS System IDs

| Device | NET / System ID |
|--------|-----------------|
| agg-01 | 1001.2700.1021 |
| twr-01 | 1001.2705.0101 |
| twr-02 | 1001.2705.0102 |
| twr-03 | 1001.2705.0103 |

---

## Point-to-Point Underlay Links

| # | Source Device | Source Interface | Source IPv4 | Source IPv6 | Dest Device | Dest Interface | Dest IPv4 | Dest IPv6 | Subnet |
|---|-------------|-----------------|-------------|-------------|-------------|----------------|-----------|-----------|--------|
| 1 | core-01 | gig2 | 100.126.1.49/29 | 3fff:1ab:d1:d48::49/64 | agg-01 | gig5 | 100.126.1.50/29 | 3fff:1ab:d1:d48::50/64 | 100.126.1.48/29 |
| 2 | agg-01 | gig2 | 100.126.50.1/29 | 3fff:1ab:d50:d0::1/64 | twr-01 | eth2 | 100.126.50.2/29 | 3fff:1ab:d50:d0::2/64 | 100.126.50.0/29 |
| 3 | agg-01 | gig3 | 100.126.50.17/29 | 3fff:1ab:d50:d16::17/64 | twr-02 | eth2 | 100.126.50.18/29 | 3fff:1ab:d50:d16::18/64 | 100.126.50.16/29 |
| 4 | twr-01 | eth3 | 100.126.50.9/29 | 3fff:1ab:d50:d8::9/64 | twr-03 | eth2 | 100.126.50.10/29 | 3fff:1ab:d50:d8::10/64 | 100.126.50.8/29 |
| 5 | twr-02 | eth3 | 100.126.50.25/29 | 3fff:1ab:d50:d24::25/64 | twr-03 | eth3 | 100.126.50.26/29 | 3fff:1ab:d50:d24::26/64 | 100.126.50.24/29 |

> **Interface mapping note:** Sherpa reserves the first interface for management on each
> platform (gig1 for Cat8000v, eth1 for MikroTik CHR). Data interfaces therefore start
> at gig2 / eth2. The original OcNOS interface numbers (eth2, eth3, eth5) have been
> preserved where they map to valid Sherpa Cat8000v `gig` interfaces. MikroTik `ether`
> interfaces have been shifted by +1 to account for the management reservation
> (e.g., original ether1 → Sherpa eth2).

---

## Per-Device Interface Summary

### core-01 (Cisco Cat8000v — Route Reflector)

| Interface | Connects To | IPv4 Address | IPv6 Address |
|-----------|-------------|--------------|--------------|
| Loopback | — | 100.127.1.1/32 | 3fff:1ab:d127:d1::1/128 |
| gig2 | agg-01 gig5 | 100.126.1.49/29 | 3fff:1ab:d1:d48::49/64 |

### agg-01 (Cisco Cat8000v — Aggregation)

| Interface | Connects To | IPv4 Address | IPv6 Address |
|-----------|-------------|--------------|--------------|
| Loopback | — | 100.127.1.21/32 | 3fff:1ab:d127:d1::21/128 |
| gig5 | core-01 gig2 | 100.126.1.50/29 | 3fff:1ab:d1:d48::50/64 |
| gig2 | twr-01 eth2 | 100.126.50.1/29 | 3fff:1ab:d50:d0::1/64 |
| gig3 | twr-02 eth2 | 100.126.50.17/29 | 3fff:1ab:d50:d16::17/64 |

### twr-01 (MikroTik CHR — Tower/Edge VTEP)

| Interface | Connects To | IPv4 Address | IPv6 Address |
|-----------|-------------|--------------|--------------|
| Loopback | — | 100.127.50.101/32 | 3fff:1ab:d127:d50::101/128 |
| eth2 | agg-01 gig2 | 100.126.50.2/29 | 3fff:1ab:d50:d0::2/64 |
| eth3 | twr-03 eth2 | 100.126.50.9/29 | 3fff:1ab:d50:d8::9/64 |

### twr-02 (MikroTik CHR — Tower/Edge VTEP)

| Interface | Connects To | IPv4 Address | IPv6 Address |
|-----------|-------------|--------------|--------------|
| Loopback | — | 100.127.50.102/32 | 3fff:1ab:d127:d50::102/128 |
| eth2 | agg-01 gig3 | 100.126.50.18/29 | 3fff:1ab:d50:d16::18/64 |
| eth3 | twr-03 eth3 | 100.126.50.25/29 | 3fff:1ab:d50:d24::25/64 |

### twr-03 (MikroTik CHR — Tower/Edge VTEP, Legacy MCLAG)

| Interface | Connects To | IPv4 Address | IPv6 Address |
|-----------|-------------|--------------|--------------|
| Loopback | — | 100.127.50.103/32 | 3fff:1ab:d127:d50::103/128 |
| eth2 | twr-01 eth3 | 100.126.50.10/29 | 3fff:1ab:d50:d8::10/64 |
| eth3 | twr-02 eth3 | 100.126.50.26/29 | 3fff:1ab:d50:d24::26/64 |

---

## EVPN/VXLAN Overlay

### VNI 1104 — IPv4 over IPv4 VXLAN

| Parameter | Value |
|-----------|-------|
| VNI | 1104 |
| VLAN ID | 1104 |
| Subnet | 198.18.104.0/24 |
| Route Target | 1104:1104 |
| VTEP Transport | IPv4 (Loopback) |

| Device | VTEP Address | Overlay IP |
|--------|-------------|------------|
| twr-01 | 100.127.50.101 | 198.18.104.101/24 |
| twr-02 | 100.127.50.102 | 198.18.104.102/24 |
| twr-03 | 100.127.50.103 | 198.18.104.103/24 |

### VNI 1106 — IPv4 over IPv6 VXLAN

| Parameter | Value |
|-----------|-------|
| VNI | 1106 |
| VLAN ID | 1106 |
| Subnet | 198.18.106.0/24 |
| Route Target | 1106:1106 |
| VTEP Transport | IPv6 (Loopback) |

| Device | VTEP Address | Overlay IP |
|--------|-------------|------------|
| twr-01 | 3fff:1ab:d127:d50::101 | 198.18.106.101/24 |
| twr-02 | 3fff:1ab:d127:d50::102 | 198.18.106.102/24 |
| twr-03 | 3fff:1ab:d127:d50::103 | 198.18.106.103/24 |

---

## Topology Diagram (ASCII)

```
               ┌──────────┐
               │ core-01  │
               │ Cat8000v │
               │  (RR)    │
               └────┬─────┘
                    │ gig2 ←→ gig5
               ┌────┴─────┐
               │  agg-01  │
               │ Cat8000v │
               └──┬────┬──┘
          gig2 ───┘    └─── gig3
           │                  │
      eth2 │                  │ eth2
     ┌─────┴─────┐    ┌──────┴─────┐
     │  twr-01   │    │   twr-02   │
     │ MikroTik  │    │  MikroTik  │
     └─────┬─────┘    └──────┬─────┘
      eth3 │                  │ eth3
           │    ┌────────┐    │
           └────┤ twr-03 ├────┘
         eth2   │MikroTik│  eth3
                │(MCLAG) │
                └────────┘
```
