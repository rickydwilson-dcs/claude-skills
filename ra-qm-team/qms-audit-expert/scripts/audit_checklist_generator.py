#!/usr/bin/env python3
"""
ISO 13485 QMS Audit Checklist Generator
Generates comprehensive audit checklists based on ISO 13485:2016 clauses with risk-based focus.

This script creates detailed audit checklists covering all ISO 13485 requirements,
prioritizes high-risk areas, tracks previous findings, and calculates audit coverage.

Usage:
    python audit_checklist_generator.py audit_scope.json
    python audit_checklist_generator.py audit_scope.json --output json
    python audit_checklist_generator.py audit_scope.json -o csv -f audit_checklist.csv

Author: Quality Management Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class ISO13485Clause(Enum):
    """ISO 13485:2016 main clauses"""
    CLAUSE_4 = "4_QMS"
    CLAUSE_5 = "5_MANAGEMENT"
    CLAUSE_6 = "6_RESOURCE"
    CLAUSE_7 = "7_PRODUCT_REALIZATION"
    CLAUSE_8 = "8_MEASUREMENT"


class RiskLevel(Enum):
    """Risk-based audit prioritization"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class FindingStatus(Enum):
    """Previous finding status tracking"""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CAR = "CAR"  # Corrective Action Required
    VERIFIED = "VERIFIED"


@dataclass
class AuditQuestion:
    """Individual audit question"""
    question_id: str
    clause: str
    sub_clause: str
    question_text: str
    risk_level: RiskLevel
    audit_evidence: List[str]
    compliance_criteria: str
    notes: str = ""


@dataclass
class PreviousFinding:
    """Previous audit finding for follow-up"""
    finding_id: str
    clause: str
    description: str
    status: FindingStatus
    car_number: Optional[str]
    identified_date: str
    target_closure: str
    follow_up_required: bool = True


