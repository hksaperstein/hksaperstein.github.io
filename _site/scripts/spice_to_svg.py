#!/usr/bin/env python3
"""
SPICE to SVG Schematic Generator
Converts SPICE netlists to professional-quality circuit schematics in SVG format.

Features:
- Professional IEEE/IEC component symbols
- Automatic wire routing with connection dots
- Clean black and white output
- Component labels and values
- Node labeling
- Support for R, C, L, D, Q, M, V, I components

Usage:
    python spice_to_svg.py <spice_file> [output_file.svg]

Example:
    python spice_to_svg.py circuit.cir
    python spice_to_svg.py circuit.cir schematic.svg
"""

import re
import sys
import math
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict


@dataclass
class Component:
    """Represents an electronic component"""
    name: str           # e.g., R1, C1, Q1
    type: str           # e.g., 'R', 'C', 'L', 'Q', 'D'
    value: str          # e.g., '10k', '100uF'
    nodes: List[str]    # Connection nodes
    x: int = 0          # X position
    y: int = 0          # Y position
    rotation: int = 0   # Rotation in degrees (0, 90, 180, 270)
    ports: Dict[int, Tuple[int, int]] = field(default_factory=dict)  # Pin positions


@dataclass
class Connection:
    """Represents a connection between components"""
    node: str
    components: List[Tuple[str, int]]  # (component_name, pin_index)


