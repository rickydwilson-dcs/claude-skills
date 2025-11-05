#!/usr/bin/env python3
"""
Module: fda_submission_planner.py
Description: Plan and track FDA regulatory submissions (510(k), PMA, De Novo) for medical devices

This tool helps medical device companies plan FDA submissions by analyzing device classification,
recommending submission pathways, generating document checklists, calculating timelines, and
tracking FDA interactions.

Usage:
    python fda_submission_planner.py device_info.json
    python fda_submission_planner.py device_info.json --output json
    python fda_submission_planner.py device_info.json -o csv --file submission_plan.csv
    python fda_submission_planner.py sample  # Create sample JSON file

Author: claude-skills
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class DeviceClass(Enum):
    """FDA Device Classification"""
    CLASS_I = "Class I"
    CLASS_II = "Class II"
    CLASS_III = "Class III"


class SubmissionType(Enum):
    """FDA Submission Types"""
    TRADITIONAL_510K = "510(k) Traditional"
    SPECIAL_510K = "510(k) Special"
    ABBREVIATED_510K = "510(k) Abbreviated"
    PMA = "PMA (Premarket Approval)"
    DE_NOVO = "De Novo Classification Request"
    HDE = "HDE (Humanitarian Device Exemption)"


class RiskLevel(Enum):
    """Device Risk Levels"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


def analyze_device_classification(device_info: Dict[str, Any]) -> Tuple[DeviceClass, RiskLevel]:
    """
    Analyze device information to determine FDA classification.

    Args:
        device_info: Dictionary containing device characteristics

    Returns:
        Tuple of (DeviceClass, RiskLevel)
    """
    intended_use = device_info.get("intended_use", "").lower()
    invasiveness = device_info.get("invasiveness", "").lower()
    duration = device_info.get("duration_of_contact", "").lower()
    technological_characteristics = device_info.get("technological_characteristics", {})

    # Class III indicators (High Risk)
    class_iii_indicators = [
        "life-sustaining" in intended_use,
        "life-supporting" in intended_use,
        "implantable" in intended_use and invasiveness == "invasive",
        invasiveness == "invasive" and duration in ["long-term", "permanent"],
        "active implantable" in intended_use
    ]

    # Class II indicators (Moderate Risk)
    class_ii_indicators = [
        invasiveness == "invasive" and duration == "short-term",
        "diagnostic" in intended_use or "screening" in intended_use,
        "therapeutic" in intended_use and not any(class_iii_indicators),
        technological_characteristics.get("software_as_primary_function", False),
        technological_characteristics.get("ai_ml_enabled", False) and not any(class_iii_indicators),
        "active" in device_info.get("device_type", "").lower() and not any(class_iii_indicators)
    ]

    # Determine classification
    if any(class_iii_indicators):
        return DeviceClass.CLASS_III, RiskLevel.HIGH
    elif any(class_ii_indicators):
        return DeviceClass.CLASS_II, RiskLevel.MODERATE
    else:
        return DeviceClass.CLASS_I, RiskLevel.LOW


def recommend_submission_pathway(
    device_class: DeviceClass,
    risk_level: RiskLevel,
    device_info: Dict[str, Any]
) -> Tuple[SubmissionType, str]:
    """
    Recommend optimal FDA submission pathway based on device characteristics.

    Args:
        device_class: Determined device class
        risk_level: Assessed risk level
        device_info: Device information dictionary

    Returns:
        Tuple of (SubmissionType, reasoning string)
    """
    has_predicate = device_info.get("predicate_device", {}).get("identified", False)
    is_novel = device_info.get("novel_technology", False)
    design_changes = device_info.get("design_changes_from_predicate", "").lower()
    rare_disease = device_info.get("rare_disease_indication", False)
    patient_population = device_info.get("annual_patient_population", 0)

    # HDE pathway for rare diseases
    if rare_disease and patient_population < 8000:
        return (
            SubmissionType.HDE,
            "Device treats rare disease (<8,000 patients/year in US). HDE pathway recommended."
        )

    # Class III PMA pathway
    if device_class == DeviceClass.CLASS_III:
        if is_novel or not has_predicate:
            return (
                SubmissionType.PMA,
                "Class III device with novel technology or no predicate. PMA required."
            )
        else:
            return (
                SubmissionType.TRADITIONAL_510K,
                "Class III device with valid predicate. 510(k) pathway possible if substantial equivalence demonstrated."
            )

    # De Novo pathway for novel Class I/II devices
    if is_novel and not has_predicate:
        return (
            SubmissionType.DE_NOVO,
            "Novel device with no predicate. De Novo classification request recommended to establish new device type."
        )

    # Class II pathways
    if device_class == DeviceClass.CLASS_II:
        if not has_predicate:
            return (
                SubmissionType.DE_NOVO,
                "No predicate device identified. De Novo pathway recommended."
            )
        elif design_changes == "manufacturing only":
            return (
                SubmissionType.SPECIAL_510K,
                "Design changes limited to manufacturing. Special 510(k) provides faster review (30 days)."
            )
        elif device_info.get("guidance_document_available", False):
            return (
                SubmissionType.ABBREVIATED_510K,
                "FDA guidance document available for device type. Abbreviated 510(k) with summary report recommended."
            )
        else:
            return (
                SubmissionType.TRADITIONAL_510K,
                "Standard 510(k) pathway. Valid predicate identified with technological comparison required."
            )

    # Class I - typically exempt
    return (
        SubmissionType.TRADITIONAL_510K,
        "Class I device. Verify if 510(k) exempt under 21 CFR. If not exempt, Traditional 510(k) required."
    )


