# EVPN/VXLAN Interop Lab — stubarea51

## What is this project?

A Sherpa virtual network lab reproducing the EVPN/VXLAN interop topology from
[stubarea51.net](https://stubarea51.net/2025/09/22/evpn-vxlan-interop-ipv4-ipv6-mikrotik-ip-infusion/).
The original lab tests EVPN/VXLAN between IP Infusion OcNOS and MikroTik RouterOS v7.
Since Sherpa does not support IP Infusion devices, OcNOS nodes have been replaced with
**Cisco Cat8000v** (`cisco_cat8000v`).

## Topology — 5 devices, 5 links

```
core-01 (Cat8000v, Route Reflector)
    │
  agg-01 (Cat8000v, Aggregation)
   / \
twr-01  twr-02   (MikroTik CHR, EVPN/VXLAN VTEPs)
   \   /
  twr-03          (MikroTik CHR, Legacy MCLAG)
```

- **Underlay:** IS-IS Level-2, area 49.0051, dual-stack IPv4+IPv6
- **Overlay:** BGP EVPN with VXLAN data plane — VNI 1104 (IPv4/IPv4), VNI 1106 (IPv4/IPv6)
- **BGP AS:** 4208675309, core-01 is the route reflector
- **Loopbacks:** 100.127.x.x/32, 3fff:1ab:d127::/48
- **P2P links:** 100.126.x.x/29, 3fff:1ab::/32

## File layout

```
├── CLAUDE.md                          ← you are here
├── evpn-vxlan-interop.toml            ← Sherpa lab manifest (TOML)
├── evpn-vxlan-interop.md              ← Device/interface/IP reference doc
├── evpn-vxlan-interop-testplan.md     ← 175-test validation plan
├── evpn-vxlan-interop.drawio          ← draw.io topology diagram
└── configs/
    ├── core-01.cfg                    ← IOS-XE config (translated from OcNOS)
    ├── agg-01.cfg                     ← IOS-XE config (translated from OcNOS)
    ├── twr-01.rsc                     ← MikroTik RouterOS v7 config
    ├── twr-02.rsc                     ← MikroTik RouterOS v7 config
    └── twr-03.rsc                     ← MikroTik RouterOS v7 config
```

## Sherpa reference

- Sherpa source: `~/code/rust/sherpa`
- Manifests are TOML — see `crates/topology/tests/manifest_tests.rs` for schema examples
- Cat8000v interfaces: `gig1` (mgmt), `gig2`–`gig16` (data)
- MikroTik CHR interfaces: `eth1` (mgmt), `eth2`–`eth9` (data)
- Links use `"node::interface"` format, e.g. `"agg-01::gig2"`

## Key decisions

- Original MikroTik `ether` interfaces are shifted +1 in Sherpa (ether1→eth2) because
  Sherpa reserves eth1 for management.
- OcNOS interface numbers (eth2, eth3, eth5) map directly to Cat8000v gig numbers
  (gig2, gig3, gig5).
- The edge-01 ISP router from the original diagram was excluded — this lab focuses on
  the 5 core EVPN/VXLAN nodes only.
- MikroTik configs are taken verbatim from the blog article. IOS-XE configs are
  translated from OcNOS with appropriate syntax changes.

## Known limitations (MikroTik RouterOS VXLAN)

- Only EVPN Type 3 (IMET) routes supported; ETREE leaf only
- VTEPs do not support ECMP, bond/bridge/VLAN source, VRFs, or IGMP snooping offload
- Bridged VXLAN not supported by MLAG
- IPv6 VTEP support (VNI 1106) may have caveats depending on RouterOS version
