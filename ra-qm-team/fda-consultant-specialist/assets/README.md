# FDA Submission Planner - Sample Device Files

This directory contains sample device information JSON files for testing the FDA submission planner script.

## Sample Files

### 1. sample_device_info.json
**Device Type:** 510(k) Traditional/Abbreviated
- Device: CardioMonitor Pro X200
- Classification: Class II
- Submission: 510(k) Abbreviated
- Scenario: Medical device with identified predicate and FDA guidance available

**Use Case:** Standard 510(k) submission for device with established predicate

### 2. sample_pma_device.json
**Device Type:** PMA (Premarket Approval)
- Device: CardioVascular Implantable Heart Monitor
- Classification: Class III
- Submission: PMA
- Scenario: Life-sustaining implantable device requiring clinical trials

**Use Case:** High-risk device requiring comprehensive clinical data and PMA submission

### 3. sample_de_novo_device.json
**Device Type:** De Novo Classification
- Device: AI-Powered Diabetic Retinopathy Screening System
- Classification: Class II
- Submission: De Novo
- Scenario: Novel AI/ML medical device with no predicate

**Use Case:** First-of-kind device establishing new classification and special controls

### 4. sample_hde_device.json
**Device Type:** HDE (Humanitarian Device Exemption)
- Device: Pediatric Ventricular Assist Device
- Classification: Class III
- Submission: HDE
- Scenario: Device for rare disease affecting <8,000 patients/year in US

**Use Case:** Orphan device for rare pediatric congenital heart defects

## Usage Examples

### Generate Submission Plan (Text Output)
```bash
python scripts/fda_submission_planner.py assets/sample_device_info.json
```

### Generate JSON Output
```bash
python scripts/fda_submission_planner.py assets/sample_pma_device.json --output json
```

### Generate CSV Checklist
```bash
python scripts/fda_submission_planner.py assets/sample_de_novo_device.json -o csv --file checklist.csv
```

### Verbose Mode
```bash
python scripts/fda_submission_planner.py assets/sample_hde_device.json -v
```

### Complete Workflow
```bash
python scripts/fda_submission_planner.py assets/sample_device_info.json -o json -f submission_plan.json -v
```

## JSON Schema

### Required Fields
- `device_name` (string): Device name
- `intended_use` (string): Clinical indications and patient population

### Recommended Fields
- `manufacturer` (string)
- `device_type` (string)
- `invasiveness` (string): "invasive" | "non-invasive"
- `duration_of_contact` (string): "short-term" | "long-term" | "permanent"
- `patient_contact` (boolean)
- `sterile` (boolean)
- `technological_characteristics` (object)
  - `software_as_primary_function` (boolean)
  - `ai_ml_enabled` (boolean)
  - `connectivity` (string)
  - `data_storage` (string)
- `predicate_device` (object)
  - `identified` (boolean)
  - `name` (string)
  - `510k_number` (string)
- `design_changes_from_predicate` (string)
- `novel_technology` (boolean)
- `guidance_document_available` (boolean)
- `complex_device` (boolean)
- `rare_disease_indication` (boolean)
- `annual_patient_population` (number)

## Creating Custom Device Files

1. Copy one of the sample files as a template
2. Modify device characteristics to match your device
3. Run the planner to generate submission plan
4. Review recommendations and adjust device information as needed

## Submission Type Decision Logic

The planner uses the following logic to recommend submission pathways:

1. **HDE**: Rare disease with <8,000 patients/year in US
2. **PMA**: Class III devices with novel technology or no predicate
3. **De Novo**: Novel Class I/II devices with no predicate
4. **Special 510(k)**: Manufacturing changes only to predicate device
5. **Abbreviated 510(k)**: FDA guidance document available
6. **Traditional 510(k)**: Standard pathway with predicate comparison

## Support

For questions or issues with the FDA submission planner, see:
- Main documentation: `ra-qm-team/fda-consultant-specialist/SKILL.md`
- CLI standards: `standards/cli-standards.md`
