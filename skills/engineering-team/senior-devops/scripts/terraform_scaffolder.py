#!/usr/bin/env python3
"""
Terraform Scaffolder
Infrastructure as Code template generator for AWS, GCP, and Azure.

Features:
- Multi-cloud support (AWS, GCP, Azure)
- Modular Terraform structure generation
- Remote state configuration (S3, GCS, Azure Blob)
- Environment separation (dev/staging/prod)
- Variable and output management
- Security best practices built-in

Standard library only - no external dependencies required.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class RemoteStateBackend(Enum):
    """Remote state backend types"""
    S3 = "s3"
    GCS = "gcs"
    AZURERM = "azurerm"
    LOCAL = "local"


class ModuleType(Enum):
    """Terraform module types"""
    VPC = "vpc"
    NETWORKING = "networking"
    COMPUTE = "compute"
    EKS = "eks"
    GKE = "gke"
    AKS = "aks"
    RDS = "rds"
    CLOUDSQL = "cloudsql"
    AZURE_SQL = "azure-sql"
    S3 = "s3"
    GCS = "gcs"
    BLOB = "blob"
    IAM = "iam"
    ALB = "alb"
    EC2 = "ec2"
    VNET = "vnet"


@dataclass
class ModuleConfig:
    """Configuration for a Terraform module"""
    name: str
    module_type: ModuleType
    provider: CloudProvider
    variables: Dict[str, Dict[str, Any]]
    outputs: Dict[str, str]
    resources: List[str]
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TerraformConfig:
    """Complete Terraform project configuration"""
    project_name: str
    provider: CloudProvider
    modules: List[ModuleConfig]
    environments: List[str]
    remote_state: RemoteStateBackend
    region: str
    terraform_version: str = "~> 1.6"
    use_workspaces: bool = True


@dataclass
class GeneratedFile:
    """A generated Terraform file"""
    path: str
    content: str


class TerraformScaffolder:
    """
    Terraform infrastructure scaffolder supporting multiple cloud providers.
    """

    # Module definitions per provider
    AWS_MODULES = {
        "vpc": {
            "resources": ["aws_vpc", "aws_subnet", "aws_internet_gateway", "aws_nat_gateway", "aws_route_table"],
            "variables": {
                "vpc_cidr": {"type": "string", "default": "10.0.0.0/16", "description": "CIDR block for VPC"},
                "availability_zones": {"type": "list(string)", "default": '["us-east-1a", "us-east-1b", "us-east-1c"]', "description": "Availability zones"},
                "private_subnets": {"type": "list(string)", "default": '["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]', "description": "Private subnet CIDRs"},
                "public_subnets": {"type": "list(string)", "default": '["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]', "description": "Public subnet CIDRs"}
            },
            "outputs": {
                "vpc_id": "aws_vpc.main.id",
                "private_subnet_ids": "aws_subnet.private[*].id",
                "public_subnet_ids": "aws_subnet.public[*].id"
            }
        },
        "eks": {
            "resources": ["aws_eks_cluster", "aws_eks_node_group", "aws_iam_role"],
            "variables": {
                "cluster_name": {"type": "string", "description": "EKS cluster name"},
                "cluster_version": {"type": "string", "default": "1.28", "description": "Kubernetes version"},
                "node_instance_types": {"type": "list(string)", "default": '["t3.medium"]', "description": "Instance types for nodes"},
                "node_desired_size": {"type": "number", "default": "2", "description": "Desired number of nodes"},
                "node_min_size": {"type": "number", "default": "1", "description": "Minimum number of nodes"},
                "node_max_size": {"type": "number", "default": "4", "description": "Maximum number of nodes"}
            },
            "outputs": {
                "cluster_endpoint": "aws_eks_cluster.main.endpoint",
                "cluster_ca_certificate": "aws_eks_cluster.main.certificate_authority[0].data",
                "cluster_name": "aws_eks_cluster.main.name"
            }
        },
        "rds": {
            "resources": ["aws_db_instance", "aws_db_subnet_group", "aws_security_group"],
            "variables": {
                "db_name": {"type": "string", "description": "Database name"},
                "db_username": {"type": "string", "description": "Database master username"},
                "db_password": {"type": "string", "sensitive": "true", "description": "Database master password"},
                "db_instance_class": {"type": "string", "default": "db.t3.micro", "description": "Instance class"},
                "db_engine": {"type": "string", "default": "postgres", "description": "Database engine"},
                "db_engine_version": {"type": "string", "default": "15.4", "description": "Engine version"},
                "db_allocated_storage": {"type": "number", "default": "20", "description": "Allocated storage in GB"}
            },
            "outputs": {
                "db_endpoint": "aws_db_instance.main.endpoint",
                "db_port": "aws_db_instance.main.port",
                "db_name": "aws_db_instance.main.db_name"
            }
        },
        "s3": {
            "resources": ["aws_s3_bucket", "aws_s3_bucket_versioning", "aws_s3_bucket_server_side_encryption_configuration"],
            "variables": {
                "bucket_name": {"type": "string", "description": "S3 bucket name"},
                "enable_versioning": {"type": "bool", "default": "true", "description": "Enable versioning"},
                "enable_encryption": {"type": "bool", "default": "true", "description": "Enable server-side encryption"}
            },
            "outputs": {
                "bucket_id": "aws_s3_bucket.main.id",
                "bucket_arn": "aws_s3_bucket.main.arn",
                "bucket_domain_name": "aws_s3_bucket.main.bucket_domain_name"
            }
        },
        "iam": {
            "resources": ["aws_iam_role", "aws_iam_policy", "aws_iam_role_policy_attachment"],
            "variables": {
                "role_name": {"type": "string", "description": "IAM role name"},
                "assume_role_policy": {"type": "string", "description": "Assume role policy document"}
            },
            "outputs": {
                "role_arn": "aws_iam_role.main.arn",
                "role_name": "aws_iam_role.main.name"
            }
        },
        "alb": {
            "resources": ["aws_lb", "aws_lb_target_group", "aws_lb_listener", "aws_security_group"],
            "variables": {
                "alb_name": {"type": "string", "description": "ALB name"},
                "internal": {"type": "bool", "default": "false", "description": "Internal or external ALB"},
                "enable_https": {"type": "bool", "default": "true", "description": "Enable HTTPS listener"},
                "certificate_arn": {"type": "string", "default": '""', "description": "ACM certificate ARN"}
            },
            "outputs": {
                "alb_arn": "aws_lb.main.arn",
                "alb_dns_name": "aws_lb.main.dns_name",
                "target_group_arn": "aws_lb_target_group.main.arn"
            }
        },
        "ec2": {
            "resources": ["aws_instance", "aws_security_group", "aws_key_pair"],
            "variables": {
                "instance_type": {"type": "string", "default": "t3.micro", "description": "EC2 instance type"},
                "ami_id": {"type": "string", "description": "AMI ID"},
                "key_name": {"type": "string", "description": "SSH key pair name"},
                "instance_count": {"type": "number", "default": "1", "description": "Number of instances"}
            },
            "outputs": {
                "instance_ids": "aws_instance.main[*].id",
                "public_ips": "aws_instance.main[*].public_ip",
                "private_ips": "aws_instance.main[*].private_ip"
            }
        }
    }

    GCP_MODULES = {
        "vpc": {
            "resources": ["google_compute_network", "google_compute_subnetwork", "google_compute_router", "google_compute_router_nat"],
            "variables": {
                "network_name": {"type": "string", "description": "VPC network name"},
                "subnet_cidr": {"type": "string", "default": "10.0.0.0/16", "description": "Subnet CIDR"},
                "region": {"type": "string", "description": "GCP region"}
            },
            "outputs": {
                "network_id": "google_compute_network.main.id",
                "network_name": "google_compute_network.main.name",
                "subnet_id": "google_compute_subnetwork.main.id"
            }
        },
        "gke": {
            "resources": ["google_container_cluster", "google_container_node_pool"],
            "variables": {
                "cluster_name": {"type": "string", "description": "GKE cluster name"},
                "node_count": {"type": "number", "default": "3", "description": "Number of nodes"},
                "machine_type": {"type": "string", "default": "e2-medium", "description": "Machine type for nodes"},
                "min_node_count": {"type": "number", "default": "1", "description": "Minimum nodes for autoscaling"},
                "max_node_count": {"type": "number", "default": "5", "description": "Maximum nodes for autoscaling"}
            },
            "outputs": {
                "cluster_endpoint": "google_container_cluster.main.endpoint",
                "cluster_ca_certificate": "google_container_cluster.main.master_auth[0].cluster_ca_certificate",
                "cluster_name": "google_container_cluster.main.name"
            }
        },
        "cloudsql": {
            "resources": ["google_sql_database_instance", "google_sql_database", "google_sql_user"],
            "variables": {
                "instance_name": {"type": "string", "description": "Cloud SQL instance name"},
                "database_version": {"type": "string", "default": "POSTGRES_15", "description": "Database version"},
                "tier": {"type": "string", "default": "db-f1-micro", "description": "Machine tier"},
                "db_name": {"type": "string", "description": "Database name"},
                "db_user": {"type": "string", "description": "Database user"},
                "db_password": {"type": "string", "sensitive": "true", "description": "Database password"}
            },
            "outputs": {
                "connection_name": "google_sql_database_instance.main.connection_name",
                "public_ip": "google_sql_database_instance.main.public_ip_address",
                "private_ip": "google_sql_database_instance.main.private_ip_address"
            }
        },
        "gcs": {
            "resources": ["google_storage_bucket", "google_storage_bucket_iam_member"],
            "variables": {
                "bucket_name": {"type": "string", "description": "GCS bucket name"},
                "location": {"type": "string", "default": "US", "description": "Bucket location"},
                "storage_class": {"type": "string", "default": "STANDARD", "description": "Storage class"},
                "versioning": {"type": "bool", "default": "true", "description": "Enable versioning"}
            },
            "outputs": {
                "bucket_name": "google_storage_bucket.main.name",
                "bucket_url": "google_storage_bucket.main.url",
                "bucket_self_link": "google_storage_bucket.main.self_link"
            }
        },
        "iam": {
            "resources": ["google_service_account", "google_project_iam_member", "google_service_account_key"],
            "variables": {
                "service_account_id": {"type": "string", "description": "Service account ID"},
                "display_name": {"type": "string", "description": "Service account display name"},
                "roles": {"type": "list(string)", "default": "[]", "description": "IAM roles to assign"}
            },
            "outputs": {
                "service_account_email": "google_service_account.main.email",
                "service_account_id": "google_service_account.main.unique_id"
            }
        }
    }

    AZURE_MODULES = {
        "vnet": {
            "resources": ["azurerm_virtual_network", "azurerm_subnet", "azurerm_network_security_group"],
            "variables": {
                "vnet_name": {"type": "string", "description": "Virtual network name"},
                "address_space": {"type": "list(string)", "default": '["10.0.0.0/16"]', "description": "Address space"},
                "subnet_prefixes": {"type": "list(string)", "default": '["10.0.1.0/24", "10.0.2.0/24"]', "description": "Subnet prefixes"}
            },
            "outputs": {
                "vnet_id": "azurerm_virtual_network.main.id",
                "vnet_name": "azurerm_virtual_network.main.name",
                "subnet_ids": "azurerm_subnet.main[*].id"
            }
        },
        "aks": {
            "resources": ["azurerm_kubernetes_cluster", "azurerm_kubernetes_cluster_node_pool"],
            "variables": {
                "cluster_name": {"type": "string", "description": "AKS cluster name"},
                "dns_prefix": {"type": "string", "description": "DNS prefix"},
                "node_count": {"type": "number", "default": "3", "description": "Number of nodes"},
                "vm_size": {"type": "string", "default": "Standard_D2_v2", "description": "VM size for nodes"},
                "kubernetes_version": {"type": "string", "default": "1.28", "description": "Kubernetes version"}
            },
            "outputs": {
                "cluster_id": "azurerm_kubernetes_cluster.main.id",
                "kube_config": "azurerm_kubernetes_cluster.main.kube_config_raw",
                "cluster_fqdn": "azurerm_kubernetes_cluster.main.fqdn"
            }
        },
        "azure-sql": {
            "resources": ["azurerm_mssql_server", "azurerm_mssql_database", "azurerm_mssql_firewall_rule"],
            "variables": {
                "server_name": {"type": "string", "description": "SQL Server name"},
                "database_name": {"type": "string", "description": "Database name"},
                "admin_login": {"type": "string", "description": "Admin login"},
                "admin_password": {"type": "string", "sensitive": "true", "description": "Admin password"},
                "sku_name": {"type": "string", "default": "S0", "description": "SKU name"}
            },
            "outputs": {
                "server_fqdn": "azurerm_mssql_server.main.fully_qualified_domain_name",
                "database_id": "azurerm_mssql_database.main.id"
            }
        },
        "blob": {
            "resources": ["azurerm_storage_account", "azurerm_storage_container"],
            "variables": {
                "storage_account_name": {"type": "string", "description": "Storage account name"},
                "container_name": {"type": "string", "description": "Container name"},
                "account_tier": {"type": "string", "default": "Standard", "description": "Account tier"},
                "replication_type": {"type": "string", "default": "LRS", "description": "Replication type"}
            },
            "outputs": {
                "storage_account_id": "azurerm_storage_account.main.id",
                "primary_blob_endpoint": "azurerm_storage_account.main.primary_blob_endpoint",
                "primary_access_key": "azurerm_storage_account.main.primary_access_key"
            }
        },
        "iam": {
            "resources": ["azurerm_user_assigned_identity", "azurerm_role_assignment"],
            "variables": {
                "identity_name": {"type": "string", "description": "Managed identity name"},
                "role_definition_name": {"type": "string", "default": "Contributor", "description": "Role definition"}
            },
            "outputs": {
                "identity_id": "azurerm_user_assigned_identity.main.id",
                "principal_id": "azurerm_user_assigned_identity.main.principal_id",
                "client_id": "azurerm_user_assigned_identity.main.client_id"
            }
        }
    }

    DEFAULT_REGIONS = {
        CloudProvider.AWS: "us-east-1",
        CloudProvider.GCP: "us-central1",
        CloudProvider.AZURE: "eastus"
    }

    def __init__(
        self,
        project_name: str,
        provider: str,
        modules: List[str],
        environments: List[str],
        remote_state: str = "local",
        region: Optional[str] = None,
        output_dir: str = "./infrastructure",
        verbose: bool = False
    ):
        self.project_name = project_name
        self.provider = CloudProvider(provider)
        self.requested_modules = modules
        self.environments = environments
        self.remote_state = RemoteStateBackend(remote_state)
        self.region = region or self.DEFAULT_REGIONS[self.provider]
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.generated_files: List[GeneratedFile] = []
        self.config: Optional[TerraformConfig] = None

    def run(self) -> Dict[str, Any]:
        """Execute the Terraform scaffolding"""
        if self.verbose:
            print(f"Scaffolding Terraform for {self.provider.value}", file=sys.stderr)
            print(f"Modules: {', '.join(self.requested_modules)}", file=sys.stderr)
            print(f"Output: {self.output_dir}", file=sys.stderr)

        # Build configuration
        self.config = self._build_config()

        # Generate root files
        self._generate_providers_tf()
        self._generate_backend_tf()
        self._generate_variables_tf()
        self._generate_outputs_tf()
        self._generate_main_tf()
        self._generate_versions_tf()

        # Generate modules
        for module in self.config.modules:
            self._generate_module(module)

        # Generate environment files
        for env in self.environments:
            self._generate_tfvars(env)

        # Generate example tfvars
        self._generate_tfvars_example()

        # Generate .gitignore
        self._generate_gitignore()

        # Generate README
        self._generate_readme()

        # Write all files
        files_written = self._write_files()

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "project": {
                "name": self.project_name,
                "provider": self.provider.value,
                "region": self.region,
                "remote_state": self.remote_state.value
            },
            "configuration": {
                "modules": [m.name for m in self.config.modules],
                "environments": self.environments,
                "terraform_version": self.config.terraform_version
            },
            "output_directory": str(self.output_dir),
            "files_created": len(files_written),
            "files": files_written
        }

    def _build_config(self) -> TerraformConfig:
        """Build the Terraform configuration"""
        modules: List[ModuleConfig] = []

        # Get module definitions for provider
        if self.provider == CloudProvider.AWS:
            module_defs = self.AWS_MODULES
        elif self.provider == CloudProvider.GCP:
            module_defs = self.GCP_MODULES
        else:
            module_defs = self.AZURE_MODULES

        for module_name in self.requested_modules:
            if module_name in module_defs:
                mod_def = module_defs[module_name]
                modules.append(ModuleConfig(
                    name=module_name,
                    module_type=ModuleType(module_name) if module_name in [m.value for m in ModuleType] else ModuleType.COMPUTE,
                    provider=self.provider,
                    variables=mod_def["variables"],
                    outputs=mod_def["outputs"],
                    resources=mod_def["resources"]
                ))

        return TerraformConfig(
            project_name=self.project_name,
            provider=self.provider,
            modules=modules,
            environments=self.environments,
            remote_state=self.remote_state,
            region=self.region
        )

    def _generate_providers_tf(self):
        """Generate providers.tf"""
        content = [
            '# Terraform Providers Configuration',
            f'# Generated by Terraform Scaffolder for {self.project_name}',
            ''
        ]

        if self.provider == CloudProvider.AWS:
            content.extend([
                'provider "aws" {',
                '  region = var.region',
                '',
                '  default_tags {',
                '    tags = {',
                '      Project     = var.project_name',
                '      Environment = var.environment',
                '      ManagedBy   = "terraform"',
                '    }',
                '  }',
                '}',
                ''
            ])
        elif self.provider == CloudProvider.GCP:
            content.extend([
                'provider "google" {',
                '  project = var.project_id',
                '  region  = var.region',
                '}',
                '',
                'provider "google-beta" {',
                '  project = var.project_id',
                '  region  = var.region',
                '}',
                ''
            ])
        elif self.provider == CloudProvider.AZURE:
            content.extend([
                'provider "azurerm" {',
                '  features {}',
                '}',
                '',
                '# Resource group for all resources',
                'resource "azurerm_resource_group" "main" {',
                '  name     = "${var.project_name}-${var.environment}-rg"',
                '  location = var.region',
                '',
                '  tags = {',
                '    Project     = var.project_name',
                '    Environment = var.environment',
                '    ManagedBy   = "terraform"',
                '  }',
                '}',
                ''
            ])

        self.generated_files.append(GeneratedFile("providers.tf", "\n".join(content)))

    def _generate_backend_tf(self):
        """Generate backend.tf for remote state"""
        content = [
            '# Terraform Backend Configuration',
            '# Configure remote state storage',
            ''
        ]

        if self.remote_state == RemoteStateBackend.S3:
            content.extend([
                'terraform {',
                '  backend "s3" {',
                f'    bucket         = "{self.project_name}-terraform-state"',
                f'    key            = "{self.project_name}/terraform.tfstate"',
                f'    region         = "{self.region}"',
                '    encrypt        = true',
                f'    dynamodb_table = "{self.project_name}-terraform-locks"',
                '  }',
                '}',
                '',
                '# Note: Create the S3 bucket and DynamoDB table before running terraform init',
                '# aws s3api create-bucket --bucket ' + self.project_name + '-terraform-state --region ' + self.region,
                '# aws dynamodb create-table --table-name ' + self.project_name + '-terraform-locks \\',
                '#   --attribute-definitions AttributeName=LockID,AttributeType=S \\',
                '#   --key-schema AttributeName=LockID,KeyType=HASH \\',
                '#   --billing-mode PAY_PER_REQUEST',
                ''
            ])
        elif self.remote_state == RemoteStateBackend.GCS:
            content.extend([
                'terraform {',
                '  backend "gcs" {',
                f'    bucket = "{self.project_name}-terraform-state"',
                f'    prefix = "{self.project_name}"',
                '  }',
                '}',
                '',
                '# Note: Create the GCS bucket before running terraform init',
                '# gsutil mb -l ' + self.region + ' gs://' + self.project_name + '-terraform-state',
                '# gsutil versioning set on gs://' + self.project_name + '-terraform-state',
                ''
            ])
        elif self.remote_state == RemoteStateBackend.AZURERM:
            content.extend([
                'terraform {',
                '  backend "azurerm" {',
                f'    resource_group_name  = "{self.project_name}-tfstate-rg"',
                f'    storage_account_name = "{self.project_name.replace("-", "")}tfstate"',
                '    container_name       = "tfstate"',
                f'    key                  = "{self.project_name}.terraform.tfstate"',
                '  }',
                '}',
                '',
                '# Note: Create the storage account before running terraform init',
                ''
            ])
        else:
            content.extend([
                '# Using local backend (not recommended for production)',
                '# Configure a remote backend for team collaboration',
                ''
            ])

        self.generated_files.append(GeneratedFile("backend.tf", "\n".join(content)))

    def _generate_variables_tf(self):
        """Generate variables.tf with common variables"""
        content = [
            '# Common Variables',
            '# These variables are used across all modules',
            ''
        ]

        # Common variables
        common_vars = [
            ('project_name', 'string', self.project_name, 'Project name for resource naming'),
            ('environment', 'string', 'dev', 'Environment (dev, staging, prod)'),
            ('region', 'string', self.region, 'Cloud region for resources'),
        ]

        # Provider-specific variables
        if self.provider == CloudProvider.GCP:
            common_vars.append(('project_id', 'string', None, 'GCP Project ID'))

        for var_name, var_type, default, description in common_vars:
            content.append(f'variable "{var_name}" {{')
            content.append(f'  type        = {var_type}')
            content.append(f'  description = "{description}"')
            if default is not None:
                if var_type == 'string':
                    content.append(f'  default     = "{default}"')
                else:
                    content.append(f'  default     = {default}')
            content.append('}')
            content.append('')

        # Module-specific variables
        content.append('# Module-specific Variables')
        content.append('')

        for module in self.config.modules:
            content.append(f'# Variables for {module.name} module')
            for var_name, var_config in module.variables.items():
                full_var_name = f"{module.name}_{var_name}"
                content.append(f'variable "{full_var_name}" {{')
                content.append(f'  type        = {var_config["type"]}')
                content.append(f'  description = "{var_config.get("description", "")}"')
                if 'default' in var_config:
                    if var_config['type'] == 'string':
                        content.append(f'  default     = "{var_config["default"]}"')
                    else:
                        content.append(f'  default     = {var_config["default"]}')
                if var_config.get('sensitive'):
                    content.append('  sensitive   = true')
                content.append('}')
                content.append('')

        self.generated_files.append(GeneratedFile("variables.tf", "\n".join(content)))

    def _generate_outputs_tf(self):
        """Generate outputs.tf"""
        content = [
            '# Terraform Outputs',
            '# Export values from modules for use by other tools',
            ''
        ]

        for module in self.config.modules:
            content.append(f'# Outputs from {module.name} module')
            for output_name, output_value in module.outputs.items():
                full_output_name = f"{module.name}_{output_name}"
                content.append(f'output "{full_output_name}" {{')
                content.append(f'  description = "{module.name} {output_name}"')
                content.append(f'  value       = module.{module.name}.{output_name}')
                if 'password' in output_name or 'key' in output_name or 'secret' in output_name:
                    content.append('  sensitive   = true')
                content.append('}')
                content.append('')

        self.generated_files.append(GeneratedFile("outputs.tf", "\n".join(content)))

    def _generate_main_tf(self):
        """Generate main.tf that calls modules"""
        content = [
            '# Main Terraform Configuration',
            f'# Orchestrates modules for {self.project_name}',
            ''
        ]

        for module in self.config.modules:
            content.append(f'module "{module.name}" {{')
            content.append(f'  source = "./modules/{module.name}"')
            content.append('')

            # Pass common variables
            content.append('  # Common variables')
            content.append('  project_name = var.project_name')
            content.append('  environment  = var.environment')
            if self.provider != CloudProvider.AZURE:
                content.append('  region       = var.region')
            if self.provider == CloudProvider.AZURE:
                content.append('  resource_group_name = azurerm_resource_group.main.name')
                content.append('  location            = azurerm_resource_group.main.location')
            content.append('')

            # Pass module-specific variables
            content.append('  # Module-specific variables')
            for var_name in module.variables.keys():
                full_var_name = f"{module.name}_{var_name}"
                content.append(f'  {var_name} = var.{full_var_name}')
            content.append('')

            # Add dependencies on other modules
            if module.name in ['eks', 'gke', 'aks', 'rds', 'cloudsql', 'azure-sql', 'alb', 'ec2']:
                if any(m.name in ['vpc', 'vnet', 'networking'] for m in self.config.modules):
                    vpc_module = 'vpc' if self.provider == CloudProvider.AWS else ('vnet' if self.provider == CloudProvider.AZURE else 'vpc')
                    if any(m.name == vpc_module for m in self.config.modules):
                        content.append('  # Dependencies')
                        if self.provider == CloudProvider.AWS:
                            content.append('  vpc_id     = module.vpc.vpc_id')
                            content.append('  subnet_ids = module.vpc.private_subnet_ids')
                        elif self.provider == CloudProvider.GCP:
                            content.append('  network_id = module.vpc.network_id')
                            content.append('  subnet_id  = module.vpc.subnet_id')
                        elif self.provider == CloudProvider.AZURE:
                            content.append('  vnet_id    = module.vnet.vnet_id')
                            content.append('  subnet_ids = module.vnet.subnet_ids')
                        content.append('')

            content.append('}')
            content.append('')

        self.generated_files.append(GeneratedFile("main.tf", "\n".join(content)))

    def _generate_versions_tf(self):
        """Generate versions.tf with required providers"""
        content = [
            '# Terraform Version and Provider Requirements',
            ''
        ]

        content.append('terraform {')
        content.append(f'  required_version = "{self.config.terraform_version}"')
        content.append('')
        content.append('  required_providers {')

        if self.provider == CloudProvider.AWS:
            content.extend([
                '    aws = {',
                '      source  = "hashicorp/aws"',
                '      version = "~> 5.0"',
                '    }'
            ])
        elif self.provider == CloudProvider.GCP:
            content.extend([
                '    google = {',
                '      source  = "hashicorp/google"',
                '      version = "~> 5.0"',
                '    }',
                '    google-beta = {',
                '      source  = "hashicorp/google-beta"',
                '      version = "~> 5.0"',
                '    }'
            ])
        elif self.provider == CloudProvider.AZURE:
            content.extend([
                '    azurerm = {',
                '      source  = "hashicorp/azurerm"',
                '      version = "~> 3.0"',
                '    }'
            ])

        content.append('  }')
        content.append('}')
        content.append('')

        self.generated_files.append(GeneratedFile("versions.tf", "\n".join(content)))

    def _generate_module(self, module: ModuleConfig):
        """Generate a complete module directory"""
        module_path = f"modules/{module.name}"

        # Generate module main.tf
        main_content = self._generate_module_main(module)
        self.generated_files.append(GeneratedFile(f"{module_path}/main.tf", main_content))

        # Generate module variables.tf
        vars_content = self._generate_module_variables(module)
        self.generated_files.append(GeneratedFile(f"{module_path}/variables.tf", vars_content))

        # Generate module outputs.tf
        outputs_content = self._generate_module_outputs(module)
        self.generated_files.append(GeneratedFile(f"{module_path}/outputs.tf", outputs_content))

    def _generate_module_main(self, module: ModuleConfig) -> str:
        """Generate main.tf for a module"""
        content = [
            f'# {module.name.upper()} Module',
            f'# Resources: {", ".join(module.resources)}',
            ''
        ]

        # Generate resource blocks based on module type
        if self.provider == CloudProvider.AWS:
            content.extend(self._generate_aws_resources(module))
        elif self.provider == CloudProvider.GCP:
            content.extend(self._generate_gcp_resources(module))
        elif self.provider == CloudProvider.AZURE:
            content.extend(self._generate_azure_resources(module))

        return "\n".join(content)

    def _generate_aws_resources(self, module: ModuleConfig) -> List[str]:
        """Generate AWS resource blocks"""
        content = []

        if module.name == "vpc":
            content.extend([
                'resource "aws_vpc" "main" {',
                '  cidr_block           = var.vpc_cidr',
                '  enable_dns_hostnames = true',
                '  enable_dns_support   = true',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-vpc"',
                '  }',
                '}',
                '',
                'resource "aws_internet_gateway" "main" {',
                '  vpc_id = aws_vpc.main.id',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-igw"',
                '  }',
                '}',
                '',
                'resource "aws_subnet" "public" {',
                '  count = length(var.public_subnets)',
                '',
                '  vpc_id                  = aws_vpc.main.id',
                '  cidr_block              = var.public_subnets[count.index]',
                '  availability_zone       = var.availability_zones[count.index]',
                '  map_public_ip_on_launch = true',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"',
                '  }',
                '}',
                '',
                'resource "aws_subnet" "private" {',
                '  count = length(var.private_subnets)',
                '',
                '  vpc_id            = aws_vpc.main.id',
                '  cidr_block        = var.private_subnets[count.index]',
                '  availability_zone = var.availability_zones[count.index]',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"',
                '  }',
                '}',
                '',
                'resource "aws_eip" "nat" {',
                '  count  = length(var.public_subnets)',
                '  domain = "vpc"',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-nat-eip-${count.index + 1}"',
                '  }',
                '}',
                '',
                'resource "aws_nat_gateway" "main" {',
                '  count = length(var.public_subnets)',
                '',
                '  allocation_id = aws_eip.nat[count.index].id',
                '  subnet_id     = aws_subnet.public[count.index].id',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-nat-${count.index + 1}"',
                '  }',
                '',
                '  depends_on = [aws_internet_gateway.main]',
                '}',
                '',
                'resource "aws_route_table" "public" {',
                '  vpc_id = aws_vpc.main.id',
                '',
                '  route {',
                '    cidr_block = "0.0.0.0/0"',
                '    gateway_id = aws_internet_gateway.main.id',
                '  }',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-public-rt"',
                '  }',
                '}',
                '',
                'resource "aws_route_table" "private" {',
                '  count  = length(var.private_subnets)',
                '  vpc_id = aws_vpc.main.id',
                '',
                '  route {',
                '    cidr_block     = "0.0.0.0/0"',
                '    nat_gateway_id = aws_nat_gateway.main[count.index].id',
                '  }',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-private-rt-${count.index + 1}"',
                '  }',
                '}',
                '',
                'resource "aws_route_table_association" "public" {',
                '  count = length(var.public_subnets)',
                '',
                '  subnet_id      = aws_subnet.public[count.index].id',
                '  route_table_id = aws_route_table.public.id',
                '}',
                '',
                'resource "aws_route_table_association" "private" {',
                '  count = length(var.private_subnets)',
                '',
                '  subnet_id      = aws_subnet.private[count.index].id',
                '  route_table_id = aws_route_table.private[count.index].id',
                '}',
                ''
            ])
        elif module.name == "eks":
            content.extend([
                '# EKS Cluster IAM Role',
                'resource "aws_iam_role" "cluster" {',
                '  name = "${var.project_name}-${var.environment}-eks-cluster-role"',
                '',
                '  assume_role_policy = jsonencode({',
                '    Version = "2012-10-17"',
                '    Statement = [{',
                '      Action = "sts:AssumeRole"',
                '      Effect = "Allow"',
                '      Principal = {',
                '        Service = "eks.amazonaws.com"',
                '      }',
                '    }]',
                '  })',
                '}',
                '',
                'resource "aws_iam_role_policy_attachment" "cluster_policy" {',
                '  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"',
                '  role       = aws_iam_role.cluster.name',
                '}',
                '',
                '# EKS Cluster',
                'resource "aws_eks_cluster" "main" {',
                '  name     = var.cluster_name',
                '  version  = var.cluster_version',
                '  role_arn = aws_iam_role.cluster.arn',
                '',
                '  vpc_config {',
                '    subnet_ids              = var.subnet_ids',
                '    endpoint_private_access = true',
                '    endpoint_public_access  = true',
                '  }',
                '',
                '  depends_on = [aws_iam_role_policy_attachment.cluster_policy]',
                '}',
                '',
                '# Node Group IAM Role',
                'resource "aws_iam_role" "node" {',
                '  name = "${var.project_name}-${var.environment}-eks-node-role"',
                '',
                '  assume_role_policy = jsonencode({',
                '    Version = "2012-10-17"',
                '    Statement = [{',
                '      Action = "sts:AssumeRole"',
                '      Effect = "Allow"',
                '      Principal = {',
                '        Service = "ec2.amazonaws.com"',
                '      }',
                '    }]',
                '  })',
                '}',
                '',
                'resource "aws_iam_role_policy_attachment" "node_policy" {',
                '  for_each = toset([',
                '    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",',
                '    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",',
                '    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"',
                '  ])',
                '',
                '  policy_arn = each.value',
                '  role       = aws_iam_role.node.name',
                '}',
                '',
                '# EKS Node Group',
                'resource "aws_eks_node_group" "main" {',
                '  cluster_name    = aws_eks_cluster.main.name',
                '  node_group_name = "${var.project_name}-${var.environment}-nodes"',
                '  node_role_arn   = aws_iam_role.node.arn',
                '  subnet_ids      = var.subnet_ids',
                '',
                '  instance_types = var.node_instance_types',
                '',
                '  scaling_config {',
                '    desired_size = var.node_desired_size',
                '    min_size     = var.node_min_size',
                '    max_size     = var.node_max_size',
                '  }',
                '',
                '  depends_on = [aws_iam_role_policy_attachment.node_policy]',
                '}',
                ''
            ])
        elif module.name == "rds":
            content.extend([
                'resource "aws_db_subnet_group" "main" {',
                '  name       = "${var.project_name}-${var.environment}-db-subnet"',
                '  subnet_ids = var.subnet_ids',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-db-subnet"',
                '  }',
                '}',
                '',
                'resource "aws_security_group" "db" {',
                '  name        = "${var.project_name}-${var.environment}-db-sg"',
                '  description = "Security group for RDS"',
                '  vpc_id      = var.vpc_id',
                '',
                '  ingress {',
                '    from_port   = 5432',
                '    to_port     = 5432',
                '    protocol    = "tcp"',
                '    cidr_blocks = ["10.0.0.0/16"]',
                '  }',
                '',
                '  egress {',
                '    from_port   = 0',
                '    to_port     = 0',
                '    protocol    = "-1"',
                '    cidr_blocks = ["0.0.0.0/0"]',
                '  }',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-db-sg"',
                '  }',
                '}',
                '',
                'resource "aws_db_instance" "main" {',
                '  identifier = "${var.project_name}-${var.environment}-db"',
                '',
                '  engine               = var.db_engine',
                '  engine_version       = var.db_engine_version',
                '  instance_class       = var.db_instance_class',
                '  allocated_storage    = var.db_allocated_storage',
                '  storage_encrypted    = true',
                '',
                '  db_name  = var.db_name',
                '  username = var.db_username',
                '  password = var.db_password',
                '',
                '  db_subnet_group_name   = aws_db_subnet_group.main.name',
                '  vpc_security_group_ids = [aws_security_group.db.id]',
                '',
                '  skip_final_snapshot = true',
                '  multi_az            = var.environment == "prod" ? true : false',
                '',
                '  tags = {',
                '    Name = "${var.project_name}-${var.environment}-db"',
                '  }',
                '}',
                ''
            ])
        elif module.name == "s3":
            content.extend([
                'resource "aws_s3_bucket" "main" {',
                '  bucket = var.bucket_name',
                '',
                '  tags = {',
                '    Name = var.bucket_name',
                '  }',
                '}',
                '',
                'resource "aws_s3_bucket_versioning" "main" {',
                '  bucket = aws_s3_bucket.main.id',
                '',
                '  versioning_configuration {',
                '    status = var.enable_versioning ? "Enabled" : "Suspended"',
                '  }',
                '}',
                '',
                'resource "aws_s3_bucket_server_side_encryption_configuration" "main" {',
                '  count  = var.enable_encryption ? 1 : 0',
                '  bucket = aws_s3_bucket.main.id',
                '',
                '  rule {',
                '    apply_server_side_encryption_by_default {',
                '      sse_algorithm = "AES256"',
                '    }',
                '  }',
                '}',
                '',
                'resource "aws_s3_bucket_public_access_block" "main" {',
                '  bucket = aws_s3_bucket.main.id',
                '',
                '  block_public_acls       = true',
                '  block_public_policy     = true',
                '  ignore_public_acls      = true',
                '  restrict_public_buckets = true',
                '}',
                ''
            ])
        else:
            # Generic placeholder for other modules
            content.extend([
                f'# TODO: Implement {module.name} resources',
                '# Resources: ' + ', '.join(module.resources),
                ''
            ])

        return content

    def _generate_gcp_resources(self, module: ModuleConfig) -> List[str]:
        """Generate GCP resource blocks"""
        content = []

        if module.name == "vpc":
            content.extend([
                'resource "google_compute_network" "main" {',
                '  name                    = "${var.project_name}-${var.environment}-vpc"',
                '  auto_create_subnetworks = false',
                '}',
                '',
                'resource "google_compute_subnetwork" "main" {',
                '  name          = "${var.project_name}-${var.environment}-subnet"',
                '  ip_cidr_range = var.subnet_cidr',
                '  region        = var.region',
                '  network       = google_compute_network.main.id',
                '',
                '  secondary_ip_range {',
                '    range_name    = "pods"',
                '    ip_cidr_range = "10.1.0.0/16"',
                '  }',
                '',
                '  secondary_ip_range {',
                '    range_name    = "services"',
                '    ip_cidr_range = "10.2.0.0/20"',
                '  }',
                '}',
                '',
                'resource "google_compute_router" "main" {',
                '  name    = "${var.project_name}-${var.environment}-router"',
                '  region  = var.region',
                '  network = google_compute_network.main.id',
                '}',
                '',
                'resource "google_compute_router_nat" "main" {',
                '  name                               = "${var.project_name}-${var.environment}-nat"',
                '  router                             = google_compute_router.main.name',
                '  region                             = var.region',
                '  nat_ip_allocate_option             = "AUTO_ONLY"',
                '  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"',
                '}',
                ''
            ])
        elif module.name == "gke":
            content.extend([
                'resource "google_container_cluster" "main" {',
                '  name     = var.cluster_name',
                '  location = var.region',
                '',
                '  network    = var.network_id',
                '  subnetwork = var.subnet_id',
                '',
                '  remove_default_node_pool = true',
                '  initial_node_count       = 1',
                '',
                '  ip_allocation_policy {',
                '    cluster_secondary_range_name  = "pods"',
                '    services_secondary_range_name = "services"',
                '  }',
                '',
                '  workload_identity_config {',
                '    workload_pool = "${var.project_id}.svc.id.goog"',
                '  }',
                '}',
                '',
                'resource "google_container_node_pool" "main" {',
                '  name       = "${var.cluster_name}-node-pool"',
                '  location   = var.region',
                '  cluster    = google_container_cluster.main.name',
                '  node_count = var.node_count',
                '',
                '  autoscaling {',
                '    min_node_count = var.min_node_count',
                '    max_node_count = var.max_node_count',
                '  }',
                '',
                '  node_config {',
                '    machine_type = var.machine_type',
                '',
                '    oauth_scopes = [',
                '      "https://www.googleapis.com/auth/cloud-platform"',
                '    ]',
                '',
                '    workload_metadata_config {',
                '      mode = "GKE_METADATA"',
                '    }',
                '  }',
                '}',
                ''
            ])
        else:
            content.extend([
                f'# TODO: Implement {module.name} resources for GCP',
                '# Resources: ' + ', '.join(module.resources),
                ''
            ])

        return content

    def _generate_azure_resources(self, module: ModuleConfig) -> List[str]:
        """Generate Azure resource blocks"""
        content = []

        if module.name == "vnet":
            content.extend([
                'resource "azurerm_virtual_network" "main" {',
                '  name                = "${var.project_name}-${var.environment}-vnet"',
                '  location            = var.location',
                '  resource_group_name = var.resource_group_name',
                '  address_space       = var.address_space',
                '',
                '  tags = {',
                '    Environment = var.environment',
                '  }',
                '}',
                '',
                'resource "azurerm_subnet" "main" {',
                '  count = length(var.subnet_prefixes)',
                '',
                '  name                 = "${var.project_name}-${var.environment}-subnet-${count.index + 1}"',
                '  resource_group_name  = var.resource_group_name',
                '  virtual_network_name = azurerm_virtual_network.main.name',
                '  address_prefixes     = [var.subnet_prefixes[count.index]]',
                '}',
                '',
                'resource "azurerm_network_security_group" "main" {',
                '  name                = "${var.project_name}-${var.environment}-nsg"',
                '  location            = var.location',
                '  resource_group_name = var.resource_group_name',
                '',
                '  tags = {',
                '    Environment = var.environment',
                '  }',
                '}',
                ''
            ])
        elif module.name == "aks":
            content.extend([
                'resource "azurerm_kubernetes_cluster" "main" {',
                '  name                = var.cluster_name',
                '  location            = var.location',
                '  resource_group_name = var.resource_group_name',
                '  dns_prefix          = var.dns_prefix',
                '  kubernetes_version  = var.kubernetes_version',
                '',
                '  default_node_pool {',
                '    name       = "default"',
                '    node_count = var.node_count',
                '    vm_size    = var.vm_size',
                '    vnet_subnet_id = var.subnet_ids[0]',
                '  }',
                '',
                '  identity {',
                '    type = "SystemAssigned"',
                '  }',
                '',
                '  network_profile {',
                '    network_plugin = "azure"',
                '    network_policy = "calico"',
                '  }',
                '',
                '  tags = {',
                '    Environment = var.environment',
                '  }',
                '}',
                ''
            ])
        else:
            content.extend([
                f'# TODO: Implement {module.name} resources for Azure',
                '# Resources: ' + ', '.join(module.resources),
                ''
            ])

        return content

    def _generate_module_variables(self, module: ModuleConfig) -> str:
        """Generate variables.tf for a module"""
        content = [
            f'# Variables for {module.name} module',
            ''
        ]

        # Common variables
        common_vars = [
            ('project_name', 'string', 'Project name'),
            ('environment', 'string', 'Environment'),
        ]

        if self.provider != CloudProvider.AZURE:
            common_vars.append(('region', 'string', 'Region'))
        else:
            common_vars.extend([
                ('resource_group_name', 'string', 'Resource group name'),
                ('location', 'string', 'Azure location')
            ])

        for var_name, var_type, description in common_vars:
            content.append(f'variable "{var_name}" {{')
            content.append(f'  type        = {var_type}')
            content.append(f'  description = "{description}"')
            content.append('}')
            content.append('')

        # Module-specific variables
        for var_name, var_config in module.variables.items():
            content.append(f'variable "{var_name}" {{')
            content.append(f'  type        = {var_config["type"]}')
            content.append(f'  description = "{var_config.get("description", "")}"')
            if 'default' in var_config:
                if var_config['type'] == 'string':
                    content.append(f'  default     = "{var_config["default"]}"')
                else:
                    content.append(f'  default     = {var_config["default"]}')
            if var_config.get('sensitive'):
                content.append('  sensitive   = true')
            content.append('}')
            content.append('')

        # Dependencies variables (vpc_id, subnet_ids, etc.)
        if module.name in ['eks', 'rds', 'alb', 'ec2']:
            content.extend([
                'variable "vpc_id" {',
                '  type        = string',
                '  description = "VPC ID"',
                '  default     = ""',
                '}',
                '',
                'variable "subnet_ids" {',
                '  type        = list(string)',
                '  description = "Subnet IDs"',
                '  default     = []',
                '}',
                ''
            ])
        elif module.name in ['gke', 'cloudsql']:
            content.extend([
                'variable "network_id" {',
                '  type        = string',
                '  description = "Network ID"',
                '  default     = ""',
                '}',
                '',
                'variable "subnet_id" {',
                '  type        = string',
                '  description = "Subnet ID"',
                '  default     = ""',
                '}',
                ''
            ])
        elif module.name in ['aks', 'azure-sql']:
            content.extend([
                'variable "vnet_id" {',
                '  type        = string',
                '  description = "VNet ID"',
                '  default     = ""',
                '}',
                '',
                'variable "subnet_ids" {',
                '  type        = list(string)',
                '  description = "Subnet IDs"',
                '  default     = []',
                '}',
                ''
            ])

        return "\n".join(content)

    def _generate_module_outputs(self, module: ModuleConfig) -> str:
        """Generate outputs.tf for a module"""
        content = [
            f'# Outputs for {module.name} module',
            ''
        ]

        for output_name, output_value in module.outputs.items():
            content.append(f'output "{output_name}" {{')
            content.append(f'  description = "{module.name} {output_name}"')
            content.append(f'  value       = {output_value}')
            if 'password' in output_name or 'key' in output_name or 'secret' in output_name:
                content.append('  sensitive   = true')
            content.append('}')
            content.append('')

        return "\n".join(content)

    def _generate_tfvars(self, environment: str):
        """Generate environment-specific tfvars file"""
        content = [
            f'# Terraform Variables for {environment} environment',
            f'# {self.project_name}',
            ''
        ]

        content.append(f'project_name = "{self.project_name}"')
        content.append(f'environment  = "{environment}"')
        content.append(f'region       = "{self.region}"')
        content.append('')

        if self.provider == CloudProvider.GCP:
            content.append('project_id   = "your-gcp-project-id"')
            content.append('')

        # Add module-specific variables with environment-appropriate defaults
        for module in self.config.modules:
            content.append(f'# {module.name} module variables')
            for var_name, var_config in module.variables.items():
                full_var_name = f"{module.name}_{var_name}"
                if 'default' in var_config:
                    if var_config['type'] == 'string':
                        value = var_config['default']
                        # Adjust for environment
                        if environment == 'prod' and 'micro' in str(value):
                            value = value.replace('micro', 'medium')
                        content.append(f'{full_var_name} = "{value}"')
                    else:
                        value = var_config['default']
                        # Adjust for production
                        if environment == 'prod':
                            if var_name in ['node_desired_size', 'node_count']:
                                value = '3'
                            elif var_name in ['node_max_size', 'max_node_count']:
                                value = '10'
                        content.append(f'{full_var_name} = {value}')
            content.append('')

        self.generated_files.append(GeneratedFile(f"environments/{environment}.tfvars", "\n".join(content)))

    def _generate_tfvars_example(self):
        """Generate terraform.tfvars.example"""
        content = [
            '# Terraform Variables Example',
            '# Copy this file to terraform.tfvars and fill in your values',
            ''
        ]

        content.append(f'project_name = "{self.project_name}"')
        content.append('environment  = "dev"')
        content.append(f'region       = "{self.region}"')
        content.append('')

        if self.provider == CloudProvider.GCP:
            content.append('project_id   = "your-gcp-project-id"')
            content.append('')

        for module in self.config.modules:
            content.append(f'# {module.name} module')
            for var_name, var_config in module.variables.items():
                full_var_name = f"{module.name}_{var_name}"
                if var_config.get('sensitive'):
                    content.append(f'# {full_var_name} = "SENSITIVE - set via environment variable"')
                elif 'default' in var_config:
                    if var_config['type'] == 'string':
                        content.append(f'{full_var_name} = "{var_config["default"]}"')
                    else:
                        content.append(f'{full_var_name} = {var_config["default"]}')
                else:
                    content.append(f'# {full_var_name} = ""  # Required')
            content.append('')

        self.generated_files.append(GeneratedFile("terraform.tfvars.example", "\n".join(content)))

    def _generate_gitignore(self):
        """Generate .gitignore for Terraform"""
        content = [
            '# Terraform',
            '.terraform/',
            '.terraform.lock.hcl',
            '*.tfstate',
            '*.tfstate.*',
            'crash.log',
            'crash.*.log',
            '*.tfvars',
            '!*.tfvars.example',
            'override.tf',
            'override.tf.json',
            '*_override.tf',
            '*_override.tf.json',
            '.terraformrc',
            'terraform.rc',
            '',
            '# IDE',
            '.idea/',
            '.vscode/',
            '*.swp',
            '*.swo',
            '',
            '# OS',
            '.DS_Store',
            'Thumbs.db',
            ''
        ]

        self.generated_files.append(GeneratedFile(".gitignore", "\n".join(content)))

    def _generate_readme(self):
        """Generate README.md"""
        content = [
            f'# {self.project_name} Infrastructure',
            '',
            f'Terraform infrastructure for {self.project_name} on {self.provider.value.upper()}.',
            '',
            '## Prerequisites',
            '',
            '- Terraform >= 1.6',
        ]

        if self.provider == CloudProvider.AWS:
            content.append('- AWS CLI configured with appropriate credentials')
        elif self.provider == CloudProvider.GCP:
            content.append('- Google Cloud SDK configured')
        elif self.provider == CloudProvider.AZURE:
            content.append('- Azure CLI configured')

        content.extend([
            '',
            '## Quick Start',
            '',
            '```bash',
            '# Initialize Terraform',
            'terraform init',
            '',
            '# Select workspace (environment)',
            'terraform workspace select dev || terraform workspace new dev',
            '',
            '# Plan changes',
            'terraform plan -var-file=environments/dev.tfvars',
            '',
            '# Apply changes',
            'terraform apply -var-file=environments/dev.tfvars',
            '```',
            '',
            '## Environments',
            '',
        ])

        for env in self.environments:
            content.append(f'- **{env}**: `environments/{env}.tfvars`')

        content.extend([
            '',
            '## Modules',
            '',
        ])

        for module in self.config.modules:
            content.append(f'### {module.name}')
            content.append('')
            content.append(f'Resources: {", ".join(module.resources)}')
            content.append('')

        content.extend([
            '## Security',
            '',
            '- Never commit `*.tfvars` files with sensitive values',
            '- Use environment variables for secrets: `TF_VAR_<name>=<value>`',
            '- Enable state encryption in the backend',
            '',
            '---',
            '',
            '*Generated by Terraform Scaffolder*',
            ''
        ])

        self.generated_files.append(GeneratedFile("README.md", "\n".join(content)))

    def _write_files(self) -> List[str]:
        """Write all generated files to disk"""
        files_written = []

        for gf in self.generated_files:
            file_path = self.output_dir / gf.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(gf.content)
            files_written.append(gf.path)

            if self.verbose:
                print(f"  Created: {gf.path}", file=sys.stderr)

        return files_written


class OutputFormatter:
    """Format output in different formats"""

    @staticmethod
    def format_text(results: Dict, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("TERRAFORM SCAFFOLDER REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Project info
        project = results.get("project", {})
        lines.append("PROJECT CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"Name:         {project.get('name', 'N/A')}")
        lines.append(f"Provider:     {project.get('provider', 'N/A').upper()}")
        lines.append(f"Region:       {project.get('region', 'N/A')}")
        lines.append(f"Remote State: {project.get('remote_state', 'N/A')}")
        lines.append("")

        # Configuration
        config = results.get("configuration", {})
        lines.append("TERRAFORM CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"Modules:      {', '.join(config.get('modules', []))}")
        lines.append(f"Environments: {', '.join(config.get('environments', []))}")
        lines.append(f"TF Version:   {config.get('terraform_version', 'N/A')}")
        lines.append("")

        # Files created
        lines.append("FILES CREATED")
        lines.append("-" * 40)
        lines.append(f"Output Dir:   {results.get('output_directory', 'N/A')}")
        lines.append(f"Total Files:  {results.get('files_created', 0)}")
        lines.append("")

        for f in results.get("files", []):
            lines.append(f"  - {f}")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def format_json(results: Dict) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=2, default=str)


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="Terraform Scaffolder - Generate IaC templates for AWS, GCP, and Azure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input myproject --provider aws --modules vpc,eks,rds
  %(prog)s --input myapp -p gcp -m vpc,gke,cloudsql -e dev,prod -r gcs
  %(prog)s --input myservice -p azure -m vnet,aks,blob --output-dir ./infra

Providers:
  aws       Amazon Web Services
  gcp       Google Cloud Platform
  azure     Microsoft Azure

AWS Modules:
  vpc       VPC, subnets, NAT gateway, route tables
  eks       Elastic Kubernetes Service cluster
  rds       RDS PostgreSQL/MySQL database
  s3        S3 bucket with encryption
  iam       IAM roles and policies
  alb       Application Load Balancer
  ec2       EC2 instances

GCP Modules:
  vpc       VPC network, subnets, Cloud Router
  gke       Google Kubernetes Engine cluster
  cloudsql  Cloud SQL database
  gcs       Cloud Storage bucket
  iam       Service accounts and IAM

Azure Modules:
  vnet      Virtual Network, subnets, NSG
  aks       Azure Kubernetes Service
  azure-sql Azure SQL Database
  blob      Blob Storage account
  iam       Managed identities

Remote State:
  s3        AWS S3 with DynamoDB locking
  gcs       Google Cloud Storage
  azurerm   Azure Blob Storage
  local     Local state (not recommended)
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        dest="project_name",
        help="Project name for resource naming"
    )

    parser.add_argument(
        "--provider", "-p",
        required=True,
        choices=["aws", "gcp", "azure"],
        help="Cloud provider"
    )

    parser.add_argument(
        "--modules", "-m",
        required=True,
        help="Comma-separated modules to generate"
    )

    parser.add_argument(
        "--environments", "-e",
        default="dev,staging,prod",
        help="Comma-separated environments (default: dev,staging,prod)"
    )

    parser.add_argument(
        "--remote-state", "-r",
        choices=["s3", "gcs", "azurerm", "local"],
        default="local",
        help="Remote state backend (default: local)"
    )

    parser.add_argument(
        "--region",
        help="Cloud region (default: provider-specific)"
    )

    parser.add_argument(
        "--output-dir",
        default="./infrastructure",
        help="Output directory (default: ./infrastructure)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file instead of stdout"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Parse modules and environments
    modules = [m.strip() for m in args.modules.split(",")]
    environments = [e.strip() for e in args.environments.split(",")]

    try:
        scaffolder = TerraformScaffolder(
            project_name=args.project_name,
            provider=args.provider,
            modules=modules,
            environments=environments,
            remote_state=args.remote_state,
            region=args.region,
            output_dir=args.output_dir,
            verbose=args.verbose
        )

        results = scaffolder.run()

        # Format output
        if args.output == "json":
            output = OutputFormatter.format_json(results)
        else:
            output = OutputFormatter.format_text(results, verbose=args.verbose)

        # Write output
        if args.file:
            with open(args.file, "w") as f:
                f.write(output)
            print(f"Results written to {args.file}", file=sys.stderr)
        else:
            print(output)

        sys.exit(0)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
