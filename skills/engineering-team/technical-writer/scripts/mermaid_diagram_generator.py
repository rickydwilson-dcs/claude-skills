#!/usr/bin/env python3
"""
Mermaid Diagram Generator - Generate technical and business documentation diagrams

Creates Mermaid diagrams for technical documentation and business analysis including:
- Technical: architecture, flowcharts, sequence, class, ERD, state machines
- Business Analysis: swimlanes, process flows, BPMN-style, decision trees, journey maps

COMPLEMENTARY DESIGN:
- business-analyst-toolkit/stakeholder_mapper.py: Stakeholder relationship diagrams (people/orgs)
- technical-writer/mermaid_diagram_generator.py: All other diagram types
  - Technical: architecture, class, ERD, sequence, state
  - Business: swimlanes, process flows, journey maps, Gantt, quadrant

Usage:
    # Technical diagrams
    python mermaid_diagram_generator.py --type flowchart --input process.json
    python mermaid_diagram_generator.py --type sequence --input api-flow.yaml
    python mermaid_diagram_generator.py --type class --scan src/models/
    python mermaid_diagram_generator.py --type erd --input schema.json
    python mermaid_diagram_generator.py --type state --input workflow.json
    python mermaid_diagram_generator.py --type architecture --input system.json

    # Business analysis diagrams
    python mermaid_diagram_generator.py --type swimlane --input cross-func-process.json
    python mermaid_diagram_generator.py --type journey --input customer-journey.json
    python mermaid_diagram_generator.py --type gantt --input project-timeline.json
    python mermaid_diagram_generator.py --type quadrant --input prioritization.json

Exit Codes:
    0 - Success
    1 - Validation error
    2 - Parse error
    3 - Generation error

Author: Claude Code
Version: 1.1.0
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_GENERATION_ERROR = 3

# Diagram type configurations
DIAGRAM_TYPES = {
    # Technical diagrams
    'flowchart': {
        'prefix': 'flowchart',
        'description': 'Process flows, decision trees, workflows',
        'directions': ['TD', 'TB', 'BT', 'LR', 'RL'],
        'category': 'technical'
    },
    'sequence': {
        'prefix': 'sequenceDiagram',
        'description': 'API calls, service interactions, message flows',
        'category': 'technical'
    },
    'class': {
        'prefix': 'classDiagram',
        'description': 'Object models, inheritance hierarchies, interfaces',
        'category': 'technical'
    },
    'erd': {
        'prefix': 'erDiagram',
        'description': 'Database schemas, entity relationships',
        'category': 'technical'
    },
    'state': {
        'prefix': 'stateDiagram-v2',
        'description': 'State machines, workflow states, lifecycles',
        'category': 'technical'
    },
    'architecture': {
        'prefix': 'flowchart',
        'description': 'System architecture, component diagrams, C4 models',
        'category': 'technical'
    },
    # Business analysis diagrams
    'swimlane': {
        'prefix': 'flowchart',
        'description': 'Cross-functional process flows with role/department lanes',
        'directions': ['TD', 'TB', 'LR'],
        'category': 'business'
    },
    'journey': {
        'prefix': 'journey',
        'description': 'Customer/user journey maps with touchpoints and emotions',
        'category': 'business'
    },
    'gantt': {
        'prefix': 'gantt',
        'description': 'Project timelines, milestones, task dependencies',
        'category': 'business'
    },
    'quadrant': {
        'prefix': 'quadrantChart',
        'description': 'Priority matrices, risk assessments, effort/impact analysis',
        'category': 'business'
    },
    'timeline': {
        'prefix': 'timeline',
        'description': 'Event timelines, roadmaps, milestones',
        'category': 'business'
    },
    'mindmap': {
        'prefix': 'mindmap',
        'description': 'Brainstorming, idea organization, hierarchical concepts',
        'category': 'business'
    }
}


class MermaidDiagramGenerator:
    """Generate Mermaid diagrams for technical documentation"""

    def __init__(self, verbose: bool = False):
        """Initialize generator with configuration"""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("MermaidDiagramGenerator initialized")
        self.verbose = verbose

    def log(self, message: str) -> None:
        """Print verbose logging message"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    # =========================================================================
    # INPUT PARSING
    # =========================================================================

    def parse_json_input(self, file_path: Path) -> Dict[str, Any]:
        """Parse JSON input file for diagram data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def parse_yaml_input(self, file_path: Path) -> Dict[str, Any]:
        """Parse YAML input file for diagram data (simple parser)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._simple_yaml_parse(content)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")

    def _simple_yaml_parse(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for basic structures (no dependencies)"""
        result: Dict[str, Any] = {}
        current_key = None
        current_list: List[Any] = []
        in_list = False
        indent_level = 0

        for line in content.split('\n'):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Calculate indentation
            line_indent = len(line) - len(line.lstrip())

            # List item
            if stripped.startswith('- '):
                item = stripped[2:].strip()
                if ':' in item and not item.startswith('"'):
                    # Nested object in list
                    key, val = item.split(':', 1)
                    current_list.append({key.strip(): val.strip().strip('"\'')})
                else:
                    current_list.append(item.strip('"\''))
                in_list = True
            # Key-value pair
            elif ':' in stripped:
                if in_list and current_key:
                    result[current_key] = current_list
                    current_list = []
                    in_list = False

                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip().strip('"\'')

                if value:
                    result[key] = value
                else:
                    current_key = key
                    in_list = False

        # Handle trailing list
        if in_list and current_key:
            result[current_key] = current_list

        return result

    def load_input(self, file_path: Path) -> Dict[str, Any]:
        """Load input from JSON or YAML file"""
        suffix = file_path.suffix.lower()

        if suffix == '.json':
            return self.parse_json_input(file_path)
        elif suffix in ['.yaml', '.yml']:
            return self.parse_yaml_input(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .json or .yaml")

    # =========================================================================
    # FLOWCHART GENERATION
    # =========================================================================

    def generate_flowchart(self, data: Dict[str, Any], direction: str = 'TD') -> str:
        """
        Generate flowchart diagram from process definition

        Expected input format:
        {
            "title": "Process Name",
            "direction": "TD",
            "nodes": [
                {"id": "A", "label": "Start", "shape": "circle"},
                {"id": "B", "label": "Process Step", "shape": "rect"},
                {"id": "C", "label": "Decision?", "shape": "diamond"},
                {"id": "D", "label": "End", "shape": "circle"}
            ],
            "edges": [
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "C", "to": "D", "label": "Yes"},
                {"from": "C", "to": "B", "label": "No"}
            ],
            "styles": [
                {"id": "A", "fill": "#90EE90"},
                {"id": "D", "fill": "#FFB6C1"}
            ]
        }
        """
        self.log("Generating flowchart diagram")

        direction = data.get('direction', direction).upper()
        if direction not in DIAGRAM_TYPES['flowchart']['directions']:
            direction = 'TD'

        lines = [f"flowchart {direction}"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")

        # Generate nodes
        nodes = data.get('nodes', [])
        for node in nodes:
            node_id = self._sanitize_id(node.get('id', ''))
            label = node.get('label', node_id)
            shape = node.get('shape', 'rect')

            node_def = self._format_node(node_id, label, shape)
            lines.append(f"    {node_def}")

        # Generate edges
        edges = data.get('edges', [])
        for edge in edges:
            from_id = self._sanitize_id(edge.get('from', ''))
            to_id = self._sanitize_id(edge.get('to', ''))
            label = edge.get('label', '')
            edge_type = edge.get('type', 'arrow')

            edge_def = self._format_edge(from_id, to_id, label, edge_type)
            lines.append(f"    {edge_def}")

        # Generate styles
        styles = data.get('styles', [])
        if styles:
            lines.append("")
            for style in styles:
                style_id = self._sanitize_id(style.get('id', ''))
                fill = style.get('fill', '#fff')
                stroke = style.get('stroke', '#333')
                lines.append(f"    style {style_id} fill:{fill},stroke:{stroke}")

        # Generate subgraphs
        subgraphs = data.get('subgraphs', [])
        for subgraph in subgraphs:
            sg_id = self._sanitize_id(subgraph.get('id', ''))
            sg_label = subgraph.get('label', sg_id)
            sg_nodes = subgraph.get('nodes', [])

            lines.append(f"    subgraph {sg_id}[{sg_label}]")
            for node_id in sg_nodes:
                lines.append(f"        {self._sanitize_id(node_id)}")
            lines.append("    end")

        return '\n'.join(lines)

    def _format_node(self, node_id: str, label: str, shape: str) -> str:
        """Format node with appropriate shape syntax"""
        shapes = {
            'rect': f'{node_id}["{label}"]',
            'rounded': f'{node_id}("{label}")',
            'circle': f'{node_id}(("{label}"))',
            'diamond': f'{node_id}{{"{label}"}}',
            'hexagon': f'{node_id}{{{{"{label}"}}}}',
            'parallelogram': f'{node_id}[/"{label}"/]',
            'trapezoid': f'{node_id}[/"{label}"\\]',
            'database': f'{node_id}[("{label}")]',
            'stadium': f'{node_id}(["{label}"])',
            'subroutine': f'{node_id}[["{label}"]]',
            'cylinder': f'{node_id}[(("{label}"))]',
        }
        return shapes.get(shape, shapes['rect'])

    def _format_edge(self, from_id: str, to_id: str, label: str, edge_type: str) -> str:
        """Format edge with appropriate arrow syntax"""
        if label:
            arrows = {
                'arrow': f'{from_id} -->|{label}| {to_id}',
                'dotted': f'{from_id} -.->|{label}| {to_id}',
                'thick': f'{from_id} ==>|{label}| {to_id}',
                'open': f'{from_id} ---|{label}| {to_id}',
            }
        else:
            arrows = {
                'arrow': f'{from_id} --> {to_id}',
                'dotted': f'{from_id} -.-> {to_id}',
                'thick': f'{from_id} ==> {to_id}',
                'open': f'{from_id} --- {to_id}',
            }
        return arrows.get(edge_type, arrows['arrow'])

    # =========================================================================
    # SEQUENCE DIAGRAM GENERATION
    # =========================================================================

    def generate_sequence(self, data: Dict[str, Any]) -> str:
        """
        Generate sequence diagram from interaction definition

        Expected input format:
        {
            "title": "API Authentication Flow",
            "participants": [
                {"id": "client", "label": "Client App", "type": "actor"},
                {"id": "api", "label": "API Gateway"},
                {"id": "auth", "label": "Auth Service"},
                {"id": "db", "label": "Database", "type": "database"}
            ],
            "messages": [
                {"from": "client", "to": "api", "label": "POST /login", "type": "sync"},
                {"from": "api", "to": "auth", "label": "validateCredentials()", "type": "sync"},
                {"from": "auth", "to": "db", "label": "SELECT user", "type": "sync"},
                {"from": "db", "to": "auth", "label": "User data", "type": "reply"},
                {"from": "auth", "to": "api", "label": "JWT token", "type": "reply"},
                {"from": "api", "to": "client", "label": "200 OK + token", "type": "reply"}
            ],
            "notes": [
                {"over": ["api", "auth"], "text": "Internal network"},
                {"right_of": "client", "text": "Mobile or Web"}
            ],
            "loops": [
                {"label": "Retry 3 times", "messages": [0, 1]}
            ],
            "alt": [
                {"condition": "Valid credentials", "messages": [3, 4, 5]},
                {"condition": "Invalid credentials", "messages": []}
            ]
        }
        """
        self.log("Generating sequence diagram")

        lines = ["sequenceDiagram"]

        # Title
        if 'title' in data:
            lines.append(f"    title: {data['title']}")

        # Participants
        participants = data.get('participants', [])
        for p in participants:
            p_id = self._sanitize_id(p.get('id', ''))
            p_label = p.get('label', p_id)
            p_type = p.get('type', 'participant')

            if p_type == 'actor':
                lines.append(f"    actor {p_id} as {p_label}")
            elif p_type == 'database':
                lines.append(f"    participant {p_id} as {p_label}")
            else:
                lines.append(f"    participant {p_id} as {p_label}")

        lines.append("")

        # Notes (placed before messages)
        notes = data.get('notes', [])
        for note in notes:
            text = note.get('text', '')
            if 'over' in note:
                over = ', '.join(note['over'])
                lines.append(f"    note over {over}: {text}")
            elif 'right_of' in note:
                lines.append(f"    note right of {note['right_of']}: {text}")
            elif 'left_of' in note:
                lines.append(f"    note left of {note['left_of']}: {text}")

        # Messages
        messages = data.get('messages', [])
        for msg in messages:
            from_id = self._sanitize_id(msg.get('from', ''))
            to_id = self._sanitize_id(msg.get('to', ''))
            label = msg.get('label', '')
            msg_type = msg.get('type', 'sync')

            arrow = self._get_sequence_arrow(msg_type)
            lines.append(f"    {from_id}{arrow}{to_id}: {label}")

            # Activation
            if msg.get('activate'):
                lines.append(f"    activate {to_id}")
            if msg.get('deactivate'):
                lines.append(f"    deactivate {msg['deactivate']}")

        # Alt/Opt/Loop blocks (simplified)
        alt_blocks = data.get('alt', [])
        if alt_blocks:
            for i, alt in enumerate(alt_blocks):
                condition = alt.get('condition', 'Condition')
                if i == 0:
                    lines.append(f"    alt {condition}")
                else:
                    lines.append(f"    else {condition}")
            if alt_blocks:
                lines.append("    end")

        return '\n'.join(lines)

    def _get_sequence_arrow(self, msg_type: str) -> str:
        """Get sequence diagram arrow for message type"""
        arrows = {
            'sync': '->>',
            'async': '-))',
            'reply': '-->>',
            'dotted': '-->>',
            'create': '->>+',
            'destroy': '->>-',
        }
        return arrows.get(msg_type, '->>')

    # =========================================================================
    # CLASS DIAGRAM GENERATION
    # =========================================================================

    def generate_class(self, data: Dict[str, Any]) -> str:
        """
        Generate class diagram from object model definition

        Expected input format:
        {
            "title": "User Domain Model",
            "classes": [
                {
                    "name": "User",
                    "attributes": [
                        {"name": "id", "type": "string", "visibility": "private"},
                        {"name": "email", "type": "string", "visibility": "public"},
                        {"name": "passwordHash", "type": "string", "visibility": "private"}
                    ],
                    "methods": [
                        {"name": "authenticate", "params": "password: string", "return": "boolean", "visibility": "public"},
                        {"name": "updateEmail", "params": "email: string", "return": "void", "visibility": "public"}
                    ],
                    "stereotype": "entity"
                },
                {
                    "name": "UserRepository",
                    "attributes": [],
                    "methods": [
                        {"name": "findById", "params": "id: string", "return": "User", "visibility": "public"},
                        {"name": "save", "params": "user: User", "return": "void", "visibility": "public"}
                    ],
                    "stereotype": "interface"
                }
            ],
            "relationships": [
                {"from": "UserService", "to": "UserRepository", "type": "dependency", "label": "uses"},
                {"from": "User", "to": "Address", "type": "composition", "cardinality": "1..*"},
                {"from": "User", "to": "Profile", "type": "aggregation", "cardinality": "1"},
                {"from": "Admin", "to": "User", "type": "inheritance"}
            ]
        }
        """
        self.log("Generating class diagram")

        lines = ["classDiagram"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")

        # Classes
        classes = data.get('classes', [])
        for cls in classes:
            cls_name = self._sanitize_id(cls.get('name', ''))
            stereotype = cls.get('stereotype', '')

            # Class definition
            lines.append(f"    class {cls_name} {{")

            # Stereotype annotation
            if stereotype:
                lines.append(f"        <<{stereotype}>>")

            # Attributes
            for attr in cls.get('attributes', []):
                visibility = self._get_visibility_symbol(attr.get('visibility', 'public'))
                attr_name = attr.get('name', '')
                attr_type = attr.get('type', '')
                lines.append(f"        {visibility}{attr_type} {attr_name}")

            # Methods
            for method in cls.get('methods', []):
                visibility = self._get_visibility_symbol(method.get('visibility', 'public'))
                method_name = method.get('name', '')
                params = method.get('params', '')
                return_type = method.get('return', 'void')
                lines.append(f"        {visibility}{method_name}({params}) {return_type}")

            lines.append("    }")
            lines.append("")

        # Relationships
        relationships = data.get('relationships', [])
        for rel in relationships:
            from_cls = self._sanitize_id(rel.get('from', ''))
            to_cls = self._sanitize_id(rel.get('to', ''))
            rel_type = rel.get('type', 'association')
            label = rel.get('label', '')
            cardinality = rel.get('cardinality', '')

            arrow = self._get_class_relationship_arrow(rel_type)
            rel_line = f"    {from_cls} {arrow} {to_cls}"

            if label:
                rel_line += f" : {label}"
            if cardinality:
                rel_line = rel_line.replace(arrow, f'"{cardinality}" {arrow}')

            lines.append(rel_line)

        return '\n'.join(lines)

    def _get_visibility_symbol(self, visibility: str) -> str:
        """Get UML visibility symbol"""
        symbols = {
            'public': '+',
            'private': '-',
            'protected': '#',
            'package': '~',
        }
        return symbols.get(visibility, '+')

    def _get_class_relationship_arrow(self, rel_type: str) -> str:
        """Get class diagram relationship arrow"""
        arrows = {
            'inheritance': '<|--',
            'composition': '*--',
            'aggregation': 'o--',
            'association': '-->',
            'dependency': '..>',
            'realization': '<|..',
        }
        return arrows.get(rel_type, '-->')

    # =========================================================================
    # ERD GENERATION
    # =========================================================================

    def generate_erd(self, data: Dict[str, Any]) -> str:
        """
        Generate entity-relationship diagram from schema definition

        Expected input format:
        {
            "title": "E-Commerce Database Schema",
            "entities": [
                {
                    "name": "users",
                    "attributes": [
                        {"name": "id", "type": "uuid", "key": "PK"},
                        {"name": "email", "type": "varchar(255)", "constraints": "UK, NN"},
                        {"name": "created_at", "type": "timestamp", "constraints": "NN"}
                    ]
                },
                {
                    "name": "orders",
                    "attributes": [
                        {"name": "id", "type": "uuid", "key": "PK"},
                        {"name": "user_id", "type": "uuid", "key": "FK"},
                        {"name": "total", "type": "decimal(10,2)", "constraints": "NN"},
                        {"name": "status", "type": "varchar(50)", "constraints": "NN"}
                    ]
                }
            ],
            "relationships": [
                {"from": "users", "to": "orders", "type": "one-to-many", "label": "places"},
                {"from": "orders", "to": "order_items", "type": "one-to-many", "label": "contains"},
                {"from": "products", "to": "order_items", "type": "one-to-many", "label": "appears in"}
            ]
        }
        """
        self.log("Generating ERD diagram")

        lines = ["erDiagram"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")

        # Entities with attributes
        entities = data.get('entities', [])
        for entity in entities:
            entity_name = self._sanitize_id(entity.get('name', ''))
            lines.append(f"    {entity_name} {{")

            for attr in entity.get('attributes', []):
                attr_type = attr.get('type', 'string')
                attr_name = attr.get('name', '')
                key = attr.get('key', '')
                constraints = attr.get('constraints', '')

                # Format: type name "comment"
                comment_parts = []
                if key:
                    comment_parts.append(key)
                if constraints:
                    comment_parts.append(constraints)

                if comment_parts:
                    lines.append(f'        {attr_type} {attr_name} "{", ".join(comment_parts)}"')
                else:
                    lines.append(f"        {attr_type} {attr_name}")

            lines.append("    }")
            lines.append("")

        # Relationships
        relationships = data.get('relationships', [])
        for rel in relationships:
            from_entity = self._sanitize_id(rel.get('from', ''))
            to_entity = self._sanitize_id(rel.get('to', ''))
            rel_type = rel.get('type', 'one-to-many')
            label = rel.get('label', 'has')

            cardinality = self._get_erd_cardinality(rel_type)
            lines.append(f'    {from_entity} {cardinality} {to_entity} : "{label}"')

        return '\n'.join(lines)

    def _get_erd_cardinality(self, rel_type: str) -> str:
        """Get ERD cardinality notation"""
        cardinalities = {
            'one-to-one': '||--||',
            'one-to-many': '||--o{',
            'many-to-one': '}o--||',
            'many-to-many': '}o--o{',
            'zero-or-one': '||--o|',
            'zero-or-many': '||--o{',
        }
        return cardinalities.get(rel_type, '||--o{')

    # =========================================================================
    # STATE DIAGRAM GENERATION
    # =========================================================================

    def generate_state(self, data: Dict[str, Any]) -> str:
        """
        Generate state diagram from state machine definition

        Expected input format:
        {
            "title": "Order Lifecycle",
            "states": [
                {"id": "pending", "label": "Pending", "description": "Order created"},
                {"id": "processing", "label": "Processing", "description": "Being prepared"},
                {"id": "shipped", "label": "Shipped", "description": "In transit"},
                {"id": "delivered", "label": "Delivered", "type": "final"},
                {"id": "cancelled", "label": "Cancelled", "type": "final"}
            ],
            "transitions": [
                {"from": "[*]", "to": "pending", "label": "create order"},
                {"from": "pending", "to": "processing", "label": "payment received"},
                {"from": "pending", "to": "cancelled", "label": "cancel"},
                {"from": "processing", "to": "shipped", "label": "dispatch"},
                {"from": "shipped", "to": "delivered", "label": "confirm delivery"},
                {"from": "delivered", "to": "[*]"}
            ],
            "composite": [
                {
                    "id": "processing",
                    "states": [
                        {"id": "picking", "label": "Picking"},
                        {"id": "packing", "label": "Packing"}
                    ],
                    "transitions": [
                        {"from": "[*]", "to": "picking"},
                        {"from": "picking", "to": "packing"},
                        {"from": "packing", "to": "[*]"}
                    ]
                }
            ],
            "notes": [
                {"state": "cancelled", "text": "Refund processed"}
            ]
        }
        """
        self.log("Generating state diagram")

        lines = ["stateDiagram-v2"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")

        # State definitions with descriptions
        states = data.get('states', [])
        for state in states:
            state_id = self._sanitize_id(state.get('id', ''))
            label = state.get('label', state_id)
            description = state.get('description', '')
            state_type = state.get('type', '')

            if state_id != '[*]':
                if description:
                    lines.append(f"    {state_id} : {label}")
                    lines.append(f"    {state_id} : {description}")
                else:
                    lines.append(f"    {state_id} : {label}")

        lines.append("")

        # Transitions
        transitions = data.get('transitions', [])
        for trans in transitions:
            from_state = trans.get('from', '')
            to_state = trans.get('to', '')
            label = trans.get('label', '')

            # Handle special start/end states
            from_id = from_state if from_state == '[*]' else self._sanitize_id(from_state)
            to_id = to_state if to_state == '[*]' else self._sanitize_id(to_state)

            if label:
                lines.append(f"    {from_id} --> {to_id} : {label}")
            else:
                lines.append(f"    {from_id} --> {to_id}")

        # Composite states
        composite = data.get('composite', [])
        for comp in composite:
            comp_id = self._sanitize_id(comp.get('id', ''))
            lines.append(f"    state {comp_id} {{")

            for sub_state in comp.get('states', []):
                sub_id = self._sanitize_id(sub_state.get('id', ''))
                sub_label = sub_state.get('label', sub_id)
                lines.append(f"        {sub_id} : {sub_label}")

            for sub_trans in comp.get('transitions', []):
                from_s = sub_trans.get('from', '')
                to_s = sub_trans.get('to', '')
                label = sub_trans.get('label', '')
                from_id = from_s if from_s == '[*]' else self._sanitize_id(from_s)
                to_id = to_s if to_s == '[*]' else self._sanitize_id(to_s)

                if label:
                    lines.append(f"        {from_id} --> {to_id} : {label}")
                else:
                    lines.append(f"        {from_id} --> {to_id}")

            lines.append("    }")

        # Notes
        notes = data.get('notes', [])
        for note in notes:
            state = self._sanitize_id(note.get('state', ''))
            text = note.get('text', '')
            lines.append(f"    note right of {state} : {text}")

        return '\n'.join(lines)

    # =========================================================================
    # ARCHITECTURE DIAGRAM GENERATION
    # =========================================================================

    def generate_architecture(self, data: Dict[str, Any]) -> str:
        """
        Generate architecture diagram from system definition

        Expected input format:
        {
            "title": "Microservices Architecture",
            "style": "c4",
            "layers": [
                {
                    "name": "Presentation",
                    "components": [
                        {"id": "web", "label": "Web App", "type": "webapp"},
                        {"id": "mobile", "label": "Mobile App", "type": "mobileapp"}
                    ]
                },
                {
                    "name": "API Gateway",
                    "components": [
                        {"id": "gateway", "label": "API Gateway", "type": "service"}
                    ]
                },
                {
                    "name": "Services",
                    "components": [
                        {"id": "user_svc", "label": "User Service", "type": "service"},
                        {"id": "order_svc", "label": "Order Service", "type": "service"},
                        {"id": "payment_svc", "label": "Payment Service", "type": "service"}
                    ]
                },
                {
                    "name": "Data",
                    "components": [
                        {"id": "user_db", "label": "User DB", "type": "database"},
                        {"id": "order_db", "label": "Order DB", "type": "database"},
                        {"id": "cache", "label": "Redis Cache", "type": "cache"}
                    ]
                }
            ],
            "connections": [
                {"from": "web", "to": "gateway", "label": "HTTPS"},
                {"from": "mobile", "to": "gateway", "label": "HTTPS"},
                {"from": "gateway", "to": "user_svc", "label": "gRPC"},
                {"from": "gateway", "to": "order_svc", "label": "gRPC"},
                {"from": "user_svc", "to": "user_db"},
                {"from": "order_svc", "to": "order_db"},
                {"from": "order_svc", "to": "cache"}
            ],
            "external": [
                {"id": "stripe", "label": "Stripe API", "type": "external"},
                {"connection": {"from": "payment_svc", "to": "stripe", "label": "REST"}}
            ]
        }
        """
        self.log("Generating architecture diagram")

        lines = ["flowchart TB"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")

        # Component type styles
        component_styles = {
            'webapp': {'shape': 'rect', 'fill': '#4A90D9'},
            'mobileapp': {'shape': 'rect', 'fill': '#4A90D9'},
            'service': {'shape': 'rounded', 'fill': '#48BB78'},
            'database': {'shape': 'cylinder', 'fill': '#ED8936'},
            'cache': {'shape': 'stadium', 'fill': '#9F7AEA'},
            'queue': {'shape': 'parallelogram', 'fill': '#F6AD55'},
            'external': {'shape': 'hexagon', 'fill': '#FC8181'},
            'user': {'shape': 'circle', 'fill': '#63B3ED'},
        }

        # Track all nodes for styling
        all_nodes: List[Tuple[str, str]] = []

        # Layers as subgraphs
        layers = data.get('layers', [])
        for layer in layers:
            layer_name = layer.get('name', 'Layer')
            layer_id = self._sanitize_id(layer_name)

            lines.append(f"    subgraph {layer_id}[{layer_name}]")

            for comp in layer.get('components', []):
                comp_id = self._sanitize_id(comp.get('id', ''))
                comp_label = comp.get('label', comp_id)
                comp_type = comp.get('type', 'service')

                style = component_styles.get(comp_type, component_styles['service'])
                node_def = self._format_node(comp_id, comp_label, style['shape'])
                lines.append(f"        {node_def}")
                all_nodes.append((comp_id, comp_type))

            lines.append("    end")
            lines.append("")

        # External systems
        external = data.get('external', [])
        if external:
            lines.append("    subgraph External[External Systems]")
            for ext in external:
                if 'id' in ext:
                    ext_id = self._sanitize_id(ext.get('id', ''))
                    ext_label = ext.get('label', ext_id)
                    ext_type = ext.get('type', 'external')

                    style = component_styles.get(ext_type, component_styles['external'])
                    node_def = self._format_node(ext_id, ext_label, style['shape'])
                    lines.append(f"        {node_def}")
                    all_nodes.append((ext_id, ext_type))
            lines.append("    end")
            lines.append("")

        # Connections
        connections = data.get('connections', [])
        for conn in connections:
            from_id = self._sanitize_id(conn.get('from', ''))
            to_id = self._sanitize_id(conn.get('to', ''))
            label = conn.get('label', '')
            conn_type = conn.get('type', 'arrow')

            edge_def = self._format_edge(from_id, to_id, label, conn_type)
            lines.append(f"    {edge_def}")

        # External connections
        for ext in external:
            if 'connection' in ext:
                conn = ext['connection']
                from_id = self._sanitize_id(conn.get('from', ''))
                to_id = self._sanitize_id(conn.get('to', ''))
                label = conn.get('label', '')

                edge_def = self._format_edge(from_id, to_id, label, 'dotted')
                lines.append(f"    {edge_def}")

        # Apply styles
        lines.append("")
        for node_id, node_type in all_nodes:
            style = component_styles.get(node_type, component_styles['service'])
            lines.append(f"    style {node_id} fill:{style['fill']},stroke:#333,color:#fff")

        return '\n'.join(lines)

    # =========================================================================
    # CODE SCANNING
    # =========================================================================

    def scan_directory_for_classes(self, directory: Path) -> Dict[str, Any]:
        """
        Scan Python/TypeScript files for class definitions

        Returns data structure suitable for generate_class()
        """
        self.log(f"Scanning directory: {directory}")

        classes = []
        relationships = []

        # Scan Python files
        for py_file in directory.rglob('*.py'):
            self.log(f"Scanning: {py_file}")
            file_classes = self._extract_python_classes(py_file)
            classes.extend(file_classes)

        # Scan TypeScript files
        for ts_file in directory.rglob('*.ts'):
            if not ts_file.name.endswith('.d.ts'):
                self.log(f"Scanning: {ts_file}")
                file_classes = self._extract_typescript_classes(ts_file)
                classes.extend(file_classes)

        # Infer relationships from type hints and imports
        relationships = self._infer_relationships(classes)

        return {
            'title': f'Class Diagram - {directory.name}',
            'classes': classes,
            'relationships': relationships
        }

    def _extract_python_classes(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract class definitions from Python file"""
        classes = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return []

        # Simple regex-based extraction (no AST for zero dependencies)
        class_pattern = r'^class\s+(\w+)(?:\((.*?)\))?:'
        method_pattern = r'^\s{4}def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*(\w+))?:'
        attr_pattern = r'^\s{4}self\.(\w+)\s*(?::\s*(\w+))?\s*='

        current_class = None
        current_attrs = []
        current_methods = []

        for line in content.split('\n'):
            class_match = re.match(class_pattern, line)
            if class_match:
                # Save previous class
                if current_class:
                    classes.append({
                        'name': current_class['name'],
                        'attributes': current_attrs,
                        'methods': current_methods,
                        'inherits': current_class.get('inherits', [])
                    })

                # Start new class
                class_name = class_match.group(1)
                parents = class_match.group(2) or ''
                inherits = [p.strip() for p in parents.split(',') if p.strip() and p.strip() != 'object']

                current_class = {'name': class_name, 'inherits': inherits}
                current_attrs = []
                current_methods = []
                continue

            if current_class:
                method_match = re.match(method_pattern, line)
                if method_match:
                    method_name = method_match.group(1)
                    params = method_match.group(2) or ''
                    return_type = method_match.group(3) or 'None'

                    # Skip dunder methods
                    if not method_name.startswith('__'):
                        visibility = 'private' if method_name.startswith('_') else 'public'
                        current_methods.append({
                            'name': method_name,
                            'params': params.replace('self, ', '').replace('self', ''),
                            'return': return_type,
                            'visibility': visibility
                        })
                    continue

                attr_match = re.match(attr_pattern, line)
                if attr_match:
                    attr_name = attr_match.group(1)
                    attr_type = attr_match.group(2) or 'Any'

                    if not attr_name.startswith('_'):
                        visibility = 'public'
                    else:
                        visibility = 'private'

                    # Avoid duplicates
                    if not any(a['name'] == attr_name for a in current_attrs):
                        current_attrs.append({
                            'name': attr_name,
                            'type': attr_type,
                            'visibility': visibility
                        })

        # Save last class
        if current_class:
            classes.append({
                'name': current_class['name'],
                'attributes': current_attrs,
                'methods': current_methods,
                'inherits': current_class.get('inherits', [])
            })

        return classes

    def _extract_typescript_classes(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract class/interface definitions from TypeScript file"""
        classes = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return []

        # Simple regex for TypeScript classes and interfaces
        class_pattern = r'(?:export\s+)?(?:class|interface)\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?'

        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            extends = match.group(2)
            implements = match.group(3)

            inherits = []
            if extends:
                inherits.append(extends)
            if implements:
                inherits.extend([i.strip() for i in implements.split(',')])

            classes.append({
                'name': class_name,
                'attributes': [],  # Would need more complex parsing
                'methods': [],
                'inherits': inherits
            })

        return classes

    def _infer_relationships(self, classes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Infer relationships from inheritance and type references"""
        relationships = []
        class_names = {c['name'] for c in classes}

        for cls in classes:
            # Inheritance relationships
            for parent in cls.get('inherits', []):
                if parent in class_names:
                    relationships.append({
                        'from': cls['name'],
                        'to': parent,
                        'type': 'inheritance'
                    })

            # Association from attributes
            for attr in cls.get('attributes', []):
                attr_type = attr.get('type', '')
                # Check if type references another class
                for class_name in class_names:
                    if class_name in attr_type and class_name != cls['name']:
                        relationships.append({
                            'from': cls['name'],
                            'to': class_name,
                            'type': 'association',
                            'label': attr.get('name', '')
                        })

        return relationships

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _sanitize_id(self, node_id: str) -> str:
        """Sanitize node ID for Mermaid compatibility"""
        if not node_id:
            return ''
        # Replace spaces and special chars with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', str(node_id))
        # Ensure doesn't start with number
        if sanitized and sanitized[0].isdigit():
            sanitized = f'n{sanitized}'
        return sanitized

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - SWIMLANE
    # =========================================================================

    def generate_swimlane(self, data: Dict[str, Any], direction: str = 'LR') -> str:
        """
        Generate swimlane diagram for cross-functional processes

        Expected input format:
        {
            "title": "Order Fulfillment Process",
            "direction": "LR",
            "lanes": [
                {
                    "id": "customer",
                    "label": "Customer",
                    "steps": [
                        {"id": "order", "label": "Place Order", "shape": "stadium"},
                        {"id": "receive", "label": "Receive Package", "shape": "stadium"}
                    ]
                },
                {
                    "id": "sales",
                    "label": "Sales Team",
                    "steps": [
                        {"id": "verify", "label": "Verify Order", "shape": "rect"},
                        {"id": "confirm", "label": "Send Confirmation", "shape": "rect"}
                    ]
                },
                {
                    "id": "warehouse",
                    "label": "Warehouse",
                    "steps": [
                        {"id": "pick", "label": "Pick Items", "shape": "rect"},
                        {"id": "pack", "label": "Pack Order", "shape": "rect"},
                        {"id": "ship", "label": "Ship", "shape": "rect"}
                    ]
                }
            ],
            "flows": [
                {"from": "order", "to": "verify"},
                {"from": "verify", "to": "confirm"},
                {"from": "confirm", "to": "pick"},
                {"from": "pick", "to": "pack"},
                {"from": "pack", "to": "ship"},
                {"from": "ship", "to": "receive"}
            ],
            "handoffs": [
                {"from": "order", "to": "verify", "label": "Order details"},
                {"from": "ship", "to": "receive", "label": "Tracking info"}
            ]
        }
        """
        self.log("Generating swimlane diagram")

        direction = data.get('direction', direction).upper()
        if direction not in ['LR', 'TD', 'TB']:
            direction = 'LR'

        lines = [f"flowchart {direction}"]

        # Title as comment
        if 'title' in data:
            lines.insert(0, f"%% {data['title']}")
            lines.insert(1, f"%% Swimlane Process Diagram")

        # Lane styles (alternate colors)
        lane_colors = ['#e3f2fd', '#fff3e0', '#e8f5e9', '#fce4ec', '#f3e5f5', '#e0f7fa']

        # Generate lanes as subgraphs
        lanes = data.get('lanes', [])
        all_nodes: List[Tuple[str, int]] = []

        for idx, lane in enumerate(lanes):
            lane_id = self._sanitize_id(lane.get('id', f'lane{idx}'))
            lane_label = lane.get('label', lane_id)
            color = lane_colors[idx % len(lane_colors)]

            lines.append(f"    subgraph {lane_id}[{lane_label}]")

            for step in lane.get('steps', []):
                step_id = self._sanitize_id(step.get('id', ''))
                step_label = step.get('label', step_id)
                shape = step.get('shape', 'rect')

                node_def = self._format_node(step_id, step_label, shape)
                lines.append(f"        {node_def}")
                all_nodes.append((step_id, idx))

            lines.append("    end")
            lines.append("")

        # Generate flows within lanes
        flows = data.get('flows', [])
        for flow in flows:
            from_id = self._sanitize_id(flow.get('from', ''))
            to_id = self._sanitize_id(flow.get('to', ''))
            label = flow.get('label', '')

            if label:
                lines.append(f"    {from_id} -->|{label}| {to_id}")
            else:
                lines.append(f"    {from_id} --> {to_id}")

        # Generate handoffs (cross-lane flows with different styling)
        handoffs = data.get('handoffs', [])
        for handoff in handoffs:
            from_id = self._sanitize_id(handoff.get('from', ''))
            to_id = self._sanitize_id(handoff.get('to', ''))
            label = handoff.get('label', 'Handoff')

            # Use dotted line for handoffs
            lines.append(f"    {from_id} -.->|{label}| {to_id}")

        # Apply lane background styles
        lines.append("")
        for idx, lane in enumerate(lanes):
            lane_id = self._sanitize_id(lane.get('id', f'lane{idx}'))
            color = lane_colors[idx % len(lane_colors)]
            lines.append(f"    style {lane_id} fill:{color},stroke:#666")

        return '\n'.join(lines)

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - JOURNEY MAP
    # =========================================================================

    def generate_journey(self, data: Dict[str, Any]) -> str:
        """
        Generate user journey map diagram

        Expected input format:
        {
            "title": "Customer Onboarding Journey",
            "sections": [
                {
                    "name": "Discovery",
                    "tasks": [
                        {"name": "Find website", "score": 5, "actor": "Customer"},
                        {"name": "Browse products", "score": 4, "actor": "Customer"},
                        {"name": "Read reviews", "score": 4, "actor": "Customer"}
                    ]
                },
                {
                    "name": "Sign Up",
                    "tasks": [
                        {"name": "Create account", "score": 3, "actor": "Customer"},
                        {"name": "Verify email", "score": 2, "actor": "Customer"},
                        {"name": "Complete profile", "score": 3, "actor": "Customer"}
                    ]
                },
                {
                    "name": "First Purchase",
                    "tasks": [
                        {"name": "Add to cart", "score": 4, "actor": "Customer"},
                        {"name": "Enter payment", "score": 2, "actor": "Customer"},
                        {"name": "Receive confirmation", "score": 5, "actor": "Customer"}
                    ]
                }
            ]
        }
        """
        self.log("Generating journey map diagram")

        lines = ["journey"]

        # Title
        title = data.get('title', 'User Journey')
        lines.append(f"    title {title}")
        lines.append("")

        # Sections and tasks
        sections = data.get('sections', [])
        for section in sections:
            section_name = section.get('name', 'Section')
            lines.append(f"    section {section_name}")

            for task in section.get('tasks', []):
                task_name = task.get('name', 'Task')
                score = task.get('score', 3)  # 1-5 happiness score
                actor = task.get('actor', 'User')

                # Score must be 1-5
                score = max(1, min(5, int(score)))
                lines.append(f"        {task_name}: {score}: {actor}")

        return '\n'.join(lines)

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - GANTT
    # =========================================================================

    def generate_gantt(self, data: Dict[str, Any]) -> str:
        """
        Generate Gantt chart for project timelines

        Expected input format:
        {
            "title": "Project Implementation Timeline",
            "dateFormat": "YYYY-MM-DD",
            "excludes": ["weekends"],
            "sections": [
                {
                    "name": "Planning",
                    "tasks": [
                        {"name": "Requirements gathering", "id": "req", "start": "2025-01-01", "duration": "5d"},
                        {"name": "Design review", "id": "design", "after": "req", "duration": "3d"}
                    ]
                },
                {
                    "name": "Development",
                    "tasks": [
                        {"name": "Backend API", "id": "api", "after": "design", "duration": "10d"},
                        {"name": "Frontend UI", "id": "ui", "after": "design", "duration": "8d"},
                        {"name": "Integration", "id": "int", "after": "api ui", "duration": "5d"}
                    ]
                },
                {
                    "name": "Testing",
                    "tasks": [
                        {"name": "QA Testing", "id": "qa", "after": "int", "duration": "5d", "critical": true},
                        {"name": "UAT", "id": "uat", "after": "qa", "duration": "3d"}
                    ]
                },
                {
                    "name": "Milestones",
                    "tasks": [
                        {"name": "Beta Release", "milestone": "beta", "after": "qa", "duration": "0d"},
                        {"name": "Go Live", "milestone": "live", "after": "uat", "duration": "0d"}
                    ]
                }
            ]
        }
        """
        self.log("Generating Gantt chart")

        lines = ["gantt"]

        # Title
        title = data.get('title', 'Project Timeline')
        lines.append(f"    title {title}")

        # Date format
        date_format = data.get('dateFormat', 'YYYY-MM-DD')
        lines.append(f"    dateFormat {date_format}")

        # Excludes
        excludes = data.get('excludes', [])
        if excludes:
            lines.append(f"    excludes {', '.join(excludes)}")

        lines.append("")

        # Sections and tasks
        sections = data.get('sections', [])
        for section in sections:
            section_name = section.get('name', 'Section')
            lines.append(f"    section {section_name}")

            for task in section.get('tasks', []):
                task_name = task.get('name', 'Task')
                task_id = task.get('id', '')
                start = task.get('start', '')
                after = task.get('after', '')
                duration = task.get('duration', '1d')
                critical = task.get('critical', False)
                milestone = task.get('milestone', '')

                # Build task definition
                parts = [task_name]

                # Add task ID and status
                if task_id:
                    if critical:
                        parts.append(f": crit, {task_id}")
                    elif milestone:
                        parts.append(f": milestone, {milestone}")
                    else:
                        parts.append(f": {task_id}")
                elif critical:
                    parts.append(": crit")
                elif milestone:
                    parts.append(f": milestone, {milestone}")

                # Add timing
                if after:
                    parts.append(f", after {after}")
                elif start:
                    parts.append(f", {start}")

                # Add duration
                parts.append(f", {duration}")

                lines.append(f"        {''.join(parts)}")

        return '\n'.join(lines)

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - QUADRANT CHART
    # =========================================================================

    def generate_quadrant(self, data: Dict[str, Any]) -> str:
        """
        Generate quadrant chart for prioritization matrices

        Expected input format:
        {
            "title": "Feature Prioritization Matrix",
            "x_axis": {"label": "Implementation Effort", "low": "Low Effort", "high": "High Effort"},
            "y_axis": {"label": "Business Value", "low": "Low Value", "high": "High Value"},
            "quadrants": {
                "q1": {"label": "Quick Wins", "description": "Do First"},
                "q2": {"label": "Major Projects", "description": "Plan Carefully"},
                "q3": {"label": "Fill-ins", "description": "Do If Time"},
                "q4": {"label": "Thankless Tasks", "description": "Avoid"}
            },
            "points": [
                {"label": "Feature A", "x": 0.2, "y": 0.8},
                {"label": "Feature B", "x": 0.8, "y": 0.9},
                {"label": "Feature C", "x": 0.3, "y": 0.3},
                {"label": "Feature D", "x": 0.7, "y": 0.2},
                {"label": "Feature E", "x": 0.5, "y": 0.5}
            ]
        }
        """
        self.log("Generating quadrant chart")

        lines = ["quadrantChart"]

        # Title
        title = data.get('title', 'Quadrant Chart')
        lines.append(f"    title {title}")

        # X-axis
        x_axis = data.get('x_axis', {})
        x_low = x_axis.get('low', 'Low')
        x_high = x_axis.get('high', 'High')
        lines.append(f'    x-axis "{x_low}" --> "{x_high}"')

        # Y-axis
        y_axis = data.get('y_axis', {})
        y_low = y_axis.get('low', 'Low')
        y_high = y_axis.get('high', 'High')
        lines.append(f'    y-axis "{y_low}" --> "{y_high}"')

        # Quadrant labels
        quadrants = data.get('quadrants', {})
        if quadrants:
            q1 = quadrants.get('q1', {}).get('label', 'Quadrant 1')
            q2 = quadrants.get('q2', {}).get('label', 'Quadrant 2')
            q3 = quadrants.get('q3', {}).get('label', 'Quadrant 3')
            q4 = quadrants.get('q4', {}).get('label', 'Quadrant 4')

            lines.append(f'    quadrant-1 {q1}')
            lines.append(f'    quadrant-2 {q2}')
            lines.append(f'    quadrant-3 {q3}')
            lines.append(f'    quadrant-4 {q4}')

        lines.append("")

        # Data points
        points = data.get('points', [])
        for point in points:
            label = point.get('label', 'Point')
            x = point.get('x', 0.5)
            y = point.get('y', 0.5)

            # Ensure coordinates are 0-1
            x = max(0, min(1, float(x)))
            y = max(0, min(1, float(y)))

            lines.append(f'    "{label}": [{x}, {y}]')

        return '\n'.join(lines)

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - TIMELINE
    # =========================================================================

    def generate_timeline(self, data: Dict[str, Any]) -> str:
        """
        Generate timeline diagram for roadmaps and event sequences

        Expected input format:
        {
            "title": "Product Roadmap 2025",
            "periods": [
                {
                    "name": "Q1 2025",
                    "events": ["MVP Launch", "Beta Testing", "First 100 Users"]
                },
                {
                    "name": "Q2 2025",
                    "events": ["Public Launch", "Mobile App", "API v2"]
                },
                {
                    "name": "Q3 2025",
                    "events": ["Enterprise Features", "SOC2 Certification"]
                },
                {
                    "name": "Q4 2025",
                    "events": ["International Expansion", "Series A"]
                }
            ]
        }
        """
        self.log("Generating timeline diagram")

        lines = ["timeline"]

        # Title
        title = data.get('title', 'Timeline')
        lines.append(f"    title {title}")
        lines.append("")

        # Periods and events
        periods = data.get('periods', [])
        for period in periods:
            period_name = period.get('name', 'Period')
            events = period.get('events', [])

            lines.append(f"    {period_name}")
            for event in events:
                lines.append(f"        : {event}")

        return '\n'.join(lines)

    # =========================================================================
    # BUSINESS ANALYSIS DIAGRAMS - MINDMAP
    # =========================================================================

    def generate_mindmap(self, data: Dict[str, Any]) -> str:
        """
        Generate mindmap diagram for brainstorming and idea organization

        Expected input format:
        {
            "root": "Process Improvement",
            "branches": [
                {
                    "label": "Pain Points",
                    "children": [
                        {"label": "Long cycle times", "children": ["Manual data entry", "Approval delays"]},
                        {"label": "High error rates", "children": ["No validation", "Paper forms"]},
                        {"label": "Poor visibility", "children": ["No tracking", "Siloed data"]}
                    ]
                },
                {
                    "label": "Solutions",
                    "children": [
                        {"label": "Automation", "children": ["RPA", "Workflows"]},
                        {"label": "Integration", "children": ["API", "Data sync"]},
                        {"label": "Dashboards", "children": ["Real-time", "Self-service"]}
                    ]
                },
                {
                    "label": "Success Metrics",
                    "children": [
                        {"label": "50% cycle time reduction"},
                        {"label": "90% error reduction"},
                        {"label": "Real-time visibility"}
                    ]
                }
            ]
        }
        """
        self.log("Generating mindmap diagram")

        lines = ["mindmap"]

        # Root node
        root = data.get('root', 'Root')
        lines.append(f"    root(({root}))")

        # Generate branches recursively
        branches = data.get('branches', [])
        for branch in branches:
            self._add_mindmap_branch(lines, branch, indent=2)

        return '\n'.join(lines)

    def _add_mindmap_branch(self, lines: List[str], node: Dict[str, Any], indent: int = 2) -> None:
        """Recursively add mindmap branches"""
        spaces = "    " * indent
        label = node.get('label', 'Node')

        # Add this node
        lines.append(f"{spaces}{label}")

        # Add children
        children = node.get('children', [])
        for child in children:
            if isinstance(child, str):
                # Simple string child
                lines.append(f"{spaces}    {child}")
            elif isinstance(child, dict):
                # Nested child with potential grandchildren
                self._add_mindmap_branch(lines, child, indent + 1)

    def generate_diagram(self, diagram_type: str, data: Dict[str, Any],
                         **kwargs: Any) -> str:
        """Generate diagram of specified type"""
        generators = {
            # Technical diagrams
            'flowchart': self.generate_flowchart,
            'sequence': self.generate_sequence,
            'class': self.generate_class,
            'erd': self.generate_erd,
            'state': self.generate_state,
            'architecture': self.generate_architecture,
            # Business analysis diagrams
            'swimlane': self.generate_swimlane,
            'journey': self.generate_journey,
            'gantt': self.generate_gantt,
            'quadrant': self.generate_quadrant,
            'timeline': self.generate_timeline,
            'mindmap': self.generate_mindmap,
        }

        generator = generators.get(diagram_type)
        if not generator:
            raise ValueError(f"Unknown diagram type: {diagram_type}. "
                           f"Supported: {list(generators.keys())}")

        # Handle direction parameter for flowchart and swimlane
        if diagram_type in ['flowchart', 'swimlane']:
            return generator(data, **kwargs)
        return generator(data)

    def format_output(self, diagram: str, output_format: str = 'mermaid',
                      title: str = '') -> str:
        """Format diagram for output"""
        if output_format == 'mermaid':
            return diagram

        elif output_format == 'markdown':
            lines = []
            if title:
                lines.append(f"# {title}")
                lines.append("")
            lines.append("```mermaid")
            lines.append(diagram)
            lines.append("```")
            return '\n'.join(lines)

        elif output_format == 'html':
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title or 'Mermaid Diagram'}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <h1>{title}</h1>
    <div class="mermaid">
{diagram}
    </div>
    <script>mermaid.initialize({{startOnLoad: true}});</script>