def generate_document_checklist(submission_type: SubmissionType, device_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate FDA submission document checklist based on submission type.

    Args:
        submission_type: Recommended submission type
        device_info: Device characteristics

    Returns:
        List of required documents with CFR references
    """
    checklist = []

    # Common documents for all submissions
    common_docs = [
        {
            "section": "Administrative",
            "document": "FDA Cover Letter",
            "cfr_reference": "21 CFR 807.87",
            "required": True,
            "description": "Submission cover letter with device identification"
        },
        {
            "section": "Administrative",
            "document": "510(k) Summary or Statement",
            "cfr_reference": "21 CFR 807.92/807.93",
            "required": True,
            "description": "Public summary or statement of safety/effectiveness"
        },
        {
            "section": "Device Description",
            "document": "Device Description",
            "cfr_reference": "21 CFR 807.87(b)",
            "required": True,
            "description": "Detailed device description, specifications, and components"
        },
        {
            "section": "Device Description",
            "document": "Indications for Use",
            "cfr_reference": "21 CFR 807.87(e)",
            "required": True,
            "description": "Clinical indications, patient population, and contraindications"
        },
        {
            "section": "Labeling",
            "document": "Proposed Labeling",
            "cfr_reference": "21 CFR 807.87(e)",
            "required": True,
            "description": "Instructions for use, warnings, and contraindications"
        }
    ]

    # 510(k) specific documents
    if "510(k)" in submission_type.value:
        checklist.extend(common_docs)
        checklist.extend([
            {
                "section": "Substantial Equivalence",
                "document": "Predicate Device Comparison",
                "cfr_reference": "21 CFR 807.87(f)",
                "required": True,
                "description": "Detailed comparison to predicate device(s)"
            },
            {
                "section": "Testing",
                "document": "Performance Testing",
                "cfr_reference": "21 CFR 807.87(h)",
                "required": True,
                "description": "Bench testing, biocompatibility, sterilization validation"
            },
            {
                "section": "Testing",
                "document": "Software Validation",
                "cfr_reference": "21 CFR 820.30(g)",
                "required": device_info.get("technological_characteristics", {}).get("software_as_primary_function", False),
                "description": "Software verification and validation documentation"
            },
            {
                "section": "Testing",
                "document": "Biocompatibility Testing",
                "cfr_reference": "ISO 10993",
                "required": device_info.get("patient_contact", False),
                "description": "ISO 10993 biocompatibility evaluation"
            }
        ])

        if device_info.get("sterile", False):
            checklist.append({
                "section": "Testing",
                "document": "Sterilization Validation",
                "cfr_reference": "ISO 11135/11137",
                "required": True,
                "description": "Sterilization process validation per ISO standards"
            })

    # PMA specific documents
    elif submission_type == SubmissionType.PMA:
        checklist.extend([
            {
                "section": "Administrative",
                "document": "PMA Cover Letter",
                "cfr_reference": "21 CFR 814.20",
                "required": True,
                "description": "PMA application cover letter"
            },
            {
                "section": "Manufacturing",
                "document": "Manufacturing Information",
                "cfr_reference": "21 CFR 814.20(b)(4)",
                "required": True,
                "description": "Complete manufacturing processes and facilities"
            },
            {
                "section": "Clinical",
                "document": "Clinical Study Protocol",
                "cfr_reference": "21 CFR 814.20(b)(6)",
                "required": True,
                "description": "Clinical investigation protocol and study design"
            },
            {
                "section": "Clinical",
                "document": "Clinical Study Report",
                "cfr_reference": "21 CFR 814.20(b)(6)",
                "required": True,
                "description": "Complete clinical trial results and statistical analysis"
            },
            {
                "section": "Risk",
                "document": "Risk Analysis Report",
                "cfr_reference": "ISO 14971",
                "required": True,
                "description": "Comprehensive risk management per ISO 14971"
            },
            {
                "section": "Risk",
                "document": "Benefit-Risk Assessment",
                "cfr_reference": "21 CFR 814.20(b)(3)",
                "required": True,
                "description": "Clinical benefit-risk analysis"
            }
        ])

    # De Novo specific documents
    elif submission_type == SubmissionType.DE_NOVO:
        checklist.extend(common_docs)
        checklist.extend([
            {
                "section": "Classification",
                "document": "Device Classification Recommendation",
                "cfr_reference": "21 CFR 860",
                "required": True,
                "description": "Recommended classification with risk analysis"
            },
            {
                "section": "Risk",
                "document": "Special Controls Proposal",
                "cfr_reference": "21 CFR 860.93",
                "required": True,
                "description": "Proposed special controls for device type"
            },
            {
                "section": "Testing",
                "document": "Performance Data",
                "cfr_reference": "21 CFR 860.7",
                "required": True,
                "description": "Safety and effectiveness performance data"
            }
        ])

    # HDE specific documents
    elif submission_type == SubmissionType.HDE:
        checklist.extend([
            {
                "section": "Administrative",
                "document": "HDE Application",
                "cfr_reference": "21 CFR 814.104",
                "required": True,
                "description": "HDE application for rare disease device"
            },
            {
                "section": "Clinical",
                "document": "Probable Benefit Demonstration",
                "cfr_reference": "21 CFR 814.104(b)(4)",
                "required": True,
                "description": "Evidence of probable benefit to patient population"
            },
            {
                "section": "Administrative",
                "document": "Patient Population Documentation",
                "cfr_reference": "21 CFR 814.3(n)",
                "required": True,
                "description": "Documentation of <8,000 patients/year in US"
            }
        ])

    return checklist


def calculate_timeline(
    submission_type: SubmissionType,
    device_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate FDA submission timeline with milestones.

    Args:
        submission_type: Type of FDA submission
        device_info: Device characteristics

    Returns:
        Dictionary containing timeline milestones and durations
    """
    today = datetime.now()
    milestones = []

    # Pre-submission activities (common to all)
    pre_submission_days = 60
    milestones.append({
        "phase": "Pre-Submission",
        "activity": "Document preparation and internal review",
        "duration_days": pre_submission_days,
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": (today + timedelta(days=pre_submission_days)).strftime("%Y-%m-%d")
    })

    current_date = today + timedelta(days=pre_submission_days)

    # Q-Sub meeting (if complex device)
    if device_info.get("complex_device", False) or submission_type == SubmissionType.PMA:
        q_sub_days = 75  # FDA responds within 75 days
        milestones.append({
            "phase": "Q-Sub",
            "activity": "Pre-submission meeting with FDA",
            "duration_days": q_sub_days,
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": (current_date + timedelta(days=q_sub_days)).strftime("%Y-%m-%d")
        })
        current_date += timedelta(days=q_sub_days)

    # FDA review timelines
    if submission_type == SubmissionType.SPECIAL_510K:
        fda_review_days = 30
    elif "510(k)" in submission_type.value:
        fda_review_days = 90
    elif submission_type == SubmissionType.PMA:
        fda_review_days = 180
    elif submission_type == SubmissionType.DE_NOVO:
        fda_review_days = 150
    elif submission_type == SubmissionType.HDE:
        fda_review_days = 75
    else:
        fda_review_days = 90

    milestones.append({
        "phase": "FDA Review",
        "activity": f"FDA {submission_type.value} review",
        "duration_days": fda_review_days,
        "start_date": current_date.strftime("%Y-%m-%d"),
        "end_date": (current_date + timedelta(days=fda_review_days)).strftime("%Y-%m-%d")
    })
    current_date += timedelta(days=fda_review_days)

    # Additional information request (buffer)
    rfi_buffer_days = 30
    milestones.append({
        "phase": "RFI Response",
        "activity": "Response to FDA additional information requests (if any)",
        "duration_days": rfi_buffer_days,
        "start_date": current_date.strftime("%Y-%m-%d"),
        "end_date": (current_date + timedelta(days=rfi_buffer_days)).strftime("%Y-%m-%d"),
        "note": "Buffer time - may not be needed"
    })
    current_date += timedelta(days=rfi_buffer_days)

    # Final decision
    milestones.append({
        "phase": "Decision",
        "activity": "FDA decision and clearance letter",
        "duration_days": 5,
        "start_date": current_date.strftime("%Y-%m-%d"),
        "end_date": (current_date + timedelta(days=5)).strftime("%Y-%m-%d")
    })

    total_days = sum(m["duration_days"] for m in milestones)

    return {
        "submission_type": submission_type.value,
        "estimated_total_days": total_days,
        "estimated_months": round(total_days / 30, 1),
        "projected_clearance_date": (today + timedelta(days=total_days)).strftime("%Y-%m-%d"),
        "milestones": milestones
    }


def generate_fda_correspondence_tracker() -> List[Dict[str, str]]:
    """
    Generate FDA correspondence tracking template.

    Returns:
        List of FDA interaction types with tracking fields
    """
    return [
        {
            "interaction_type": "Pre-Sub Meeting Request",
            "description": "Q-Sub meeting request for pre-submission consultation",
            "typical_timeline": "75 days for FDA response",
            "tracking_fields": "Request date, FDA response date, meeting date"
        },
        {
            "interaction_type": "Pre-Sub Meeting",
            "description": "Pre-submission meeting with FDA reviewers",
            "typical_timeline": "Scheduled after request approval",
            "tracking_fields": "Meeting date, attendees, minutes, action items"
        },
        {
            "interaction_type": "Submission Acceptance",
            "description": "FDA accepts submission for substantive review",
            "typical_timeline": "15 days after submission",
            "tracking_fields": "Submission date, acceptance date, 510(k) number"
        },
        {
            "interaction_type": "Additional Information Request",
            "description": "FDA requests additional information (AI/RFI)",
            "typical_timeline": "Day 60-90 of review",
            "tracking_fields": "Request date, deficiency list, response due date"
        },
        {
            "interaction_type": "Interactive Review",
            "description": "Phone/email communications during review",
            "typical_timeline": "Throughout review period",
            "tracking_fields": "Communication date, topic, FDA contact, outcome"
        },
        {
            "interaction_type": "Advisory Committee Meeting",
            "description": "FDA panel meeting for Class III devices",
            "typical_timeline": "PMA review process",
            "tracking_fields": "Meeting date, panel decision, recommendations"
        },
        {
            "interaction_type": "Clearance Letter",
            "description": "FDA issues clearance/approval letter",
            "typical_timeline": "End of review period",
            "tracking_fields": "Clearance date, 510(k) number, conditions"
        }
    ]


def process_device_info(device_info: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Main processing logic for FDA submission planning.

    Args:
        device_info: Device characteristics and submission strategy
        verbose: Include detailed information

    Returns:
        Dictionary containing complete submission plan
    """
    # Analyze device classification
    device_class, risk_level = analyze_device_classification(device_info)

    if verbose:
        print(f"Device classified as: {device_class.value} ({risk_level.value} risk)", file=sys.stderr)

    # Recommend submission pathway
    submission_type, reasoning = recommend_submission_pathway(device_class, risk_level, device_info)

    if verbose:
        print(f"Recommended pathway: {submission_type.value}", file=sys.stderr)

    # Generate document checklist
    document_checklist = generate_document_checklist(submission_type, device_info)

    # Calculate timeline
    timeline = calculate_timeline(submission_type, device_info)

    # Generate correspondence tracker
    correspondence_tracker = generate_fda_correspondence_tracker()

    # Compile results
    results = {
        "device_information": {
            "name": device_info.get("device_name", "Unknown"),
            "manufacturer": device_info.get("manufacturer", "Unknown"),
            "classification": device_class.value,
            "risk_level": risk_level.value
        },
        "submission_recommendation": {
            "submission_type": submission_type.value,
            "reasoning": reasoning,
            "regulatory_pathway": submission_type.value
        },
        "document_checklist": document_checklist,
        "timeline": timeline,
        "fda_correspondence_tracker": correspondence_tracker,
        "next_steps": [
            "Review document checklist and assign document owners",
            "Schedule internal kickoff meeting with cross-functional team",
            f"Initiate {'Q-Sub meeting request' if device_info.get('complex_device', False) else 'document preparation'}",
            "Establish document management system for submission materials",
            "Schedule regular submission progress reviews"
        ]
    }

    return results


def format_text_output(results: Dict[str, Any], verbose: bool = False) -> str:
    """
    Format results as human-readable text.

    Args:
        results: Processing results dictionary
        verbose: Include detailed information

    Returns:
        Formatted text output
    """
    output = "=" * 80 + "\n"
    output += "FDA SUBMISSION PLAN\n"
    output += "=" * 80 + "\n\n"

    # Device Information
    device_info = results["device_information"]
    output += "DEVICE INFORMATION\n"
    output += "-" * 80 + "\n"
    output += f"Device Name:     {device_info['name']}\n"
    output += f"Manufacturer:    {device_info['manufacturer']}\n"
    output += f"Classification:  {device_info['classification']}\n"
    output += f"Risk Level:      {device_info['risk_level']}\n\n"

    # Submission Recommendation
    submission = results["submission_recommendation"]
    output += "RECOMMENDED SUBMISSION PATHWAY\n"
    output += "-" * 80 + "\n"
    output += f"Submission Type: {submission['submission_type']}\n"
    output += f"Reasoning:       {submission['reasoning']}\n\n"

    # Timeline
    timeline = results["timeline"]
    output += "SUBMISSION TIMELINE\n"
    output += "-" * 80 + "\n"
    output += f"Estimated Duration:     {timeline['estimated_total_days']} days ({timeline['estimated_months']} months)\n"
    output += f"Projected Clearance:    {timeline['projected_clearance_date']}\n\n"
    output += "Key Milestones:\n"
    for milestone in timeline["milestones"]:
        output += f"  • {milestone['phase']}: {milestone['activity']}\n"
        output += f"    Duration: {milestone['duration_days']} days ({milestone['start_date']} to {milestone['end_date']})\n"
        if "note" in milestone:
            output += f"    Note: {milestone['note']}\n"
    output += "\n"

    # Document Checklist
    output += "DOCUMENT CHECKLIST\n"
    output += "-" * 80 + "\n"

    # Group by section
    sections = {}
    for doc in results["document_checklist"]:
        section = doc["section"]
        if section not in sections:
            sections[section] = []
        sections[section].append(doc)

    for section, docs in sections.items():
        output += f"\n{section}:\n"
        for doc in docs:
            req_marker = "[REQUIRED]" if doc["required"] else "[OPTIONAL]"
            output += f"  {req_marker} {doc['document']}\n"
            if verbose:
                output += f"    CFR: {doc['cfr_reference']}\n"
                output += f"    Description: {doc['description']}\n"

    output += "\n"

    # FDA Correspondence Tracking
    output += "FDA CORRESPONDENCE TRACKING\n"
    output += "-" * 80 + "\n"
    for interaction in results["fda_correspondence_tracker"]:
        output += f"  • {interaction['interaction_type']}\n"
        if verbose:
            output += f"    Description: {interaction['description']}\n"
            output += f"    Timeline: {interaction['typical_timeline']}\n"
            output += f"    Track: {interaction['tracking_fields']}\n"

    output += "\n"

    # Next Steps
    output += "NEXT STEPS\n"
    output += "-" * 80 + "\n"
    for i, step in enumerate(results["next_steps"], 1):
        output += f"  {i}. {step}\n"

    output += "\n" + "=" * 80 + "\n"

    return output


def format_json_output(results: Dict[str, Any]) -> str:
    """
    Format results as JSON with metadata.

    Args:
        results: Processing results dictionary

    Returns:
        JSON-formatted string
    """
    output = {
        "metadata": {
            "tool": "fda_submission_planner.py",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "description": "FDA Regulatory Submission Plan"
        },
        "results": results
    }

    return json.dumps(output, indent=2)


def format_csv_output(results: Dict[str, Any]) -> str:
    """
    Format document checklist as CSV.

    Args:
        results: Processing results dictionary

    Returns:
        CSV-formatted string
    """
    output = "Section,Document,Required,CFR_Reference,Description\n"

    for doc in results["document_checklist"]:
        required = "Yes" if doc["required"] else "No"
        # Escape commas in descriptions
        description = doc["description"].replace(",", ";")
        output += f'"{doc["section"]}","{doc["document"]}",{required},"{doc["cfr_reference"]}","{description}"\n'

    return output


def create_sample_file(output_file: str = "sample_device_info.json"):
    """
    Create a sample device information JSON file.

    Args:
        output_file: Output filename for sample JSON
    """
    sample_data = {
        "device_name": "CardioMonitor Pro X200",
        "manufacturer": "MedTech Innovations Inc.",
        "intended_use": "Continuous cardiac monitoring for hospitalized patients with suspected arrhythmias",
        "device_type": "Active monitoring device",
        "invasiveness": "non-invasive",
        "duration_of_contact": "short-term",
        "patient_contact": True,
        "sterile": False,
        "technological_characteristics": {
            "software_as_primary_function": True,
            "ai_ml_enabled": False,
            "connectivity": "wireless",
            "data_storage": "cloud-based"
        },
        "predicate_device": {
            "identified": True,
            "name": "CardioMonitor X100",
            "510k_number": "K123456",
            "manufacturer": "MedTech Innovations Inc."
        },
        "design_changes_from_predicate": "software enhancement",
        "novel_technology": False,
        "guidance_document_available": True,
        "complex_device": False,
        "rare_disease_indication": False,
        "annual_patient_population": 500000
    }

    with open(output_file, 'w') as f:
        json.dump(sample_data, f, indent=2)

    print(f"Sample device information file created: {output_file}")
    print(f"\nTo generate submission plan, run:")
    print(f"  python fda_submission_planner.py {output_file}")


def main():
    """
    Main entry point with standardized argument parsing.

    Parses command-line arguments, validates input, processes device information,
    and generates FDA submission plan in the specified format.
    """
    parser = argparse.ArgumentParser(
        description='Plan and track FDA regulatory submissions (510(k), PMA, De Novo) for medical devices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create sample input file
  %(prog)s sample

  # Generate submission plan (text output)
  %(prog)s device_info.json

  # Generate JSON output
  %(prog)s device_info.json --output json

  # Generate CSV checklist
  %(prog)s device_info.json -o csv --file submission_checklist.csv

  # Verbose output with detailed information
  %(prog)s device_info.json -v

  # Complete workflow
  %(prog)s device_info.json -o json -f submission_plan.json -v

FDA Submission Types Supported:
  - 510(k) Traditional/Special/Abbreviated
  - PMA (Premarket Approval)
  - De Novo Classification Request
  - HDE (Humanitarian Device Exemption)

For more information, see:
ra-qm-team/fda-consultant-specialist/SKILL.md
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='Device information JSON file or "sample" to create sample file'
    )

    # Optional arguments
    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format: text (default), json, or csv (checklist only)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Handle sample file creation
        if args.input.lower() == 'sample':
            output_filename = args.file if args.file else "sample_device_info.json"
            create_sample_file(output_filename)
            sys.exit(0)

        # Validate input file
        input_path = Path(args.input)

        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            print(f"Tip: Run 'python {Path(__file__).name} sample' to create a sample file", file=sys.stderr)
            sys.exit(1)

        if not input_path.is_file():
            print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Read and parse JSON input
        if args.verbose:
            print(f"Reading device information from: {args.input}", file=sys.stderr)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                device_info = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
            sys.exit(3)
        except UnicodeDecodeError:
            print(f"Error: Unable to read file as UTF-8 text: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Validate required fields
        required_fields = ["device_name", "intended_use"]
        missing_fields = [f for f in required_fields if f not in device_info]
        if missing_fields:
            print(f"Error: Missing required fields in JSON: {', '.join(missing_fields)}", file=sys.stderr)
            sys.exit(3)

        if args.verbose:
            print(f"Processing device: {device_info.get('device_name')}", file=sys.stderr)

        # Process device information
        results = process_device_info(device_info, verbose=args.verbose)

        # Format output
        if args.output == 'json':
            output = format_json_output(results)
        elif args.output == 'csv':
            output = format_csv_output(results)
        else:  # text (default)
            output = format_text_output(results, verbose=args.verbose)

        # Write output
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"\nSubmission plan written to: {args.file}", file=sys.stderr)
                else:
                    print(f"Submission plan saved to: {args.file}")

            except PermissionError:
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        # Success
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: Invalid input: {e}", file=sys.stderr)
        sys.exit(3)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
