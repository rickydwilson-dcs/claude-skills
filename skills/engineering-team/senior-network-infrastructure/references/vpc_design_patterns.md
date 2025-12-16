# VPC Design Patterns

Comprehensive guide to VPC/VNet architecture patterns for AWS, Azure, and GCP.

## Overview

This reference covers proven VPC design patterns for enterprise deployments, from single-VPC architectures to complex multi-region, multi-account topologies. Each pattern includes use cases, trade-offs, and implementation considerations.

## Single VPC Architectures

### Basic 3-Tier Architecture

The foundational pattern for web applications with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                         VPC (10.0.0.0/16)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Public     │  │  Public     │  │  Public     │         │
│  │  Subnet     │  │  Subnet     │  │  Subnet     │         │
│  │  AZ-A       │  │  AZ-B       │  │  AZ-C       │         │
│  │ 10.0.1.0/24 │  │ 10.0.2.0/24 │  │ 10.0.3.0/24 │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Private    │  │  Private    │  │  Private    │         │
│  │  Subnet     │  │  Subnet     │  │  Subnet     │         │
│  │  AZ-A       │  │  AZ-B       │  │  AZ-C       │         │
│  │ 10.0.11.0/24│  │ 10.0.12.0/24│  │ 10.0.13.0/24│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Database   │  │  Database   │  │  Database   │         │
│  │  Subnet     │  │  Subnet     │  │  Subnet     │         │
│  │  AZ-A       │  │  AZ-B       │  │  AZ-C       │         │
│  │ 10.0.21.0/24│  │ 10.0.22.0/24│  │ 10.0.23.0/24│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- **Public Subnets**: Load balancers, bastion hosts, NAT gateways
- **Private Subnets**: Application servers, compute workloads
- **Database Subnets**: RDS, ElastiCache, data stores

**Best Practices:**
- Use /16 for VPC CIDR (65,536 IPs)
- Use /24 for subnets (251 usable IPs each)
- Deploy across minimum 3 AZs for high availability
- Place NAT Gateway in each AZ for resilience

### 4-Tier Architecture (with Cache Layer)

Extended pattern adding dedicated cache tier for high-performance applications.

```
Public → Application → Cache → Database
```

**Additional Subnet:**
- Cache Subnet: ElastiCache, Memcached, Redis clusters
- Typically /27 subnets (27 usable IPs) - cache clusters are small

**Use Cases:**
- High-traffic e-commerce platforms
- Real-time analytics dashboards
- Content delivery systems

## Hub-Spoke Topology

### Transit Gateway Architecture (AWS)

Central hub connecting multiple VPCs with shared services.

```
                    ┌─────────────────┐
                    │  Transit        │
                    │  Gateway        │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │  Shared     │   │  Production │   │  Development│
    │  Services   │   │  VPC        │   │  VPC        │
    │  VPC        │   │             │   │             │
    │  (Hub)      │   │  (Spoke)    │   │  (Spoke)    │
    └─────────────┘   └─────────────┘   └─────────────┘
```

**Hub VPC Contains:**
- VPN/Direct Connect termination
- Centralized NAT
- Shared security services
- DNS resolution (Route 53 Resolver)
- Bastion/jump servers

**Spoke VPCs Contain:**
- Application workloads
- Environment-specific resources
- No direct internet access (routes through hub)

**CIDR Planning:**
```
Hub VPC:         10.0.0.0/16
Production VPC:  10.1.0.0/16
Development VPC: 10.2.0.0/16
Staging VPC:     10.3.0.0/16
```

**Transit Gateway Route Tables:**
- Shared services route table (hub access)
- Production route table (isolated)
- Non-production route table (dev/staging shared)

### Virtual WAN Architecture (Azure)

Azure's equivalent hub-spoke using Virtual WAN.

```
                    ┌─────────────────┐
                    │  Virtual WAN    │
                    │  Hub            │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │  Shared     │   │  Production │   │  Development│
    │  Services   │   │  VNet       │   │  VNet       │
    │  VNet       │   │             │   │             │
    └─────────────┘   └─────────────┘   └─────────────┘
```

**Key Differences from AWS:**
- Virtual WAN Hub is Azure-managed
- Built-in VPN Gateway and ExpressRoute support
- Automatic route propagation
- Global transit connectivity between hubs

## Multi-Region Architectures

### Active-Active Multi-Region

Both regions serve traffic simultaneously for global applications.