</body>
</html>"""
            return html

        else:
            raise ValueError(f"Unknown output format: {output_format}")


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate command-line arguments"""
    if args.input and args.scan:
        raise ValueError("Cannot use both --input and --scan")

    if not args.input and not args.scan:
        raise ValueError("Must specify either --input or --scan")

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            raise ValueError(f"Input file not found: {args.input}")
        if input_path.suffix.lower() not in ['.json', '.yaml', '.yml']:
            raise ValueError(f"Unsupported input format: {input_path.suffix}")

    if args.scan:
        scan_path = Path(args.scan)
        if not scan_path.exists():
            raise ValueError(f"Scan directory not found: {args.scan}")
        if not scan_path.is_dir():
            raise ValueError(f"Scan path must be a directory: {args.scan}")

    if args.type not in DIAGRAM_TYPES:
        raise ValueError(f"Unknown diagram type: {args.type}. "
                        f"Supported: {list(DIAGRAM_TYPES.keys())}")


def main() -> None:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate Mermaid diagrams for technical and business documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples - Technical Diagrams:
  # Flowchart from JSON definition
  python mermaid_diagram_generator.py --type flowchart --input process.json

  # Sequence diagram from YAML
  python mermaid_diagram_generator.py --type sequence --input api-flow.yaml

  # Class diagram by scanning source code
  python mermaid_diagram_generator.py --type class --scan src/models/

  # ERD from database schema
  python mermaid_diagram_generator.py --type erd --input schema.json

  # Architecture diagram
  python mermaid_diagram_generator.py --type architecture --input system.json

