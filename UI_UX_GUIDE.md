# UI/UX DESIGN SYSTEM & GUIDE — TERRAWATCH 360

## 1. Visual Language & Philosophy
TerraWatch 360 represents an Earth Observation Intelligence Command Center.
The aesthetic is high-tech, tactical, clean, and distraction-free:
- Deep-space backgrounds and dark charcoal glassmorphism.
- Neon-accented indicators with scientific restraint.
- Crisp typography and high-contrast analytical map overlays.

---

## 2. Design Tokens & Color Palette

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| `--bg-space-dark` | `#07111F` | Deep space root canvas |
| `--bg-panel` | `#0B1728` | Sidebar, headers, and container background |
| `--bg-card` | `#102238` | Interactive cards, modal dialogs, and stat boxes |
| `--border-subtle` | `#1E3A5F` | Clean boundary lines and panel dividers |
| `--accent-river` | `#38BDF8` | RiverWatch module highlight (Sky/Cyan) |
| `--accent-wetland` | `#2DD4BF` | WetlandWatch module highlight (Teal) |
| `--accent-forest` | `#10B981` | ForestGuard module highlight (Emerald) |
| `--accent-urban` | `#818CF8` | UrbanWatch module highlight (Indigo/Violet) |
| `--alert-caution` | `#F59E0B` | Spectral disturbance requiring investigation (Amber) |
| `--alert-critical` | `#EF4444` | High-confidence disturbance alert (Rose/Red) |
| `--text-primary` | `#E5F0FA` | Primary headings, values, and alerts |
| `--text-secondary`| `#91A4B8` | Subtitles, labels, and metadata |

---

## 3. Key Components
1. **Mission Control Top Navigation**:
   - Platform branding with orbital emblem.
   - 4-module direct navigation switchers with dedicated accent badges.
   - Provider connectivity pulse indicators (Copernicus / Bhoonidhi status).
2. **Interactive GIS Canvas**:
   - Leaflet / MapLibre map with dark satellite/topographic basemap options.
   - Interactive split-screen swipe slider to visually drag before vs. after raster layers.
   - Dynamic scientific legend adapting to active module layers.
3. **Temporal Analysis Drawer**:
   - Timeline slider for historical observation selection.
   - Area trend charts (Recharts) displaying monthly/seasonal changes.
   - Actionable alert list with inspection zoom buttons.