```
           Region A                          Region B
    ┌─────────────────┐               ┌─────────────────┐
    │  VPC A          │               │  VPC B          │
    │  10.0.0.0/16    │◄─────────────►│  10.1.0.0/16    │
    │                 │   VPC Peering │                 │
    │  ┌───────────┐  │   or Transit  │  ┌───────────┐  │
    │  │App Servers│  │   Gateway     │  │App Servers│  │
    │  └───────────┘  │               │  └───────────┘  │
    │  ┌───────────┐  │               │  ┌───────────┐  │
    │  │ Database  │◄─┼───────────────┼──►│ Database  │  │
    │  │ (Primary) │  │   Replication │  │ (Replica) │  │
    │  └───────────┘  │               │  └───────────┘  │
    └─────────────────┘               └─────────────────┘
           │                                   │
           └───────────┬───────────────────────┘
                       │
              ┌────────▼────────┐
              │  Global Load    │
              │  Balancer       │
              │  (Route 53/     │
              │   Cloud DNS)    │
              └─────────────────┘
```

**Implementation Considerations:**
- Non-overlapping CIDR blocks required
- Database replication strategy (async vs sync)
- Global load balancer for traffic distribution
- Latency-based routing for user proximity

### Active-Passive (DR) Pattern

Primary region handles all traffic; secondary for disaster recovery.

**RPO/RTO Targets:**
| Tier | RPO | RTO |
|------|-----|-----|
| Critical | < 1 hour | < 4 hours |
| Standard | < 24 hours | < 24 hours |
| Non-critical | < 72 hours | < 72 hours |

**DR Components:**
- Pilot light: Minimal infrastructure always running
- Warm standby: Scaled-down version of production
- Hot standby: Full production replica

## Landing Zone Patterns

### AWS Control Tower Landing Zone

Multi-account architecture with organizational units.

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Organization                          │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ Security OU   │  │ Infrastructure│  │ Workloads OU  │   │
│  │               │  │ OU            │  │               │   │
│  │ ┌───────────┐ │  │ ┌───────────┐ │  │ ┌───────────┐ │   │
│  │ │Log Archive│ │  │ │ Network   │ │  │ │Production │ │   │
│  │ │Account    │ │  │ │ Account   │ │  │ │Account    │ │   │
│  │ └───────────┘ │  │ └───────────┘ │  │ └───────────┘ │   │
│  │ ┌───────────┐ │  │ ┌───────────┐ │  │ ┌───────────┐ │   │
│  │ │Security   │ │  │ │ Shared    │ │  │ │Development│ │   │
│  │ │Tooling    │ │  │ │ Services  │ │  │ │Account    │ │   │
│  │ └───────────┘ │  │ └───────────┘ │  │ └───────────┘ │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Account Types:**
- **Management Account**: Organization root, billing
- **Log Archive**: Centralized logging, CloudTrail
- **Security Tooling**: GuardDuty, Security Hub, IAM Identity Center
- **Network Account**: Transit Gateway, Direct Connect, DNS
- **Shared Services**: CI/CD, artifact repositories
- **Workload Accounts**: Application environments

### Azure Landing Zone

Enterprise-scale architecture with management groups.

```
Root Management Group
├── Platform
│   ├── Identity (Azure AD, Key Vault)
│   ├── Management (Log Analytics, Automation)
│   └── Connectivity (Hub VNets, ExpressRoute)
├── Landing Zones
│   ├── Corp (Internal applications)
│   └── Online (Internet-facing)
├── Sandbox
│   └── Developer testing
└── Decommissioned
    └── Retired subscriptions
```

## Network Segmentation Strategies

### Micro-Segmentation Pattern

Fine-grained network isolation for zero-trust architecture.

```
┌─────────────────────────────────────────────────────────────┐
│                         VPC                                  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Web Tier                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │   │
│  │  │ Web SG  │  │ Web SG  │  │ Web SG  │              │   │
│  │  │ Pod 1   │  │ Pod 2   │  │ Pod 3   │              │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘              │   │
│  └───────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │                         │
│          ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    API Tier                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │   │
│  │  │ API SG  │  │ API SG  │  │ API SG  │              │   │
│  │  │ Svc A   │  │ Svc B   │  │ Svc C   │              │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘              │   │
│  └───────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │                         │
│          ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Database Tier                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │   │
│  │  │ DB SG   │  │ DB SG   │  │ DB SG   │              │   │
│  │  │ Primary │  │ Read    │  │ Cache   │              │   │
│  │  └─────────┘  └─────────┘  └─────────┘              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Principles:**
- Each service has dedicated security group
- Allow only required ports between services
- Default deny all traffic
- Log all inter-service communication

### Environment Isolation Pattern

Separate VPCs per environment with controlled connectivity.

```
┌───────────────────────────────────────────────────────────┐
│                    Transit Gateway                         │
└───────────────────────────────────────────────────────────┘
         │              │              │              │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │   Dev   │    │ Staging │    │  Prod   │    │ Shared  │
    │   VPC   │    │   VPC   │    │   VPC   │    │Services │
    │         │    │         │    │         │    │   VPC   │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