Examples - Business Analysis Diagrams:
  # Swimlane process diagram (cross-functional flows)
  python mermaid_diagram_generator.py --type swimlane --input order-process.json

  # Customer journey map
  python mermaid_diagram_generator.py --type journey --input onboarding.json

  # Project Gantt chart
  python mermaid_diagram_generator.py --type gantt --input timeline.json

  # Quadrant priority matrix
  python mermaid_diagram_generator.py --type quadrant --input features.json

  # Timeline / roadmap
  python mermaid_diagram_generator.py --type timeline --input roadmap.json

  # Mindmap for brainstorming
  python mermaid_diagram_generator.py --type mindmap --input ideas.json

  # Output as markdown with title
  python mermaid_diagram_generator.py --type swimlane --input flow.json \\
      --output markdown --title "Order Fulfillment Process"

Diagram Types (Technical):
  flowchart    - Process flows, decision trees, workflows
  sequence     - API calls, service interactions, message flows
  class        - Object models, inheritance hierarchies, interfaces
  erd          - Database schemas, entity relationships
  state        - State machines, workflow states, lifecycles
  architecture - System architecture, component diagrams

Diagram Types (Business Analysis):
  swimlane     - Cross-functional process flows with role/dept lanes
  journey      - Customer/user journey maps with touchpoints
  gantt        - Project timelines, milestones, dependencies
  quadrant     - Priority matrices, effort/impact, risk assessment
  timeline     - Event timelines, roadmaps, milestones
  mindmap      - Brainstorming, idea organization, hierarchies