class SPICEParser:
    """Parses SPICE netlists with support for common component types"""
    
    COMPONENT_TYPES = {
        'R': 'Resistor',
        'C': 'Capacitor',
        'L': 'Inductor',
        'D': 'Diode',
        'Q': 'BJT Transistor',
        'M': 'MOSFET',
        'J': 'JFET',
        'V': 'Voltage Source',
        'I': 'Current Source',
        'X': 'Subcircuit',
        'U': 'IC/Chip',
    }
    
    def __init__(self, filepath: str = None, content: str = None):
        self.filepath = filepath
        self.content = content
        self.components: Dict[str, Component] = {}
        self.connections: Dict[str, Connection] = {}
        self.title = "Circuit Schematic"
        
    def parse(self) -> Tuple[Dict[str, Component], Dict[str, Connection]]:
        """Parse SPICE netlist file or content"""
        if self.filepath:
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                print(f"Error: File '{self.filepath}' not found")
                sys.exit(1)
            except UnicodeDecodeError:
                with open(self.filepath, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
        elif self.content:
            lines = self.content.split('\n')
        else:
            print("Error: No input provided")
            sys.exit(1)
        
        # Join continuation lines (lines starting with +)
        joined_lines = []
        current_line = ""
        for line in lines:
            line = line.rstrip()
            if line.startswith('+'):
                current_line += ' ' + line[1:].strip()
            else:
                if current_line:
                    joined_lines.append(current_line)
                current_line = line
        if current_line:
            joined_lines.append(current_line)
        
        for line in joined_lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('*'):
                continue
            
            # Parse directives
            if line.startswith('.'):
                if line.upper().startswith('.TITLE'):
                    self.title = line.split(maxsplit=1)[1] if len(line.split(maxsplit=1)) > 1 else "Circuit"
                continue
            
            # First line is often the title
            if not self.components and not line.startswith('.'):
                first_char = line[0].upper() if line else ''
                if first_char not in self.COMPONENT_TYPES:
                    self.title = line
                    continue
            
            # Parse component lines
            self._parse_component_line(line)
        
        # Build connection map
        self._build_connections()
        
        return self.components, self.connections
    
    def _parse_component_line(self, line: str):
        """Parse a single component line with improved value extraction"""
        parts = line.split()
        if not parts:
            return
        
        comp_name = parts[0]
        comp_type = comp_name[0].upper()
        
        if comp_type not in self.COMPONENT_TYPES:
            return
        
        if len(parts) < 3:
            return
        
        # Parse based on component type
        if comp_type in ['R', 'C', 'L']:
            # Format: R1 node1 node2 value [model] [params]
            nodes = [parts[1], parts[2]]
            value = self._extract_value(parts[3:])
            self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type == 'D':
            # Format: D1 anode cathode model [params]
            nodes = [parts[1], parts[2]]
            value = parts[3] if len(parts) > 3 else "D"
            self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type == 'Q':
            # Format: Q1 collector base emitter [substrate] model
            if len(parts) >= 5:
                nodes = [parts[1], parts[2], parts[3]]  # C, B, E
                value = parts[4] if len(parts) > 4 else "NPN"
                self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type == 'M':
            # Format: M1 drain gate source bulk model [params]
            if len(parts) >= 6:
                nodes = [parts[1], parts[2], parts[3], parts[4]]  # D, G, S, B
                value = parts[5] if len(parts) > 5 else "NMOS"
                self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type == 'J':
            # Format: J1 drain gate source model
            if len(parts) >= 5:
                nodes = [parts[1], parts[2], parts[3]]  # D, G, S
                value = parts[4] if len(parts) > 4 else "JFET"
                self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type in ['V', 'I']:
            # Format: V1 n+ n- [DC value] [AC mag [phase]] [transient]
            nodes = [parts[1], parts[2]]
            value = self._extract_source_value(parts[3:])
            self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
        
        elif comp_type in ['X', 'U']:
            # Subcircuit/IC - variable number of nodes
            # Last part is the subcircuit name
            if len(parts) >= 3:
                nodes = parts[1:-1]
                value = parts[-1]
                self.components[comp_name] = Component(comp_name, comp_type, value, nodes)
    
    def _extract_value(self, parts: List[str]) -> str:
        """Extract component value from remaining parts"""
        if not parts:
            return ""
        # First part is usually the value
        value = parts[0]
        # Clean up common suffixes
        value = value.upper().replace('OHM', 'Ω').replace('OHMS', 'Ω')
        return value
    
    def _extract_source_value(self, parts: List[str]) -> str:
        """Extract source value from remaining parts"""
        if not parts:
            return "DC"
        value_parts = []
        for p in parts:
            if '=' in p:
                break
            value_parts.append(p)
        return ' '.join(value_parts) if value_parts else "DC"
    
    def _build_connections(self):
        """Build connection map from components"""
        for comp_name, comp in self.components.items():
            for pin_idx, node in enumerate(comp.nodes):
                if node not in self.connections:
                    self.connections[node] = Connection(node, [])
                self.connections[node].components.append((comp_name, pin_idx))


class SchematicRenderer:
    """
    Renders professional-quality circuit schematics to SVG.
    Uses IEEE/IEC standard symbols with clean black and white styling.
    """
    
    # Component dimensions
    GRID_SIZE = 20          # Base grid unit
    COMP_WIDTH = 60         # Component symbol width
    COMP_HEIGHT = 30        # Component symbol height
    WIRE_WIDTH = 2          # Wire stroke width
    SYMBOL_WIDTH = 2        # Symbol stroke width
    DOT_RADIUS = 4          # Connection dot radius
    FONT_SIZE = 12          # Label font size
    FONT_SIZE_SMALL = 10    # Small label font size
    
    # Layout settings
    MARGIN = 80
    COMP_SPACING_X = 180    # Horizontal spacing between components
    COMP_SPACING_Y = 140    # Vertical spacing between components
    COLS_MAX = 5            # Maximum columns before wrapping
    
    def __init__(self, components: Dict[str, Component], connections: Dict[str, Connection], title: str = "Circuit Schematic"):
        self.components = components
        self.connections = connections
        self.title = title
        self.width = 1200
        self.height = 800
        self.node_positions: Dict[str, List[Tuple[int, int]]] = defaultdict(list)  # Track wire endpoints per node
        
    def render(self, output_file: str):
        """Render the schematic to an SVG file"""
        # Calculate layout
        self._calculate_layout()
        
        # Adjust canvas size based on component positions
        self._adjust_canvas_size()
        
        # Create SVG root
        root = ET.Element('svg', {
            'xmlns': 'http://www.w3.org/2000/svg',
            'viewBox': f'0 0 {self.width} {self.height}',
            'width': str(self.width),
            'height': str(self.height),
            'style': 'background-color: white;'
        })
        
        # Add defs for markers and patterns
        self._add_defs(root)
        
        # Add stylesheet
        self._add_styles(root)
        
        # Add title
        self._add_title(root)
        
        # Create groups for layering
        wires_group = ET.SubElement(root, 'g', {'id': 'wires', 'class': 'wires-layer'})
        components_group = ET.SubElement(root, 'g', {'id': 'components', 'class': 'components-layer'})
        labels_group = ET.SubElement(root, 'g', {'id': 'labels', 'class': 'labels-layer'})
        
        # Draw components first to get port positions
        for comp_name, comp in sorted(self.components.items()):
            self._draw_component(components_group, labels_group, comp)
        
        # Draw wires between connected components
        self._draw_all_connections(wires_group)
        
        # Add legend
        self._add_legend(root)
        
        # Save to file
        self._save_svg(root, output_file)
        
        print(f"✓ Schematic saved to: {output_file}")
        print(f"  - {len(self.components)} components")
        print(f"  - {len(self.connections)} nodes")
    
    def _calculate_layout(self):
        """Calculate component positions using a grid layout"""
        comp_list = sorted(self.components.keys())
        
        # Calculate grid dimensions
        num_components = len(comp_list)
        cols = min(self.COLS_MAX, num_components)
        rows = math.ceil(num_components / cols)
        
        for idx, comp_name in enumerate(comp_list):
            comp = self.components[comp_name]
            col = idx % cols
            row = idx // cols
            
            comp.x = self.MARGIN + col * self.COMP_SPACING_X + self.COMP_SPACING_X // 2
            comp.y = self.MARGIN + 60 + row * self.COMP_SPACING_Y + self.COMP_SPACING_Y // 2
    
    def _adjust_canvas_size(self):
        """Adjust canvas size to fit all components"""
        max_x = max_y = 0
        for comp in self.components.values():
            max_x = max(max_x, comp.x + self.COMP_SPACING_X)
            max_y = max(max_y, comp.y + self.COMP_SPACING_Y)
        
        self.width = max(self.width, max_x + self.MARGIN)
        self.height = max(self.height, max_y + self.MARGIN + 50)  # Extra space for legend
    
    def _add_defs(self, root: ET.Element):
        """Add SVG definitions for markers and gradients"""
        defs = ET.SubElement(root, 'defs')
        
        # Arrow marker for current sources
        marker = ET.SubElement(defs, 'marker', {
            'id': 'arrowhead',
            'markerWidth': '10',
            'markerHeight': '7',
            'refX': '9',
            'refY': '3.5',
            'orient': 'auto'
        })
        ET.SubElement(marker, 'polygon', {
            'points': '0 0, 10 3.5, 0 7',
            'fill': 'black'
        })
    
    def _add_styles(self, root: ET.Element):
        """Add CSS styles for consistent black and white rendering"""
        style = ET.SubElement(root, 'style')
        style.text = """
            /* Base styles */
            .wire { stroke: #000000; stroke-width: 2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
            .symbol { stroke: #000000; stroke-width: 2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
            .symbol-filled { stroke: #000000; stroke-width: 2; fill: #000000; }
            .connection-dot { fill: #000000; stroke: none; }
            
            /* Text styles */
            .title-text { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 18px; font-weight: bold; fill: #000000; }
            .comp-name { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 12px; font-weight: bold; fill: #000000; }
            .comp-value { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 11px; fill: #000000; }
            .node-label { font-family: 'Courier New', monospace; font-size: 9px; fill: #444444; }
            .pin-label { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 8px; fill: #666666; }
            .legend-text { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 10px; fill: #000000; }
            
            /* Plus/minus symbols */
            .polarity { font-family: 'Arial', 'Helvetica', sans-serif; font-size: 14px; font-weight: bold; fill: #000000; }
        """
    
    def _add_title(self, root: ET.Element):
        """Add schematic title"""
        title_group = ET.SubElement(root, 'g', {'id': 'title'})
        
        # Title text
        title_elem = ET.SubElement(title_group, 'text', {
            'x': str(self.MARGIN),
            'y': str(self.MARGIN // 2 + 10),
            'class': 'title-text'
        })
        title_elem.text = self.title
        
        # Underline
        ET.SubElement(title_group, 'line', {
            'x1': str(self.MARGIN),
            'y1': str(self.MARGIN // 2 + 15),
            'x2': str(self.MARGIN + len(self.title) * 10),
            'y2': str(self.MARGIN // 2 + 15),
            'class': 'wire'
        })
    
    def _add_legend(self, root: ET.Element):
        """Add component count legend"""
        legend_y = self.height - 30
        legend_x = self.MARGIN
        
        legend_group = ET.SubElement(root, 'g', {'id': 'legend'})
        
        # Count components by type
        type_counts = defaultdict(int)
        for comp in self.components.values():
            type_counts[comp.type] += 1
        
        legend_text = "Components: " + ", ".join([f"{SPICEParser.COMPONENT_TYPES.get(t, t)}s: {c}" for t, c in sorted(type_counts.items())])
        
        text_elem = ET.SubElement(legend_group, 'text', {
            'x': str(legend_x),
            'y': str(legend_y),
            'class': 'legend-text'
        })
        text_elem.text = legend_text
    
    def _draw_component(self, comp_group: ET.Element, label_group: ET.Element, comp: Component):
        """Draw a component symbol with labels"""
        x, y = comp.x, comp.y
        
        # Create component group
        g = ET.SubElement(comp_group, 'g', {
            'id': f'comp-{comp.name}',
            'transform': f'translate({x}, {y})'
        })
        
        # Draw symbol based on type
        if comp.type == 'R':
            self._draw_resistor_symbol(g, comp)
        elif comp.type == 'C':
            self._draw_capacitor_symbol(g, comp)
        elif comp.type == 'L':
            self._draw_inductor_symbol(g, comp)
        elif comp.type == 'D':
            self._draw_diode_symbol(g, comp)
        elif comp.type == 'Q':
            self._draw_bjt_symbol(g, comp)
        elif comp.type == 'M':
            self._draw_mosfet_symbol(g, comp)
        elif comp.type == 'J':
            self._draw_jfet_symbol(g, comp)
        elif comp.type == 'V':
            self._draw_voltage_source_symbol(g, comp)
        elif comp.type == 'I':
            self._draw_current_source_symbol(g, comp)
        else:
            self._draw_generic_symbol(g, comp)
        
        # Add labels in label group (so they appear on top)
        label_g = ET.SubElement(label_group, 'g', {'transform': f'translate({x}, {y})'})
        self._add_component_labels(label_g, comp)
        
        # Register port positions for wire routing
        self._register_ports(comp)
    
    def _draw_resistor_symbol(self, g: ET.Element, comp: Component):
        """Draw IEEE-style resistor (zigzag)"""
        # Zigzag pattern
        points = []
        w = 40  # Total width of zigzag
        h = 8   # Height of zigzag peaks
        segments = 6
        step = w / segments
        
        points.append(f"M {-w//2 - 20} 0")  # Start lead
        points.append(f"L {-w//2} 0")
        
        for i in range(segments):
            x = -w//2 + i * step + step/2
            peak = h if i % 2 == 0 else -h
            points.append(f"L {x} {peak}")
        
        points.append(f"L {w//2} 0")
        points.append(f"L {w//2 + 20} 0")  # End lead
        
        ET.SubElement(g, 'path', {
            'd': ' '.join(points),
            'class': 'symbol'
        })
        
        # Store port positions (relative to component center)
        comp.ports[0] = (-60, 0)  # Left terminal
        comp.ports[1] = (60, 0)   # Right terminal
    
    def _draw_capacitor_symbol(self, g: ET.Element, comp: Component):
        """Draw capacitor symbol (two parallel plates)"""
        plate_height = 24
        gap = 8
        
        # Left plate
        ET.SubElement(g, 'line', {
            'x1': str(-gap//2), 'y1': str(-plate_height//2),
            'x2': str(-gap//2), 'y2': str(plate_height//2),
            'class': 'symbol'
        })
        
        # Right plate
        ET.SubElement(g, 'line', {
            'x1': str(gap//2), 'y1': str(-plate_height//2),
            'x2': str(gap//2), 'y2': str(plate_height//2),
            'class': 'symbol'
        })
        
        # Connection leads
        ET.SubElement(g, 'line', {
            'x1': '-60', 'y1': '0',
            'x2': str(-gap//2), 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': str(gap//2), 'y1': '0',
            'x2': '60', 'y2': '0',
            'class': 'wire'
        })
        
        comp.ports[0] = (-60, 0)
        comp.ports[1] = (60, 0)
    
    def _draw_inductor_symbol(self, g: ET.Element, comp: Component):
        """Draw inductor symbol (coil loops)"""
        num_loops = 4
        loop_width = 12
        total_width = num_loops * loop_width
        start_x = -total_width // 2
        
        # Draw arcs for coil
        path_parts = [f"M {start_x - 20} 0 L {start_x} 0"]
        for i in range(num_loops):
            x = start_x + i * loop_width
            path_parts.append(f"A {loop_width//2} {loop_width//2} 0 0 1 {x + loop_width} 0")
        path_parts.append(f"L {start_x + total_width + 20} 0")
        
        ET.SubElement(g, 'path', {
            'd': ' '.join(path_parts),
            'class': 'symbol'
        })
        
        comp.ports[0] = (-60, 0)
        comp.ports[1] = (60, 0)
    
    def _draw_diode_symbol(self, g: ET.Element, comp: Component):
        """Draw diode symbol (triangle with bar)"""
        size = 16
        
        # Triangle (pointing right)
        ET.SubElement(g, 'polygon', {
            'points': f'{-size},{ -size} {-size},{size} {size},0',
            'class': 'symbol'
        })
        
        # Cathode bar
        ET.SubElement(g, 'line', {
            'x1': str(size), 'y1': str(-size),
            'x2': str(size), 'y2': str(size),
            'class': 'symbol'
        })
        
        # Connection leads
        ET.SubElement(g, 'line', {
            'x1': '-60', 'y1': '0',
            'x2': str(-size), 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': str(size), 'y1': '0',
            'x2': '60', 'y2': '0',
            'class': 'wire'
        })
        
        comp.ports[0] = (-60, 0)  # Anode
        comp.ports[1] = (60, 0)   # Cathode
    
    def _draw_bjt_symbol(self, g: ET.Element, comp: Component):
        """Draw NPN BJT symbol"""
        # Base line (vertical)
        ET.SubElement(g, 'line', {
            'x1': '-10', 'y1': '-20',
            'x2': '-10', 'y2': '20',
            'class': 'symbol'
        })
        
        # Collector line
        ET.SubElement(g, 'line', {
            'x1': '-10', 'y1': '-10',
            'x2': '25', 'y2': '-30',
            'class': 'symbol'
        })
        
        # Emitter line with arrow
        ET.SubElement(g, 'line', {
            'x1': '-10', 'y1': '10',
            'x2': '25', 'y2': '30',
            'class': 'symbol'
        })
        
        # Emitter arrow
        ET.SubElement(g, 'polygon', {
            'points': '25,30 15,24 18,32',
            'class': 'symbol-filled'
        })
        
        # Connection leads
        ET.SubElement(g, 'line', {  # Base
            'x1': '-60', 'y1': '0',
            'x2': '-10', 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {  # Collector
            'x1': '25', 'y1': '-30',
            'x2': '60', 'y2': '-30',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {  # Emitter
            'x1': '25', 'y1': '30',
            'x2': '60', 'y2': '30',
            'class': 'wire'
        })
        
        # Pin labels
        self._add_pin_label(g, -30, -5, "B")
        self._add_pin_label(g, 40, -35, "C")
        self._add_pin_label(g, 40, 35, "E")
        
        comp.ports[0] = (60, -30)  # Collector
        comp.ports[1] = (-60, 0)   # Base
        comp.ports[2] = (60, 30)   # Emitter
    
    def _draw_mosfet_symbol(self, g: ET.Element, comp: Component):
        """Draw N-channel MOSFET symbol"""
        # Gate line (vertical, with gap)
        ET.SubElement(g, 'line', {
            'x1': '-15', 'y1': '-25',
            'x2': '-15', 'y2': '25',
            'class': 'symbol'
        })
        
        # Channel line (vertical, broken)
        ET.SubElement(g, 'line', {
            'x1': '-5', 'y1': '-25',
            'x2': '-5', 'y2': '-8',
            'class': 'symbol'
        })
        ET.SubElement(g, 'line', {
            'x1': '-5', 'y1': '-4',
            'x2': '-5', 'y2': '4',
            'class': 'symbol'
        })
        ET.SubElement(g, 'line', {
            'x1': '-5', 'y1': '8',
            'x2': '-5', 'y2': '25',
            'class': 'symbol'
        })
        
        # Drain connection
        ET.SubElement(g, 'line', {
            'x1': '-5', 'y1': '-20',
            'x2': '20', 'y2': '-20',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '20', 'y1': '-20',
            'x2': '20', 'y2': '-35',
            'class': 'wire'
        })
        
        # Source connection
        ET.SubElement(g, 'line', {
            'x1': '-5', 'y1': '20',
            'x2': '20', 'y2': '20',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '20', 'y1': '20',
            'x2': '20', 'y2': '35',
            'class': 'wire'
        })
        
        # Arrow on source
        ET.SubElement(g, 'polygon', {
            'points': '-5,0 5,-5 5,5',
            'class': 'symbol-filled'
        })
        
        # Gate lead
        ET.SubElement(g, 'line', {
            'x1': '-60', 'y1': '0',
            'x2': '-15', 'y2': '0',
            'class': 'wire'
        })
        
        # Terminal leads
        ET.SubElement(g, 'line', {
            'x1': '20', 'y1': '-35',
            'x2': '60', 'y2': '-35',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '20', 'y1': '35',
            'x2': '60', 'y2': '35',
            'class': 'wire'
        })
        
        # Pin labels
        self._add_pin_label(g, -35, -5, "G")
        self._add_pin_label(g, 40, -40, "D")
        self._add_pin_label(g, 40, 40, "S")
        
        comp.ports[0] = (60, -35)  # Drain
        comp.ports[1] = (-60, 0)   # Gate
        comp.ports[2] = (60, 35)   # Source
        if len(comp.nodes) > 3:
            comp.ports[3] = (60, 35)  # Bulk (tied to source)
    
    def _draw_jfet_symbol(self, g: ET.Element, comp: Component):
        """Draw N-channel JFET symbol"""
        # Channel line (vertical)
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': '-25',
            'x2': '0', 'y2': '25',
            'class': 'symbol'
        })
        
        # Gate arrow
        ET.SubElement(g, 'line', {
            'x1': '-25', 'y1': '0',
            'x2': '0', 'y2': '0',
            'class': 'symbol'
        })
        ET.SubElement(g, 'polygon', {
            'points': '-5,0 -12,-4 -12,4',
            'class': 'symbol-filled'
        })
        
        # Terminal leads
        ET.SubElement(g, 'line', {  # Gate
            'x1': '-60', 'y1': '0',
            'x2': '-25', 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {  # Drain
            'x1': '0', 'y1': '-25',
            'x2': '0', 'y2': '-40',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': '-40',
            'x2': '60', 'y2': '-40',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {  # Source
            'x1': '0', 'y1': '25',
            'x2': '0', 'y2': '40',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': '40',
            'x2': '60', 'y2': '40',
            'class': 'wire'
        })
        
        comp.ports[0] = (60, -40)  # Drain
        comp.ports[1] = (-60, 0)   # Gate
        comp.ports[2] = (60, 40)   # Source
    
    def _draw_voltage_source_symbol(self, g: ET.Element, comp: Component):
        """Draw DC/AC voltage source symbol"""
        radius = 20
        
        # Circle
        ET.SubElement(g, 'circle', {
            'cx': '0', 'cy': '0', 'r': str(radius),
            'class': 'symbol'
        })
        
        # Plus and minus signs
        plus = ET.SubElement(g, 'text', {
            'x': '0', 'y': '-5',
            'text-anchor': 'middle',
            'class': 'polarity'
        })
        plus.text = '+'
        
        minus = ET.SubElement(g, 'text', {
            'x': '0', 'y': '12',
            'text-anchor': 'middle',
            'class': 'polarity'
        })
        minus.text = '−'
        
        # Connection leads (top and bottom)
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': str(-radius),
            'x2': '0', 'y2': str(-radius - 25),
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': str(-radius - 25),
            'x2': '60', 'y2': str(-radius - 25),
            'class': 'wire'
        })
        
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': str(radius),
            'x2': '0', 'y2': str(radius + 25),
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': str(radius + 25),
            'x2': '60', 'y2': str(radius + 25),
            'class': 'wire'
        })
        
        comp.ports[0] = (60, -45)  # Positive
        comp.ports[1] = (60, 45)   # Negative
    
    def _draw_current_source_symbol(self, g: ET.Element, comp: Component):
        """Draw current source symbol"""
        radius = 20
        
        # Circle
        ET.SubElement(g, 'circle', {
            'cx': '0', 'cy': '0', 'r': str(radius),
            'class': 'symbol'
        })
        
        # Arrow inside (pointing up)
        ET.SubElement(g, 'line', {
            'x1': '0', 'y1': '12',
            'x2': '0', 'y2': '-12',
            'class': 'symbol'
        })
        ET.SubElement(g, 'polygon', {
            'points': '0,-12 -5,-4 5,-4',
            'class': 'symbol-filled'
        })
        
        # Connection leads
        ET.SubElement(g, 'line', {
            'x1': '-60', 'y1': '0',
            'x2': str(-radius), 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': str(radius), 'y1': '0',
            'x2': '60', 'y2': '0',
            'class': 'wire'
        })
        
        comp.ports[0] = (-60, 0)  # Input
        comp.ports[1] = (60, 0)   # Output
    
    def _draw_generic_symbol(self, g: ET.Element, comp: Component):
        """Draw generic component (box) for unknown types"""
        box_w, box_h = 50, 30
        
        ET.SubElement(g, 'rect', {
            'x': str(-box_w//2),
            'y': str(-box_h//2),
            'width': str(box_w),
            'height': str(box_h),
            'class': 'symbol'
        })
        
        # Connection leads
        ET.SubElement(g, 'line', {
            'x1': '-60', 'y1': '0',
            'x2': str(-box_w//2), 'y2': '0',
            'class': 'wire'
        })
        ET.SubElement(g, 'line', {
            'x1': str(box_w//2), 'y1': '0',
            'x2': '60', 'y2': '0',
            'class': 'wire'
        })
        
        comp.ports[0] = (-60, 0)
        comp.ports[1] = (60, 0)
    
    def _add_pin_label(self, g: ET.Element, x: int, y: int, text: str):
        """Add a pin label"""
        label = ET.SubElement(g, 'text', {
            'x': str(x),
            'y': str(y),
            'class': 'pin-label',
            'text-anchor': 'middle'
        })
        label.text = text
    
    def _add_component_labels(self, g: ET.Element, comp: Component):
        """Add component name and value labels"""
        # Component name (above)
        name_label = ET.SubElement(g, 'text', {
            'x': '0',
            'y': str(-35),
            'text-anchor': 'middle',
            'class': 'comp-name'
        })
        name_label.text = comp.name
        
        # Component value (below)
        value_label = ET.SubElement(g, 'text', {
            'x': '0',
            'y': str(50),
            'text-anchor': 'middle',
            'class': 'comp-value'
        })
        value_label.text = comp.value
    
    def _register_ports(self, comp: Component):
        """Register component port positions for wire routing"""
        for pin_idx, (rel_x, rel_y) in comp.ports.items():
            if pin_idx < len(comp.nodes):
                node = comp.nodes[pin_idx]
                abs_x = comp.x + rel_x
                abs_y = comp.y + rel_y
                self.node_positions[node].append((abs_x, abs_y, comp.name, pin_idx))
    
    def _draw_all_connections(self, wires_group: ET.Element):
        """Draw all wire connections between components"""
        drawn_dots: Set[Tuple[int, int]] = set()
        
        for node, positions in self.node_positions.items():
            if len(positions) < 2:
                continue
            
            # Skip ground node visual clutter (just draw dots)
            is_ground = node.upper() in ['0', 'GND', 'VSS', 'GROUND']
            
            if len(positions) == 2:
                # Direct connection between two points
                (x1, y1, _, _), (x2, y2, _, _) = positions
                self._draw_wire(wires_group, x1, y1, x2, y2)
            else:
                # Multiple connections - use a bus point
                # Find central point
                avg_x = sum(p[0] for p in positions) // len(positions)
                avg_y = sum(p[1] for p in positions) // len(positions)
                
                # Draw wires from each port to the bus point
                for x, y, comp_name, pin_idx in positions:
                    self._draw_wire(wires_group, x, y, avg_x, avg_y)
                
                # Draw connection dot at bus point
                if (avg_x, avg_y) not in drawn_dots:
                    ET.SubElement(wires_group, 'circle', {
                        'cx': str(avg_x),
                        'cy': str(avg_y),
                        'r': str(self.DOT_RADIUS),
                        'class': 'connection-dot'
                    })
                    drawn_dots.add((avg_x, avg_y))
                    
                    # Add node label
                    if not is_ground:
                        label = ET.SubElement(wires_group, 'text', {
                            'x': str(avg_x + 8),
                            'y': str(avg_y - 8),
                            'class': 'node-label'
                        })
                        label.text = node
            
            # Draw connection dots at each endpoint
            for x, y, _, _ in positions:
                if (x, y) not in drawn_dots:
                    if len(positions) > 2:  # Only draw dots for multi-way connections
                        ET.SubElement(wires_group, 'circle', {
                            'cx': str(x),
                            'cy': str(y),
                            'r': str(self.DOT_RADIUS - 1),
                            'class': 'connection-dot'
                        })
                    drawn_dots.add((x, y))
    
    def _draw_wire(self, parent: ET.Element, x1: int, y1: int, x2: int, y2: int):
        """Draw a wire between two points using orthogonal routing"""
        # Use L-shaped routing for cleaner look
        if x1 == x2 or y1 == y2:
            # Direct horizontal or vertical line
            ET.SubElement(parent, 'line', {
                'x1': str(x1), 'y1': str(y1),
                'x2': str(x2), 'y2': str(y2),
                'class': 'wire'
            })
        else:
            # L-shaped routing (horizontal first, then vertical)
            mid_x = (x1 + x2) // 2
            
            path = f"M {x1} {y1} L {mid_x} {y1} L {mid_x} {y2} L {x2} {y2}"
            ET.SubElement(parent, 'path', {
                'd': path,
                'class': 'wire'
            })
    
    def _save_svg(self, root: ET.Element, output_file: str):
        """Save SVG to file with pretty printing"""
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Parse and pretty print
        try:
            dom = minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ")
            # Remove extra blank lines
            lines = [line for line in pretty_xml.split('\n') if line.strip()]
            # Remove XML declaration (optional)
            if lines and lines[0].startswith('<?xml'):
                lines = lines[1:]
            pretty_xml = '\n'.join(lines)
        except Exception:
            pretty_xml = xml_str
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("SPICE to SVG Schematic Generator")
        print("=" * 60)
        print("\nUsage: python spice_to_svg.py <spice_file> [output_file.svg]")
        print("\nSupported components:")
        print("  R - Resistor       (R1 node1 node2 value)")
        print("  C - Capacitor      (C1 node1 node2 value)")
        print("  L - Inductor       (L1 node1 node2 value)")
        print("  D - Diode          (D1 anode cathode model)")
        print("  Q - BJT            (Q1 C B E model)")
        print("  M - MOSFET         (M1 D G S B model)")
        print("  J - JFET           (J1 D G S model)")
        print("  V - Voltage Source (V1 n+ n- DC value)")
        print("  I - Current Source (I1 n+ n- DC value)")
        print("\nExample:")
        print("  python spice_to_svg.py circuit.cir")
        print("  python spice_to_svg.py circuit.cir schematic.svg")
        print("\nExample SPICE file content:")
        print("  Simple RC Filter")
        print("  V1 IN 0 DC 5V")
        print("  R1 IN OUT 10k")
        print("  C1 OUT 0 100n")
        print("  .END")
        sys.exit(0)
    
    spice_file = sys.argv[1]
    
    # Determine output filename
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Replace extension with .svg
        if '.' in spice_file:
            output_file = spice_file.rsplit('.', 1)[0] + '.svg'
        else:
            output_file = spice_file + '.svg'
    
    if not output_file.endswith('.svg'):
        output_file += '.svg'
    
    print(f"\n{'=' * 60}")
    print("SPICE to SVG Schematic Generator")
    print(f"{'=' * 60}")
    print(f"\nInput:  {spice_file}")
    print(f"Output: {output_file}")
    print()
    
    # Parse SPICE file
    parser = SPICEParser(filepath=spice_file)
    components, connections = parser.parse()
    
    if not components:
        print(f"✗ Error: No components found in {spice_file}")
        print("  Make sure the file contains valid SPICE component definitions.")
        sys.exit(1)
    
    print(f"Found {len(components)} components:")
    for name, comp in sorted(components.items()):
        node_str = ', '.join(comp.nodes)
        print(f"  {name:6s} [{comp.type}] {comp.value:12s} nodes: ({node_str})")
    
    print(f"\nFound {len(connections)} unique nodes:")
    for node, conn in sorted(connections.items()):
        comp_list = ', '.join([f"{c[0]}:{c[1]}" for c in conn.components])
        print(f"  {node:10s} → {comp_list}")
    
    print()
    
    # Render schematic
    renderer = SchematicRenderer(components, connections, parser.title)
    renderer.render(output_file)
    
    print(f"\n{'=' * 60}\n")


if __name__ == '__main__':
    main()
