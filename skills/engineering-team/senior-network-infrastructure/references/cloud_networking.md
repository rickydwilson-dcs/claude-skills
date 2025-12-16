# Cloud Networking Guide

Comprehensive guide to multi-cloud connectivity, dedicated connections, and hybrid networking.

## Overview

This reference covers enterprise connectivity options including dedicated connections (Direct Connect, ExpressRoute, Cloud Interconnect), VPN architectures, and multi-cloud networking patterns. Includes BGP configuration, failover strategies, and cost optimization.

## AWS Direct Connect

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Direct Connect Architecture               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                    AWS                         │
│   ┌─────────────┐               ┌─────────────┐             │
│   │  Customer   │               │    VPC      │             │
│   │  Router     │               │  10.0.0.0/16│             │
│   │             │               └──────▲──────┘             │
│   │  BGP: 65000 │                      │                    │
│   └──────┬──────┘                      │                    │
│          │                    ┌────────┴────────┐           │
│          │                    │ Virtual Private │           │
│          │                    │    Gateway      │           │
│          │                    │  BGP: 64512     │           │
│          │                    └────────▲────────┘           │
│          │                             │                    │
│   ┌──────▼──────┐             ┌────────┴────────┐           │
│   │  Customer   │             │  Direct Connect │           │
│   │  Equipment  │◄───────────►│    Gateway      │           │
│   │  (Colo)     │   1/10 Gbps │                 │           │
│   └─────────────┘             └─────────────────┘           │
│          │                                                   │
│   ┌──────▼──────┐                                           │
│   │  Data       │                                           │
│   │  Center     │                                           │
│   └─────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Connection Types

| Type | Bandwidth | Lead Time | Use Case |
|------|-----------|-----------|----------|
| Dedicated | 1, 10, 100 Gbps | 2-4 weeks | High bandwidth, predictable |
| Hosted | 50 Mbps - 10 Gbps | Days | Flexible, partner-provided |

### Virtual Interface Types

**Private VIF:**
- Access VPC resources via private IPs
- Requires Virtual Private Gateway or Direct Connect Gateway
- BGP peering with customer ASN

**Public VIF:**
- Access AWS public services (S3, DynamoDB, etc.)
- Receive AWS public IP prefixes via BGP
- Alternative to internet for AWS API access

**Transit VIF:**
- Connect to Transit Gateway
- Access multiple VPCs across regions
- Simplified multi-VPC connectivity

### High Availability Configuration

**Recommended: Dual Connections at Different Locations**

```
┌─────────────────────────────────────────────────────────────┐
│              High Availability Direct Connect                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                                                │
│   ┌─────────────┐                                           │
│   │  Customer   │                                           │
│   │  Network    │                                           │
│   └──────┬──────┘                                           │
│          │                                                   │
│   ┌──────┴──────┐                                           │
│   │             │                                           │
│   ▼             ▼                                           │
│ Location A   Location B                                      │
│ ┌────────┐   ┌────────┐                                     │
│ │ DX     │   │ DX     │                                     │
│ │ Conn 1 │   │ Conn 2 │                                     │
│ └───┬────┘   └───┬────┘                                     │
│     │            │                                          │
│     ▼            ▼                                          │
│  ┌──────────────────┐                                       │
│  │  Direct Connect  │                                       │
│  │     Gateway      │                                       │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  Transit Gateway │                                       │
│  │   (Multi-VPC)    │                                       │
│  └──────────────────┘                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### BGP Configuration

**Customer Router Configuration (Cisco IOS):**
```
! BGP Configuration for Direct Connect
router bgp 65000
  neighbor 169.254.100.1 remote-as 64512
  neighbor 169.254.100.1 description AWS-DX-Primary

  address-family ipv4
    network 192.168.0.0 mask 255.255.0.0
    neighbor 169.254.100.1 activate
    neighbor 169.254.100.1 soft-reconfiguration inbound
    neighbor 169.254.100.1 prefix-list ADVERTISE-TO-AWS out
    neighbor 169.254.100.1 prefix-list ACCEPT-FROM-AWS in
  exit-address-family

ip prefix-list ADVERTISE-TO-AWS seq 10 permit 192.168.0.0/16
ip prefix-list ACCEPT-FROM-AWS seq 10 permit 10.0.0.0/8 le 24
```

**AS Path Prepending for Failover:**
```
! Primary path - no prepending
route-map AWS-PRIMARY permit 10
  set as-path prepend

! Backup path - prepend to make less preferred
route-map AWS-BACKUP permit 10
  set as-path prepend 65000 65000
