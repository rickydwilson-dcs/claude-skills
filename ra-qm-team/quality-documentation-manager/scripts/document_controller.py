#!/usr/bin/env python3
"""
Document Controller - Quality Documentation Management
Manages document change control, version management, and training records.

This script tracks DHF/DMR/DHR documents, manages version control, tracks
approval workflows, and maintains training record compliance.

Usage:
    python document_controller.py documents.json
    python document_controller.py data.json --output json
    python document_controller.py data.json -o csv -f doc_report.csv

Author: Quality Management Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class DocumentType(Enum):
    DHF = "DHF"  # Design History File
    DMR = "DMR"  # Device Master Record
    DHR = "DHR"  # Device History Record
    SOP = "SOP"  # Standard Operating Procedure
    WI = "WI"    # Work Instruction
    FORM = "FORM"
    SPECIFICATION = "SPECIFICATION"
    PROTOCOL = "PROTOCOL"
    REPORT = "REPORT"

class DocumentStatus(Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    EFFECTIVE = "EFFECTIVE"
    OBSOLETE = "OBSOLETE"
    ARCHIVED = "ARCHIVED"

class ChangeType(Enum):
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"

@dataclass
class Document:
    doc_id: str
    title: str
    doc_type: DocumentType
    version: str
    status: DocumentStatus
    owner: str
    created_date: str
    effective_date: Optional[str] = None
    review_date: Optional[str] = None
    change_type: Optional[ChangeType] = None
    training_required: bool = False
    trained_count: int = 0
    required_training_count: int = 0
    approvers: str = ""
    change_description: str = ""

class DocumentController:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.documents: List[Document] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load document data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.metadata = data.get('metadata', {})

                for doc_data in data.get('documents', []):
                    doc_data['doc_type'] = DocumentType(doc_data['doc_type'])
                    doc_data['status'] = DocumentStatus(doc_data['status'])
                    if doc_data.get('change_type'):
                        doc_data['change_type'] = ChangeType(doc_data['change_type'])
                    self.documents.append(Document(**doc_data))

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error: Invalid data format: {e}", file=sys.stderr)
            sys.exit(3)

    def get_pending_reviews(self) -> List[Document]:
        """Get documents pending review"""
        return [d for d in self.documents if d.status == DocumentStatus.IN_REVIEW]

    def get_training_pending(self) -> List[Document]:
        """Get documents with pending training"""
        return [d for d in self.documents 
                if d.training_required and d.trained_count < d.required_training_count]

    def get_review_due(self, days: int = 30) -> List[Document]:
        """Get documents due for periodic review"""
        today = datetime.date.today()
        cutoff = today + datetime.timedelta(days=days)
        due_docs = []

        for doc in self.documents:
            if doc.review_date and doc.status == DocumentStatus.EFFECTIVE:
                review_date = datetime.datetime.strptime(doc.review_date, '%Y-%m-%d').date()
                if today <= review_date <= cutoff:
                    due_docs.append(doc)

        return sorted(due_docs, key=lambda x: x.review_date)

    def analyze_by_type(self) -> Dict[str, int]:
        """Analyze documents by type"""
        by_type = {}
        for doc in self.documents:
            doc_type = doc.doc_type.value
            by_type[doc_type] = by_type.get(doc_type, 0) + 1
        return by_type

    def analyze_by_status(self) -> Dict[str, int]:
        """Analyze documents by status"""
        by_status = {}
        for doc in self.documents:
            status = doc.status.value
            by_status[status] = by_status.get(status, 0) + 1
        return by_status

    def calculate_training_compliance(self) -> Dict[str, Any]:
        """Calculate training compliance metrics"""
        training_docs = [d for d in self.documents if d.training_required]
        if not training_docs:
            return {"total_docs": 0, "compliant": 0, "pending": 0, "compliance_rate": 0}

        compliant = [d for d in training_docs if d.trained_count >= d.required_training_count]
        pending = len(training_docs) - len(compliant)
        compliance_rate = (len(compliant) / len(training_docs)) * 100

        return {
            "total_docs": len(training_docs),
            "compliant": len(compliant),
            "pending": pending,
            "compliance_rate": round(compliance_rate, 1),
            "total_personnel_pending": sum(d.required_training_count - d.trained_count 
                                          for d in training_docs if d.trained_count < d.required_training_count)
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate text report"""
        report = []
        report.append("=" * 70)
        report.append("DOCUMENT CONTROL & VERSION MANAGEMENT REPORT")
        report.append("=" * 70)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append("")

        report.append("--- DOCUMENT SUMMARY ---")
        report.append(f"Total Documents: {len(self.documents)}")
        
        by_status = self.analyze_by_status()
        for status, count in by_status.items():
            report.append(f"  {status}: {count}")
        report.append("")

        by_type = self.analyze_by_type()
        report.append("Documents by Type:")
        for doc_type, count in sorted(by_type.items()):
            report.append(f"  • {doc_type}: {count}")
        report.append("")

        pending_reviews = self.get_pending_reviews()
        if pending_reviews:
            report.append(f"--- PENDING REVIEWS: {len(pending_reviews)} ---")
            for doc in pending_reviews:
                report.append(f"  • {doc.doc_id} v{doc.version}: {doc.title}")
                report.append(f"    Owner: {doc.owner} | Approvers: {doc.approvers}")
            report.append("")

        review_due = self.get_review_due(30)
        if review_due:
            report.append(f"--- PERIODIC REVIEWS DUE (Next 30 Days): {len(review_due)} ---")
            for doc in review_due:
                report.append(f"  • {doc.doc_id}: {doc.title} (Due: {doc.review_date})")
            report.append("")

        report.append("--- TRAINING COMPLIANCE ---")
        training = self.calculate_training_compliance()
        report.append(f"Documents Requiring Training: {training['total_docs']}")
        report.append(f"Training Compliant: {training['compliant']} ({training['compliance_rate']}%)")
        report.append(f"Training Pending: {training['pending']}")
        report.append(f"Personnel Pending Training: {training['total_personnel_pending']}")
        report.append("")

        training_pending = self.get_training_pending()
        if training_pending:
            report.append(f"--- TRAINING PENDING: {len(training_pending)} Documents ---")
            for doc in training_pending[:10]:  # Show top 10
                completion = (doc.trained_count / doc.required_training_count * 100) if doc.required_training_count > 0 else 0
                report.append(f"  • {doc.doc_id}: {doc.title}")
                report.append(f"    Training: {doc.trained_count}/{doc.required_training_count} ({completion:.0f}%)")
            report.append("")

        if verbose:
            report.append("--- RECENT CHANGES ---")
            recent = sorted(self.documents, key=lambda x: x.created_date, reverse=True)[:10]
            for doc in recent:
                report.append(f"\n{doc.doc_id} v{doc.version}: {doc.title}")
                report.append(f"  Type: {doc.doc_type.value} | Status: {doc.status.value}")
                report.append(f"  Owner: {doc.owner} | Created: {doc.created_date}")
                if doc.change_description:
                    report.append(f"  Change: {doc.change_description}")

        report.append("=" * 70)
        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate JSON report"""
        report = {
            "metadata": {
                "tool": "document_controller.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "organization": self.metadata.get('organization', 'Not specified')
            },
            "summary": {
                "total_documents": len(self.documents),
                "by_status": self.analyze_by_status(),
                "by_type": self.analyze_by_type(),
                "pending_reviews": len(self.get_pending_reviews()),
                "training_compliance": self.calculate_training_compliance()
            }
        }

        if verbose:
            report["detailed_data"] = {
                "all_documents": [asdict(d) for d in self.documents],
                "pending_reviews": [asdict(d) for d in self.get_pending_reviews()],
                "training_pending": [asdict(d) for d in self.get_training_pending()],
                "review_due": [asdict(d) for d in self.get_review_due(30)]
            }

            for doc_list in [report["detailed_data"]["all_documents"],
                            report["detailed_data"]["pending_reviews"],
                            report["detailed_data"]["training_pending"],
                            report["detailed_data"]["review_due"]]:
                for doc in doc_list:
                    doc['doc_type'] = doc['doc_type'].value
                    doc['status'] = doc['status'].value
                    if doc.get('change_type'):
                        doc['change_type'] = doc['change_type'].value

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report"""
        output = []
        output.append("Doc ID,Title,Type,Version,Status,Owner,Created,Effective,Training Required,Training Status")
        
        for doc in self.documents:
            training_status = f"{doc.trained_count}/{doc.required_training_count}" if doc.training_required else "N/A"
            output.append(f'"{doc.doc_id}","{doc.title}",{doc.doc_type.value},"{doc.version}",'
                         f'{doc.status.value},"{doc.owner}",{doc.created_date},{doc.effective_date or ""},'
                         f'{doc.training_required},"{training_status}"')
        
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Manage document change control, version management, and training records',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s documents.json
  %(prog)s documents.json --output json
  %(prog)s documents.json -o csv -f doc_report.csv -v

For more information:
ra-qm-team/quality-documentation-manager/SKILL.md
        """
    )

    parser.add_argument('input', help='Document data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        controller = DocumentController(str(input_path))

        if args.output == 'json':
            output = json.dumps(controller.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = controller.generate_csv_report()
        else:
            output = controller.generate_text_report(verbose=args.verbose)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Report saved to: {args.file}")
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