**Route Table Configuration:**
- Dev: Access to Shared Services only
- Staging: Access to Shared Services + limited Prod read
- Prod: Access to Shared Services, no Dev/Staging access
- Shared Services: Access to all environments

## CIDR Planning Best Practices

### IP Address Space Allocation

**RFC 1918 Private Ranges:**
| Range | CIDR | Total IPs | Use Case |
|-------|------|-----------|----------|
| 10.0.0.0/8 | 10.0.0.0 - 10.255.255.255 | 16,777,216 | Large enterprise |
| 172.16.0.0/12 | 172.16.0.0 - 172.31.255.255 | 1,048,576 | Medium enterprise |
| 192.168.0.0/16 | 192.168.0.0 - 192.168.255.255 | 65,536 | Small deployments |

### Enterprise CIDR Plan Example

```
10.0.0.0/8 - Enterprise allocation
├── 10.0.0.0/12 - US East Region
│   ├── 10.0.0.0/16 - Production
│   ├── 10.1.0.0/16 - Staging
│   ├── 10.2.0.0/16 - Development
│   └── 10.3.0.0/16 - Shared Services
├── 10.16.0.0/12 - US West Region
│   ├── 10.16.0.0/16 - Production
│   └── ...
├── 10.32.0.0/12 - EU Region
│   └── ...
└── 10.48.0.0/12 - APAC Region
    └── ...
```

### Subnet Sizing Guidelines

| Workload Type | Recommended CIDR | Usable IPs | Notes |
|---------------|------------------|------------|-------|
| Public/Web | /24 | 251 | Load balancers, NAT |
| Application | /22 | 1,019 | Compute instances |
| Database | /26 | 59 | RDS, managed DBs |
| Cache | /27 | 27 | ElastiCache, Redis |
| Management | /28 | 11 | Bastion, monitoring |
| VPN | /28 | 11 | VPN endpoints |

### Reserved IP Addresses

**AWS Reserves 5 IPs per subnet:**
- .0 - Network address
- .1 - VPC router
- .2 - DNS server
- .3 - Future use
- .255 - Broadcast (not usable but reserved)

**Azure Reserves 5 IPs per subnet:**
- .0 - Network address
- .1 - Default gateway
- .2, .3 - Azure DNS
- .255 - Broadcast

**GCP Reserves 4 IPs per subnet:**
- .0 - Network address
- .1 - Default gateway
- Second-to-last - Future use
- .255 - Broadcast

## Cloud-Specific Patterns

### AWS-Specific Considerations

**VPC Endpoints:**
- Gateway endpoints: S3, DynamoDB (free)
- Interface endpoints: All other services (cost per hour + data)
- Use PrivateLink for private connectivity

**VPC Sharing:**
- Share subnets across accounts using RAM
- Centralize network management
- Reduce VPC count and complexity

### Azure-Specific Considerations

**Service Endpoints:**
- Direct connectivity to Azure services
- Traffic stays on Azure backbone
- No additional cost

**Private Link:**
- Private connectivity to PaaS services
- Private IP in your VNet
- Works across peered VNets and VPN

### GCP-Specific Considerations

**Shared VPC:**
- Host project owns network
- Service projects use shared subnets
- Centralized network control

**VPC Service Controls:**
- Define security perimeters
- Restrict data exfiltration
- Control API access

## Implementation Checklist

### New VPC Setup

- [ ] Define CIDR block (non-overlapping with existing)
- [ ] Plan subnet layout per AZ
- [ ] Enable DNS hostnames and resolution
- [ ] Create Internet Gateway (if public access needed)
- [ ] Create NAT Gateway per AZ
- [ ] Configure route tables (public, private, database)
- [ ] Enable VPC Flow Logs
- [ ] Create VPC endpoints for AWS services
- [ ] Tag all resources consistently

### Multi-Region Expansion

- [ ] Verify CIDR non-overlap
- [ ] Choose connectivity method (TGW, VPC Peering)
- [ ] Plan failover routing
- [ ] Configure cross-region DNS
- [ ] Establish database replication
- [ ] Test failover procedures
- [ ] Document recovery playbooks

## Resources

- AWS VPC Documentation: https://docs.aws.amazon.com/vpc/
- Azure Virtual Network: https://docs.microsoft.com/azure/virtual-network/
- GCP VPC: https://cloud.google.com/vpc/docs
- RFC 1918: https://tools.ietf.org/html/rfc1918