class ISO13485AuditChecklistGenerator:
    """Generate comprehensive ISO 13485 audit checklists"""

    def __init__(self, scope_file: str):
        self.scope_file = scope_file
        self.audit_scope: Dict[str, Any] = {}
        self.focus_areas: List[str] = []
        self.risk_areas: List[str] = []
        self.previous_findings: List[PreviousFinding] = []
        self.checklist: List[AuditQuestion] = []
        self.load_scope()

    def load_scope(self):
        """Load audit scope and configuration"""
        try:
            with open(self.scope_file, 'r') as f:
                data = json.load(f)
                self.audit_scope = data.get('audit_scope', {})
                self.focus_areas = data.get('focus_areas', [])
                self.risk_areas = data.get('risk_areas', [])

                # Load previous findings
                for finding_data in data.get('previous_findings', []):
                    finding_data['status'] = FindingStatus(finding_data['status'])
                    self.previous_findings.append(PreviousFinding(**finding_data))

        except FileNotFoundError:
            print(f"Error: Scope file not found: {self.scope_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading scope: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_clause_4_questions(self) -> List[AuditQuestion]:
        """Generate Clause 4: Quality Management System questions"""
        questions = []

        # 4.1 General Requirements
        questions.extend([
            AuditQuestion(
                question_id="4.1.1",
                clause="4.1",
                sub_clause="General Requirements",
                question_text="Has the organization established, documented, implemented, and maintained a QMS in accordance with ISO 13485 requirements?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Quality Manual", "Process maps", "QMS procedures"],
                compliance_criteria="QMS must be documented and operational"
            ),
            AuditQuestion(
                question_id="4.1.2",
                clause="4.1",
                sub_clause="General Requirements",
                question_text="Are QMS processes and their sequence and interactions identified and documented?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Process flowcharts", "Process interaction matrix"],
                compliance_criteria="All processes documented with interactions"
            ),
            AuditQuestion(
                question_id="4.1.3",
                clause="4.1",
                sub_clause="General Requirements",
                question_text="Are criteria and methods for process operation and control determined and effective?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Process procedures", "Work instructions", "KPIs"],
                compliance_criteria="Process controls defined and monitored"
            ),
        ])

        # 4.2 Documentation Requirements
        questions.extend([
            AuditQuestion(
                question_id="4.2.1",
                clause="4.2.1",
                sub_clause="General Documentation",
                question_text="Is the Quality Manual established and maintained with scope, exclusions (if any), and QMS procedures?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Quality Manual", "Document control records"],
                compliance_criteria="Current Quality Manual with all required elements"
            ),
            AuditQuestion(
                question_id="4.2.2",
                clause="4.2.2",
                sub_clause="Quality Manual",
                question_text="Does the Quality Manual include documented procedures and references to them?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Quality Manual", "Procedure index"],
                compliance_criteria="All procedures referenced in Quality Manual"
            ),
            AuditQuestion(
                question_id="4.2.3",
                clause="4.2.3",
                sub_clause="Medical Device File",
                question_text="Are Medical Device Files established and maintained for each device or device family?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Medical Device Files", "DMR checklist"],
                compliance_criteria="Complete and current device files"
            ),
            AuditQuestion(
                question_id="4.2.4",
                clause="4.2.4",
                sub_clause="Document Control",
                question_text="Is there a documented procedure for document control addressing approval, review, update, and distribution?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Document Control Procedure", "Document change records"],
                compliance_criteria="Controlled document system operational"
            ),
            AuditQuestion(
                question_id="4.2.5",
                clause="4.2.5",
                sub_clause="Record Control",
                question_text="Are quality records controlled, legible, identifiable, retrievable, and stored appropriately?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Records Control Procedure", "Record retention schedule"],
                compliance_criteria="Records properly controlled and retained"
            ),
        ])

        return questions

    def generate_clause_5_questions(self) -> List[AuditQuestion]:
        """Generate Clause 5: Management Responsibility questions"""
        questions = []

        questions.extend([
            AuditQuestion(
                question_id="5.1.1",
                clause="5.1",
                sub_clause="Management Commitment",
                question_text="Does top management demonstrate commitment to QMS development and improvement?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Management review records", "Resource allocation decisions"],
                compliance_criteria="Evidence of management commitment"
            ),
            AuditQuestion(
                question_id="5.2.1",
                clause="5.2",
                sub_clause="Customer Focus",
                question_text="Does management ensure customer requirements are determined and met?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Customer requirements documentation", "Feedback analysis"],
                compliance_criteria="Customer focus demonstrated"
            ),
            AuditQuestion(
                question_id="5.3.1",
                clause="5.3",
                sub_clause="Quality Policy",
                question_text="Is the quality policy appropriate, communicated, understood, and reviewed?",
                risk_level=RiskLevel.MEDIUM,
                audit_evidence=["Quality Policy", "Communication records", "Training records"],
                compliance_criteria="Current policy communicated and understood"
            ),
            AuditQuestion(
                question_id="5.4.1",
                clause="5.4.1",
                sub_clause="Quality Objectives",
                question_text="Are quality objectives established, measurable, and consistent with quality policy?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Quality objectives", "Performance metrics", "Objective reviews"],
                compliance_criteria="Objectives defined and monitored"
            ),
            AuditQuestion(
                question_id="5.5.1",
                clause="5.5",
                sub_clause="Responsibility and Authority",
                question_text="Are responsibilities, authorities, and interrelations defined and communicated?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Organization chart", "Job descriptions", "Responsibility matrix"],
                compliance_criteria="Clear roles and responsibilities"
            ),
            AuditQuestion(
                question_id="5.5.2",
                clause="5.5.2",
                sub_clause="Management Representative",
                question_text="Has management appointed a representative with defined QMS responsibilities?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Management representative appointment", "MR reports"],
                compliance_criteria="MR appointed with clear responsibilities"
            ),
            AuditQuestion(
                question_id="5.6.1",
                clause="5.6",
                sub_clause="Management Review",
                question_text="Does management review the QMS at planned intervals with required inputs and outputs?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Management review records", "Review schedules", "Action items"],
                compliance_criteria="Regular management reviews conducted"
            ),
        ])

        return questions

    def generate_clause_6_questions(self) -> List[AuditQuestion]:
        """Generate Clause 6: Resource Management questions"""
        questions = []

        questions.extend([
            AuditQuestion(
                question_id="6.1.1",
                clause="6.1",
                sub_clause="Provision of Resources",
                question_text="Are resources needed for QMS implementation and maintenance determined and provided?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Resource planning", "Budget allocations", "Staffing records"],
                compliance_criteria="Adequate resources provided"
            ),
            AuditQuestion(
                question_id="6.2.1",
                clause="6.2",
                sub_clause="Human Resources - Competence",
                question_text="Is personnel competence determined and maintained through education, training, and experience?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Training records", "Competency assessments", "Job descriptions"],
                compliance_criteria="Personnel competent for assigned tasks"
            ),
            AuditQuestion(
                question_id="6.2.2",
                clause="6.2",
                sub_clause="Human Resources - Training",
                question_text="Is training effectiveness evaluated and training records maintained?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Training effectiveness evaluations", "Training matrices"],
                compliance_criteria="Training effectiveness verified"
            ),
            AuditQuestion(
                question_id="6.3.1",
                clause="6.3",
                sub_clause="Infrastructure",
                question_text="Are infrastructure requirements determined and maintained (buildings, equipment, supporting services)?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Infrastructure inventory", "Maintenance records", "Qualification records"],
                compliance_criteria="Infrastructure adequate and maintained"
            ),
            AuditQuestion(
                question_id="6.4.1",
                clause="6.4",
                sub_clause="Work Environment",
                question_text="Is the work environment determined, managed, and monitored as needed?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Environmental monitoring", "Contamination control", "ESD procedures"],
                compliance_criteria="Work environment controlled"
            ),
        ])

        return questions

    def generate_clause_7_questions(self) -> List[AuditQuestion]:
        """Generate Clause 7: Product Realization questions"""
        questions = []

        # 7.1 Planning of Product Realization
        questions.extend([
            AuditQuestion(
                question_id="7.1.1",
                clause="7.1",
                sub_clause="Planning",
                question_text="Is product realization planned and developed including quality objectives and requirements?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Project plans", "Design plans", "Quality plans"],
                compliance_criteria="Product realization planned"
            ),
            AuditQuestion(
                question_id="7.2.1",
                clause="7.2",
                sub_clause="Customer Requirements",
                question_text="Are customer requirements including delivery and post-delivery activities determined?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Requirements specifications", "Contract reviews"],
                compliance_criteria="Requirements determined and documented"
            ),
            AuditQuestion(
                question_id="7.3.1",
                clause="7.3",
                sub_clause="Design and Development",
                question_text="Are design and development processes planned, controlled, and documented?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Design procedures", "Design plans", "DHF"],
                compliance_criteria="Design controls implemented"
            ),
            AuditQuestion(
                question_id="7.3.2",
                clause="7.3.2",
                sub_clause="Design Inputs",
                question_text="Are design inputs determined, documented, and reviewed for adequacy?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Design input specifications", "Input reviews"],
                compliance_criteria="Design inputs defined and approved"
            ),
            AuditQuestion(
                question_id="7.3.3",
                clause="7.3.3",
                sub_clause="Design Outputs",
                question_text="Do design outputs meet input requirements and provide appropriate information?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Design output documentation", "Verification records"],
                compliance_criteria="Design outputs complete and verified"
            ),
            AuditQuestion(
                question_id="7.3.4",
                clause="7.3.4",
                sub_clause="Design Review",
                question_text="Are systematic design reviews conducted at suitable stages?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Design review records", "Review schedules"],
                compliance_criteria="Design reviews conducted and documented"
            ),
            AuditQuestion(
                question_id="7.3.5",
                clause="7.3.5",
                sub_clause="Design Verification",
                question_text="Is design verification performed to ensure outputs meet input requirements?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Verification protocols", "Test reports", "Verification records"],
                compliance_criteria="Design verification completed"
            ),
            AuditQuestion(
                question_id="7.3.6",
                clause="7.3.6",
                sub_clause="Design Validation",
                question_text="Is design validation performed to ensure product meets user needs?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Validation protocols", "Clinical data", "Validation reports"],
                compliance_criteria="Design validation completed"
            ),
            AuditQuestion(
                question_id="7.3.7",
                clause="7.3.7",
                sub_clause="Design Transfer",
                question_text="Are design outputs transferred to manufacturing and verified?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Transfer protocols", "Manufacturing procedures", "DMR"],
                compliance_criteria="Design transfer verified"
            ),
            AuditQuestion(
                question_id="7.3.8",
                clause="7.3.8",
                sub_clause="Design Changes",
                question_text="Are design changes identified, documented, reviewed, and approved?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Change control records", "Impact assessments"],
                compliance_criteria="Design changes controlled"
            ),
        ])

        # 7.4 Purchasing
        questions.extend([
            AuditQuestion(
                question_id="7.4.1",
                clause="7.4.1",
                sub_clause="Purchasing Process",
                question_text="Is the purchasing process controlled to ensure conformity to requirements?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Purchasing procedures", "Supplier agreements"],
                compliance_criteria="Purchasing process controlled"
            ),
            AuditQuestion(
                question_id="7.4.2",
                clause="7.4.2",
                sub_clause="Purchasing Information",
                question_text="Does purchasing information adequately describe requirements?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Purchase orders", "Specifications", "Quality agreements"],
                compliance_criteria="Clear purchasing requirements"
            ),
            AuditQuestion(
                question_id="7.4.3",
                clause="7.4.3",
                sub_clause="Verification of Purchased Product",
                question_text="Are purchased products verified to meet specified requirements?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Incoming inspection records", "Supplier COAs", "Test reports"],
                compliance_criteria="Purchased product verified"
            ),
        ])

        # 7.5 Production and Service Provision
        questions.extend([
            AuditQuestion(
                question_id="7.5.1",
                clause="7.5.1",
                sub_clause="Control of Production",
                question_text="Is production and service provision planned and carried out under controlled conditions?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Work instructions", "Process validations", "DHR records"],
                compliance_criteria="Production controlled"
            ),
            AuditQuestion(
                question_id="7.5.2",
                clause="7.5.2",
                sub_clause="Cleanliness of Product",
                question_text="Are cleanliness requirements established and documented for product?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Cleaning procedures", "Cleanliness specifications"],
                compliance_criteria="Cleanliness requirements defined"
            ),
            AuditQuestion(
                question_id="7.5.3",
                clause="7.5.3",
                sub_clause="Installation Activities",
                question_text="Are installation acceptance criteria established and verification recorded?",
                risk_level=RiskLevel.MEDIUM,
                audit_evidence=["Installation procedures", "Acceptance records"],
                compliance_criteria="Installation controlled (if applicable)"
            ),
        ])

        # 7.6 Control of Monitoring and Measuring Equipment
        questions.extend([
            AuditQuestion(
                question_id="7.6.1",
                clause="7.6",
                sub_clause="Control of M&M Equipment",
                question_text="Are monitoring and measuring equipment calibrated, verified, and records maintained?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Calibration records", "Equipment inventory", "Calibration procedures"],
                compliance_criteria="M&M equipment controlled"
            ),
        ])

        return questions

    def generate_clause_8_questions(self) -> List[AuditQuestion]:
        """Generate Clause 8: Measurement, Analysis, Improvement questions"""
        questions = []

        questions.extend([
            AuditQuestion(
                question_id="8.1.1",
                clause="8.1",
                sub_clause="General",
                question_text="Are monitoring, measurement, analysis, and improvement processes planned and implemented?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["QMS procedures", "Performance metrics", "Improvement plans"],
                compliance_criteria="Monitoring processes defined"
            ),
            AuditQuestion(
                question_id="8.2.1",
                clause="8.2.1",
                sub_clause="Feedback",
                question_text="Is customer feedback including complaints monitored as a measure of QMS performance?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Feedback procedures", "Complaint records", "Trend analysis"],
                compliance_criteria="Feedback system operational"
            ),
            AuditQuestion(
                question_id="8.2.2",
                clause="8.2.2",
                sub_clause="Complaint Handling",
                question_text="Are complaints handled according to documented procedures including investigation and reporting?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Complaint handling procedure", "Complaint records", "Investigation reports"],
                compliance_criteria="Complaints properly handled"
            ),
            AuditQuestion(
                question_id="8.2.3",
                clause="8.2.3",
                sub_clause="Reporting to Regulatory Authorities",
                question_text="Are reportable events identified and reported to authorities within required timeframes?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Vigilance procedures", "Regulatory reports", "Reporting timelines"],
                compliance_criteria="Regulatory reporting compliant"
            ),
            AuditQuestion(
                question_id="8.2.4",
                clause="8.2.4",
                sub_clause="Internal Audit",
                question_text="Are internal audits conducted at planned intervals to verify QMS conformity?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Audit schedules", "Audit reports", "CAPA records"],
                compliance_criteria="Internal audits conducted"
            ),
            AuditQuestion(
                question_id="8.2.5",
                clause="8.2.5",
                sub_clause="Monitoring and Measurement of Processes",
                question_text="Are QMS processes monitored and measured to demonstrate conformity?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Process metrics", "Performance data", "Trend analysis"],
                compliance_criteria="Processes monitored"
            ),
            AuditQuestion(
                question_id="8.2.6",
                clause="8.2.6",
                sub_clause="Monitoring and Measurement of Product",
                question_text="Are product characteristics monitored and measured at appropriate stages?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Inspection records", "Test results", "Release documentation"],
                compliance_criteria="Product monitoring effective"
            ),
            AuditQuestion(
                question_id="8.3.1",
                clause="8.3",
                sub_clause="Control of Nonconforming Product",
                question_text="Is nonconforming product identified, controlled, and documented?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["Nonconformance procedure", "NCR records", "Disposition records"],
                compliance_criteria="Nonconformances controlled"
            ),
            AuditQuestion(
                question_id="8.4.1",
                clause="8.4",
                sub_clause="Analysis of Data",
                question_text="Is data collected and analyzed to demonstrate QMS suitability and effectiveness?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Data analysis reports", "Trend analysis", "Performance reviews"],
                compliance_criteria="Data analysis performed"
            ),
            AuditQuestion(
                question_id="8.5.1",
                clause="8.5.1",
                sub_clause="Improvement - General",
                question_text="Are improvement opportunities identified and implemented?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Improvement initiatives", "Quality objectives", "Performance trends"],
                compliance_criteria="Improvement demonstrated"
            ),
            AuditQuestion(
                question_id="8.5.2",
                clause="8.5.2",
                sub_clause="Corrective Action",
                question_text="Are corrective actions taken to eliminate causes of nonconformities?",
                risk_level=RiskLevel.CRITICAL,
                audit_evidence=["CAPA procedure", "CAPA records", "Effectiveness verification"],
                compliance_criteria="CAPA system effective"
            ),
            AuditQuestion(
                question_id="8.5.3",
                clause="8.5.3",
                sub_clause="Preventive Action",
                question_text="Are preventive actions taken to eliminate causes of potential nonconformities?",
                risk_level=RiskLevel.HIGH,
                audit_evidence=["Preventive action records", "Risk assessments", "Trend analysis"],
                compliance_criteria="Preventive actions implemented"
            ),
        ])

        return questions

    def generate_complete_checklist(self) -> List[AuditQuestion]:
        """Generate complete audit checklist"""
        all_questions = []

        all_questions.extend(self.generate_clause_4_questions())
        all_questions.extend(self.generate_clause_5_questions())
        all_questions.extend(self.generate_clause_6_questions())
        all_questions.extend(self.generate_clause_7_questions())
        all_questions.extend(self.generate_clause_8_questions())

        return all_questions

    def filter_by_scope(self, questions: List[AuditQuestion]) -> List[AuditQuestion]:
        """Filter questions based on audit scope"""
        if not self.focus_areas:
            return questions

        filtered = []
        for question in questions:
            for focus in self.focus_areas:
                if focus.lower() in question.clause.lower() or focus.lower() in question.sub_clause.lower():
                    filtered.append(question)
                    break

        return filtered if filtered else questions

    def prioritize_by_risk(self, questions: List[AuditQuestion]) -> List[AuditQuestion]:
        """Prioritize questions based on risk level and risk areas"""
        risk_priority = {
            RiskLevel.CRITICAL: 4,
            RiskLevel.HIGH: 3,
            RiskLevel.MEDIUM: 2,
            RiskLevel.LOW: 1
        }

        def get_priority_score(q: AuditQuestion) -> int:
            score = risk_priority[q.risk_level]
            # Boost priority if clause is in risk areas
            if any(risk.lower() in q.clause.lower() for risk in self.risk_areas):
                score += 2
            return score

        return sorted(questions, key=get_priority_score, reverse=True)

    def add_finding_follow_ups(self) -> List[Dict[str, Any]]:
        """Generate follow-up questions for previous findings"""
        follow_ups = []

        for finding in self.previous_findings:
            if finding.follow_up_required and finding.status in [FindingStatus.OPEN, FindingStatus.CAR]:
                follow_ups.append({
                    "finding_id": finding.finding_id,
                    "clause": finding.clause,
                    "description": finding.description,
                    "status": finding.status.value,
                    "car_number": finding.car_number,
                    "follow_up_questions": [
                        f"Has the root cause been identified for finding {finding.finding_id}?",
                        f"What corrective actions have been implemented?",
                        f"Has the effectiveness of corrective actions been verified?",
                        f"Are there any similar issues in other processes?"
                    ],
                    "verification_evidence": [
                        "CAPA records",
                        "Root cause analysis",
                        "Implementation evidence",
                        "Effectiveness check results"
                    ]
                })

        return follow_ups

    def calculate_coverage_metrics(self, checklist: List[AuditQuestion]) -> Dict[str, Any]:
        """Calculate audit coverage statistics"""
        total_questions = len(checklist)

        by_clause = {}
        by_risk = {}

        for question in checklist:
            # Count by clause
            clause_main = question.clause.split('.')[0]
            by_clause[clause_main] = by_clause.get(clause_main, 0) + 1

            # Count by risk level
            risk = question.risk_level.value
            by_risk[risk] = by_risk.get(risk, 0) + 1

        return {
            "total_questions": total_questions,
            "by_clause": by_clause,
            "by_risk_level": by_risk,
            "critical_questions": by_risk.get("CRITICAL", 0),
            "high_risk_questions": by_risk.get("HIGH", 0),
            "coverage_percentage": self._calculate_clause_coverage(by_clause)
        }

    def _calculate_clause_coverage(self, by_clause: Dict[str, int]) -> Dict[str, float]:
        """Calculate percentage coverage per clause"""
        # Expected minimum questions per clause for full coverage
        expected_coverage = {
            "4": 7,   # Clause 4: QMS
            "5": 7,   # Clause 5: Management
            "6": 5,   # Clause 6: Resource Management
            "7": 20,  # Clause 7: Product Realization
            "8": 13   # Clause 8: Measurement
        }

        coverage = {}
        for clause, expected in expected_coverage.items():
            actual = by_clause.get(clause, 0)
            coverage[f"Clause_{clause}"] = min(100.0, (actual / expected) * 100)

        return coverage

    def generate_audit_report_template(self) -> str:
        """Generate audit report template"""
        template = """
ISO 13485:2016 AUDIT REPORT TEMPLATE
=====================================

Audit Information:
------------------
Audit Date: [DD-MMM-YYYY]
Audit Type: [Internal/External/Surveillance/Certification]
Auditor(s): [Name(s)]
Auditee(s): [Department/Process]
Scope: [Audit Scope]

Audit Summary:
--------------
[ ] Conforming - No findings identified
[ ] Minor Nonconformities: [Number]
[ ] Major Nonconformities: [Number]
[ ] Observations: [Number]

Findings Summary:
-----------------
Finding ID | Clause | Description | Category | CAR Required
-----------|--------|-------------|----------|-------------
           |        |             |          |

Positive Observations:
----------------------
[List best practices and exemplary implementations]

Areas for Improvement:
---------------------
[List observations and improvement opportunities]

Conclusion:
-----------
[Overall audit conclusion and recommendation]

Signatures:
-----------
Lead Auditor: _________________ Date: _______
Management Representative: _________________ Date: _______

Next Steps:
-----------
[ ] CAPA initiation required
[ ] Follow-up audit scheduled: [Date]
[ ] Corrective action verification date: [Date]
"""
        return template

    def format_text_output(self, verbose: bool = False) -> str:
        """Generate human-readable text output"""
        checklist = self.generate_complete_checklist()
        checklist = self.filter_by_scope(checklist)
        checklist = self.prioritize_by_risk(checklist)

        output = []
        output.append("=" * 80)
        output.append("ISO 13485:2016 QMS AUDIT CHECKLIST")
        output.append("=" * 80)
        output.append(f"Generated: {datetime.date.today().strftime('%Y-%m-%d')}")
        output.append(f"Audit Type: {self.audit_scope.get('audit_type', 'Internal Audit')}")
        output.append(f"Scope: {self.audit_scope.get('scope_description', 'Full QMS')}")
        output.append(f"Organization: {self.audit_scope.get('organization', 'Not specified')}")
        output.append("")

        # Coverage Metrics
        metrics = self.calculate_coverage_metrics(checklist)
        output.append("--- AUDIT COVERAGE METRICS ---")
        output.append(f"Total Questions: {metrics['total_questions']}")
        output.append(f"Critical Questions: {metrics['critical_questions']}")
        output.append(f"High Risk Questions: {metrics['high_risk_questions']}")
        output.append("\nClause Coverage:")
        for clause, percentage in metrics['coverage_percentage'].items():
            output.append(f"  {clause}: {percentage:.1f}%")
        output.append("")

        # Risk Distribution
        output.append("--- RISK LEVEL DISTRIBUTION ---")
        for risk, count in metrics['by_risk_level'].items():
            output.append(f"  {risk}: {count}")
        output.append("")

        # Previous Findings Follow-up
        follow_ups = self.add_finding_follow_ups()
        if follow_ups:
            output.append(f"--- PREVIOUS FINDINGS FOLLOW-UP ({len(follow_ups)}) ---")
            for finding in follow_ups:
                output.append(f"\nFinding {finding['finding_id']} - {finding['clause']}")
                output.append(f"Status: {finding['status']}")
                output.append(f"Description: {finding['description']}")
                output.append("Follow-up Questions:")
                for q in finding['follow_up_questions']:
                    output.append(f"  • {q}")
            output.append("")

        # Audit Checklist Questions
        output.append("--- AUDIT CHECKLIST QUESTIONS ---")
        output.append(f"Total: {len(checklist)} questions")
        output.append("")

        current_clause = None
        for question in checklist:
            clause_main = question.clause.split('.')[0]
            if clause_main != current_clause:
                current_clause = clause_main
                output.append(f"\n{'=' * 80}")
                output.append(f"CLAUSE {clause_main}: {self._get_clause_title(clause_main)}")
                output.append('=' * 80)

            output.append(f"\n[{question.question_id}] {question.sub_clause}")
            output.append(f"Risk Level: {question.risk_level.value}")
            output.append(f"Question: {question.question_text}")
            output.append(f"Compliance Criteria: {question.compliance_criteria}")
            output.append(f"Evidence Required: {', '.join(question.audit_evidence)}")
            output.append(f"Finding: [ ] Conforming  [ ] Minor NC  [ ] Major NC  [ ] Observation")
            output.append(f"Notes: _____________________________________")

            if verbose:
                output.append(f"Sub-clause: {question.clause}")

        # Audit Report Template
        output.append("\n\n")
        output.append(self.generate_audit_report_template())

        output.append("\n" + "=" * 80)
        output.append(f"End of Audit Checklist - {len(checklist)} questions generated")
        output.append("=" * 80)

        return "\n".join(output)

    def format_json_output(self, verbose: bool = False) -> str:
        """Generate JSON output"""
        checklist = self.generate_complete_checklist()
        checklist = self.filter_by_scope(checklist)
        checklist = self.prioritize_by_risk(checklist)

        questions_dict = []
        for q in checklist:
            q_dict = asdict(q)
            q_dict['risk_level'] = q.risk_level.value
            questions_dict.append(q_dict)

        follow_ups = self.add_finding_follow_ups()
        metrics = self.calculate_coverage_metrics(checklist)

        output = {
            "metadata": {
                "tool": "audit_checklist_generator.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "standard": "ISO 13485:2016"
            },
            "audit_scope": self.audit_scope,
            "coverage_metrics": metrics,
            "checklist": questions_dict,
            "previous_findings_follow_up": follow_ups,
            "audit_report_template": self.generate_audit_report_template()
        }

        return json.dumps(output, indent=2)

    def format_csv_output(self) -> str:
        """Generate CSV output"""
        checklist = self.generate_complete_checklist()
        checklist = self.filter_by_scope(checklist)
        checklist = self.prioritize_by_risk(checklist)

        output = []
        output.append("Question ID,Clause,Sub-Clause,Risk Level,Question,Compliance Criteria,Evidence Required,Finding,Notes")

        for q in checklist:
            evidence = '; '.join(q.audit_evidence)
            output.append(
                f'"{q.question_id}","{q.clause}","{q.sub_clause}",{q.risk_level.value},'
                f'"{q.question_text}","{q.compliance_criteria}","{evidence}",'
                f'"","'
            )

        return "\n".join(output)

    def _get_clause_title(self, clause: str) -> str:
        """Get ISO 13485 clause title"""
        titles = {
            "4": "QUALITY MANAGEMENT SYSTEM",
            "5": "MANAGEMENT RESPONSIBILITY",
            "6": "RESOURCE MANAGEMENT",
            "7": "PRODUCT REALIZATION",
            "8": "MEASUREMENT, ANALYSIS, IMPROVEMENT"
        }
        return titles.get(clause, "")