```

## Azure ExpressRoute

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ExpressRoute Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                      Azure                     │
│   ┌─────────────┐                 ┌─────────────┐           │
│   │  Customer   │                 │    VNet     │           │
│   │  Network    │                 │ 10.0.0.0/16 │           │
│   └──────┬──────┘                 └──────▲──────┘           │
│          │                               │                   │
│   ┌──────▼──────┐               ┌────────┴────────┐         │
│   │  Customer   │               │  ExpressRoute   │         │
│   │  Edge       │               │  Gateway        │         │
│   │  Router     │               └────────▲────────┘         │
│   └──────┬──────┘                        │                   │
│          │                               │                   │
│   ┌──────▼──────┐               ┌────────┴────────┐         │
│   │  Partner    │◄─────────────►│  Microsoft     │         │
│   │  Edge       │   1-10 Gbps   │  Edge          │         │
│   │  (Meet-Me)  │               │  (Peering Loc) │         │
│   └─────────────┘               └─────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Peering Types

**Private Peering:**
- Connect to VNets via private IPs
- Access Azure VMs, Load Balancers, etc.
- Primary /30 and Secondary /30 subnets required

**Microsoft Peering:**
- Access Microsoft 365 and Azure PaaS services
- Requires public IPs owned by customer
- Route filters to control prefix advertisements

### Circuit SKUs

| SKU | Bandwidth | Global Reach | Metered/Unlimited |
|-----|-----------|--------------|-------------------|
| Standard | 50 Mbps - 10 Gbps | No | Both |
| Premium | 50 Mbps - 10 Gbps | Yes | Both |
| Local | 1/2/5/10 Gbps | No | Unlimited only |

### High Availability

**Zone-Redundant Gateway:**
```hcl
resource "azurerm_virtual_network_gateway" "expressroute" {
  name                = "er-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type     = "ExpressRoute"
  sku      = "ErGw1AZ"  # Zone-redundant SKU

  ip_configuration {
    name                          = "default"
    public_ip_address_id          = azurerm_public_ip.er_gw.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

**Dual Circuits (Different Peering Locations):**
```
Circuit 1: Equinix Washington DC
Circuit 2: Equinix Dallas

Both connected to same VNet via ExpressRoute Gateway
BGP handles automatic failover
```

## GCP Cloud Interconnect

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                Cloud Interconnect Architecture               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                       GCP                      │
│   ┌─────────────┐                 ┌─────────────┐           │
│   │  Customer   │                 │    VPC      │           │
│   │  Network    │                 │ 10.0.0.0/16 │           │
│   └──────┬──────┘                 └──────▲──────┘           │
│          │                               │                   │
│   ┌──────▼──────┐               ┌────────┴────────┐         │
│   │  Customer   │               │  Cloud Router   │         │
│   │  Router     │               │  (BGP)          │         │
│   └──────┬──────┘               └────────▲────────┘         │
│          │                               │                   │
│   ┌──────▼──────┐               ┌────────┴────────┐         │
│   │  Colocation │◄─────────────►│  Google Edge    │         │
│   │  Facility   │  10-200 Gbps  │  (Colo Facility)│         │
│   └─────────────┘               └─────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Connection Types

**Dedicated Interconnect:**
- Direct physical connection to Google
- 10 Gbps or 100 Gbps per link
- 8 links maximum (800 Gbps total)
- Requires colocation at Google POP

**Partner Interconnect:**
- Through service provider
- 50 Mbps to 50 Gbps
- Layer 2 or Layer 3 options
- No colocation required

### VLAN Attachments

```hcl
resource "google_compute_interconnect_attachment" "primary" {
  name         = "vlan-attachment-primary"
  router       = google_compute_router.main.id
  type         = "DEDICATED"
  interconnect = "https://www.googleapis.com/compute/v1/projects/my-project/global/interconnects/my-interconnect"

  bandwidth    = "BPS_10G"
  vlan_tag8021q = 100

  candidate_subnets = ["169.254.100.0/29"]
}
```

### Cloud Router BGP Configuration

```hcl
resource "google_compute_router" "main" {
  name    = "cloud-router"
  network = google_compute_network.vpc.id
  region  = "us-central1"

  bgp {
    asn               = 64512
    advertise_mode    = "CUSTOM"
    advertised_groups = ["ALL_SUBNETS"]

    advertised_ip_ranges {
      range = "10.0.0.0/8"
    }
  }
}

resource "google_compute_router_peer" "primary" {
  name            = "bgp-peer-primary"
  router          = google_compute_router.main.name
  region          = "us-central1"
  peer_asn        = 65000
  peer_ip_address = "169.254.100.2"

  advertised_route_priority = 100
}
```

## VPN Architectures

### Site-to-Site VPN Best Practices

**AWS Site-to-Site VPN:**
```
┌─────────────────────────────────────────────────────────────┐
│              AWS Site-to-Site VPN (Redundant)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                       AWS                      │
│   ┌─────────────┐                                           │
│   │  Customer   │          ┌─────────────────────┐          │
│   │  Gateway    │◄────────►│  VPN Connection     │          │
│   │  Device     │ Tunnel 1 │  (2 tunnels auto)   │          │
│   │             │◄────────►│                     │          │
│   │  (Active)   │ Tunnel 2 │  Virtual Private    │          │
│   └─────────────┘          │  Gateway            │          │
│                            └──────────┬──────────┘          │
│                                       │                     │
│                            ┌──────────▼──────────┐          │
│                            │       VPC           │          │
│                            │   10.0.0.0/16       │          │
│                            └─────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Configuration:**
- AWS automatically provides 2 tunnel endpoints
- Configure BGP or static routing
- Use both tunnels for redundancy
- Enable acceleration for better performance

### VPN with Transit Gateway

```hcl
resource "aws_vpn_connection" "main" {
  customer_gateway_id = aws_customer_gateway.main.id
  transit_gateway_id  = aws_ec2_transit_gateway.main.id
  type                = "ipsec.1"

  # Enable acceleration
  enable_acceleration = true

  # BGP settings
  tunnel1_inside_cidr   = "169.254.100.0/30"
  tunnel2_inside_cidr   = "169.254.100.4/30"

  # IKE settings
  tunnel1_ike_versions = ["ikev2"]
  tunnel2_ike_versions = ["ikev2"]

  # Phase 1 (IKE)
  tunnel1_phase1_dh_group_numbers      = [20, 21]
  tunnel1_phase1_encryption_algorithms = ["AES256-GCM-16"]
  tunnel1_phase1_integrity_algorithms  = ["SHA2-256"]

  # Phase 2 (IPsec)
  tunnel1_phase2_dh_group_numbers      = [20, 21]
  tunnel1_phase2_encryption_algorithms = ["AES256-GCM-16"]
  tunnel1_phase2_integrity_algorithms  = ["SHA2-256"]

  tags = {
    Name = "vpn-to-datacenter"
  }
}
```

### HA VPN (GCP)

```
┌─────────────────────────────────────────────────────────────┐
│                    GCP HA VPN Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   On-Premises                       GCP                      │
│   ┌─────────────┐                 ┌─────────────┐           │
│   │  Router 1   │◄───────────────►│  HA VPN GW  │           │
│   │  (Active)   │  Tunnels 0,1    │  Interface 0│           │
│   └─────────────┘                 │             │           │
│                                   │             │           │
│   ┌─────────────┐                 │             │           │
│   │  Router 2   │◄───────────────►│  Interface 1│           │
│   │  (Active)   │  Tunnels 2,3    │             │           │
│   └─────────────┘                 └──────┬──────┘           │
│                                          │                   │
│                                   ┌──────▼──────┐           │
│                                   │Cloud Router │           │
│                                   │   (BGP)     │           │
│                                   └──────┬──────┘           │
│                                          │                   │
│                                   ┌──────▼──────┐           │
│                                   │    VPC      │           │
│                                   └─────────────┘           │
│                                                              │
│   99.99% SLA with 4 tunnels across 2 interfaces             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Multi-Cloud Connectivity

### AWS to Azure Connectivity

**Option 1: VPN over Internet**
```
AWS VPN Gateway ◄──── IPsec ────► Azure VPN Gateway
```

**Option 2: Private Connectivity via Equinix/Megaport**
```
AWS Direct Connect ◄──── Exchange ────► Azure ExpressRoute
        │                                      │
        └──────────► Megaport ◄────────────────┘
```

### Multi-Cloud Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│               Multi-Cloud Hub Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────────────┐                       │
│                    │  Cloud Exchange │                       │
│                    │  (Equinix/      │                       │
│                    │   Megaport)     │                       │
│                    └────────┬────────┘                       │
│           ┌─────────────────┼─────────────────┐             │
│           │                 │                 │             │
│    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐     │
│    │    AWS      │   │    Azure    │   │    GCP      │     │
│    │             │   │             │   │             │     │
│    │ Direct      │   │ ExpressRoute│   │ Cloud       │     │
│    │ Connect     │   │             │   │ Interconnect│     │
│    │             │   │             │   │             │     │
│    │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │     │
│    │ │  VPCs   │ │   │ │  VNets  │ │   │ │  VPCs   │ │     │
│    │ └─────────┘ │   │ └─────────┘ │   │ └─────────┘ │     │
│    └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Megaport Configuration Example

```json
{
  "product_name": "aws-azure-connection",
  "port_speed": 1000,
  "a_end": {
    "product_uid": "aws-hosted-connection-uid",
    "vlan": 100
  },
  "b_end": {
    "product_uid": "azure-expressroute-uid",
    "vlan": 200
  },
  "rate_limit": 500
}
```

## BGP Best Practices

### BGP Communities

**AWS Communities:**
| Community | Meaning |
|-----------|---------|
| 7224:8100 | Prefer Direct Connect |
| 7224:8200 | Prefer VPN |
| 7224:9100 | Local preference 100 |
| 7224:9200 | Local preference 200 |
| 7224:9300 | Local preference 300 |

**Usage Example:**
```
! Set community on routes advertised to AWS
route-map TO-AWS permit 10
  set community 7224:9300
```

### BGP Prefix Filtering

**Inbound Filter (Accept from AWS):**
```
ip prefix-list AWS-PREFIXES seq 10 permit 10.0.0.0/8 le 24
ip prefix-list AWS-PREFIXES seq 20 permit 172.16.0.0/12 le 24
ip prefix-list AWS-PREFIXES seq 100 deny 0.0.0.0/0 le 32

router bgp 65000
  neighbor 169.254.100.1 prefix-list AWS-PREFIXES in
```

**Outbound Filter (Advertise to AWS):**
```
ip prefix-list ADVERTISE-TO-AWS seq 10 permit 192.168.0.0/16
ip prefix-list ADVERTISE-TO-AWS seq 20 permit 10.100.0.0/16
ip prefix-list ADVERTISE-TO-AWS seq 100 deny 0.0.0.0/0 le 32

router bgp 65000
  neighbor 169.254.100.1 prefix-list ADVERTISE-TO-AWS out
```

### BGP Failover Tuning

**Fast Failover Configuration:**
```
router bgp 65000
  ! BFD for sub-second failover
  neighbor 169.254.100.1 fall-over bfd

  ! Aggressive timers (3 sec hold, 1 sec keepalive)
  neighbor 169.254.100.1 timers 1 3

  ! Fast external fallover
  bgp fast-external-fallover
```

## Cost Optimization

### Direct Connect vs VPN Cost Comparison

| Factor | Direct Connect | VPN |
|--------|---------------|-----|
| Port Fee | $0.30/hr (1G) | N/A |
| Data Transfer Out | $0.02-0.05/GB | $0.09/GB |
| Data Transfer In | Free | Free |
| Setup Time | 2-4 weeks | Minutes |
| Minimum Commitment | None | None |

**Break-Even Analysis:**
- At ~2 TB/month outbound, Direct Connect becomes cheaper
- Consider latency and bandwidth requirements beyond cost

### Data Transfer Optimization

**Use VPC Endpoints:**
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"

  # Gateway endpoint - no hourly charge
  vpc_endpoint_type = "Gateway"

  route_table_ids = [
    aws_route_table.private.id
  ]
}
```

**Benefits:**
- S3/DynamoDB: Free gateway endpoints
- Traffic stays on AWS backbone
- Reduces NAT Gateway data processing charges

### Bandwidth Right-Sizing

**Monitor and Adjust:**
```bash
# AWS - Check Direct Connect utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/DX \
  --metric-name ConnectionBpsIngress \
  --dimensions Name=ConnectionId,Value=dxcon-xxx \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-31T23:59:59Z \
  --period 3600 \
  --statistics Average Maximum
```

**Recommendations:**
- Start with hosted connection (lower commitment)
- Monitor utilization for 3-6 months
- Upgrade to dedicated if consistently >70% utilization
- Consider reserved capacity for predictable workloads

## Troubleshooting

### Common Issues

**BGP Session Not Establishing:**
1. Verify BGP ASN configuration on both sides
2. Check IP addressing (must be in same /30 or /31)
3. Confirm firewall allows TCP 179
4. Verify MD5 authentication (if configured)

**VPN Tunnel Flapping:**
1. Check for NAT device in path (NAT-T required)
2. Verify IKE/IPsec parameters match exactly
3. Review DPD (Dead Peer Detection) settings
4. Check for MTU issues (enable PMTUD or reduce MTU)

**Asymmetric Routing:**
1. Verify BGP route preferences
2. Check AS path prepending configuration
3. Confirm routing tables on both ends
4. Review Transit Gateway route table associations

### Diagnostic Commands

**AWS VPN Status:**
```bash
aws ec2 describe-vpn-connections \
  --vpn-connection-ids vpn-xxx \
  --query 'VpnConnections[].VgwTelemetry'
```

**BGP Route Table:**
```bash
aws ec2 describe-transit-gateway-route-tables \
  --transit-gateway-route-table-id tgw-rtb-xxx
```

**Direct Connect Virtual Interface:**
```bash
aws directconnect describe-virtual-interfaces \
  --virtual-interface-id dxvif-xxx
```

## Resources

- AWS Direct Connect: https://docs.aws.amazon.com/directconnect/
- Azure ExpressRoute: https://docs.microsoft.com/azure/expressroute/
- GCP Cloud Interconnect: https://cloud.google.com/network-connectivity/docs/interconnect
- Megaport: https://docs.megaport.com/
- Equinix Fabric: https://docs.equinix.com/