Complementary Tools:
  - business-analyst-toolkit/stakeholder_mapper.py: Stakeholder relationships
  - technical-writer/mermaid_diagram_generator.py: All other diagram types

Input Formats:
  JSON - Full-featured structured input (recommended)
  YAML - Simple key-value input (basic parser)

Output Formats:
  mermaid  - Raw Mermaid syntax (default)
  markdown - Mermaid wrapped in markdown code block
  html     - Standalone HTML page with Mermaid.js

Exit Codes:
  0 - Success
  1 - Validation error
  2 - Parse error
  3 - Generation error
        """
    )

    parser.add_argument(
        '--type', '-t',
        required=True,
        choices=list(DIAGRAM_TYPES.keys()),
        help='Type of diagram to generate'
    )

    parser.add_argument(
        '--input', '-i',
        help='Input file (JSON or YAML) with diagram definition'
    )

    parser.add_argument(
        '--scan', '-s',
        help='Directory to scan for code (for class diagrams)'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['mermaid', 'markdown', 'html'],
        default='mermaid',
        help='Output format (default: mermaid)'
    )

    parser.add_argument(
        '--title',
        help='Diagram title (for markdown/html output)'
    )

    parser.add_argument(
        '--direction', '-d',
        choices=['TD', 'TB', 'BT', 'LR', 'RL'],
        default='TD',
        help='Flowchart direction (default: TD)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        validate_arguments(args)

        generator = MermaidDiagramGenerator(verbose=args.verbose)

        # Load or scan data
        if args.input:
            data = generator.load_input(Path(args.input))
        elif args.scan:
            if args.type != 'class':
                raise ValueError("--scan only supported for class diagrams")
            data = generator.scan_directory_for_classes(Path(args.scan))

        # Generate diagram
        diagram = generator.generate_diagram(
            args.type,
            data,
            direction=args.direction
        )

        # Format output
        title = args.title or data.get('title', '')
        output = generator.format_output(diagram, args.output, title)

        print(output)
        sys.exit(EXIT_SUCCESS)

    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)

    except json.JSONDecodeError as e:
        print(f"Parse Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)

    except Exception as e:
        print(f"Generation Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_GENERATION_ERROR)


if __name__ == '__main__':
    main()