def main():
    parser = argparse.ArgumentParser(
        description='Generate comprehensive ISO 13485:2016 audit checklists with risk-based focus',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audit_scope.json
  %(prog)s audit_scope.json --output json
  %(prog)s audit_scope.json -o csv -f audit_checklist.csv -v

Input JSON Format:
  {
    "audit_scope": {
      "audit_type": "Internal Audit",
      "scope_description": "Full QMS Review",
      "organization": "Acme Medical Devices"
    },
    "focus_areas": ["7.3", "8.2"],
    "risk_areas": ["Design Controls", "CAPA"],
    "previous_findings": [
      {
        "finding_id": "F-2024-001",
        "clause": "7.3.4",
        "description": "Design review not conducted at all stages",
        "status": "OPEN",
        "car_number": "CAR-2024-015",
        "identified_date": "2024-10-15",
        "target_closure": "2024-12-15"
      }
    ]
  }

For more information:
ra-qm-team/qms-audit-expert/SKILL.md
        """
    )

    parser.add_argument('input', help='Audit scope configuration file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        generator = ISO13485AuditChecklistGenerator(str(input_path))

        if args.output == 'json':
            output = generator.format_json_output(verbose=args.verbose)
        elif args.output == 'csv':
            output = generator.format_csv_output()
        else:
            output = generator.format_text_output(verbose=args.verbose)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Audit checklist saved to: {args.file}")
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
