# Figma Page: BLSS Report Platform — Architecture

> **Document type:** Design Handoff / Figma Setup Guide  
> **Audience:** UX Designer, Product Owner, Tech Lead  
> **Status:** Ready for Designer Replication  
> **Last updated:** 2026-04-08  
> **Linked Confluence page / Jira Epic:** _(add link)_

---

## 1. Proposed Figma Page Name

```
BLSS Report Platform — Architecture
```

> Suggested location: inside the existing **BLSS Design System** Figma project, as a new **Page** (not a new File).  
> If no shared project exists yet, create a new Figma file named **"BLSS Report Platform"** and make this the first page.

---

## 2. Frame Structure

Create the following **top-level Frames** on the page, arranged **left → right** with **80 px gap** between frames.

| # | Frame Name | Width × Height | Purpose |
|---|---|---|---|
| 1 | `Overview` | 1440 × 900 | High-level summary card: project context, PI, scope |
| 2 | `Architecture Diagram` | 1920 × 1080 | Full 3-layer + infra diagram (Mermaid render or Figma redrawn) |
| 3 | `Legend` | 600 × 900 | Color codes, shape meanings, line/arrow types |
| 4 | `Cross-cutting Concerns` | 1440 × 900 | Security, Observability, Performance/Caching callout cards |

### 2.1 Frame 1 — Overview

```
Frame: Overview  (1440 × 900, background: #F8F9FA)
├── Section header text: "BLSS Report Platform — PI12"
├── Sub-header: "Architecture Reference · Tiger Team"
├── Card group: "Scope" (3 cards side-by-side)
│   ├── Card: In Scope  → Feature list (see Section 4 of design doc)
│   ├── Card: Out of Scope → e.g., DB schema, code impl
│   └── Card: Key Stakeholders → PO / Tiger Team / ART
└── Footer: Last updated date · Version tag
```

### 2.2 Frame 2 — Architecture Diagram

```
Frame: Architecture Diagram  (1920 × 1080, background: #FFFFFF)
├── Title bar (top, full-width strip, #1B2A4A): "BLSS Report Platform — System Architecture"
├── Row 1 — Frontend Layer (background swatch: #E3F2FD)
│   └── Component box: "Web Client (Dashboard & Report Builder)"
│       ├── Sub-label: Vue / React / Angular (TypeScript)
│       ├── Sub-label: Drag-and-drop Layout
│       └── Sub-label: Visualization Components (ECharts)
├── Arrow ↓ label: "REST API Calls"
├── Row 2 — Backend / Report Service Layer (background swatch: #E8F5E9)
│   ├── Box: "Apache Tomcat / Reverse Proxy"
│   │   └── Arrow → "Forward API Requests"
│   └── Box: "Java Report Service Container (Spring)"
│       ├── Sub-box: Controller  (Input validation · Tenant/User context)
│       ├── Sub-box: Service Layer  (Granularity selection · DataSource decision)
│       ├── Sub-box: TimeSeries Engine  (Bucket alignment · Array alignment)
│       ├── Sub-box: DAO Layer  (aggregated · raw · tenant scoping)
│       └── Sub-box: Report Output  (EChart→PNG · PDFBox→PDF · POI→Excel)
├── Arrow ↓ label: "SQL / FDW Queries"
├── Row 3 — Data Layer (background swatch: #FFF8E1)
│   ├── Box: "PostgreSQL Master Gateway"  (Single logical entry · HA)
│   │   └── Arrow → "FDW" → "PostgreSQL Shard Nodes (Optional)"
│   ├── Box: "Datasets & Tables"
│   │   ├── Sub-box: ADS-layer System-wide Dataset
│   │   ├── Sub-box: aggregated_data_table  (hour/day/month)
│   │   └── Sub-box: raw_data_table  (detail · debug)
│   └── Box: "ETL — blss-telegraf container"
│       └── Arrow: Source Systems → ETL → ADS + aggregated tables
└── Row 4 — Infrastructure strip (background swatch: #F3E5F5)
    └── Docker container badges (one per component):
        Frontend · Java Report Service · blss-telegraf · PostgreSQL cluster
```

### 2.3 Frame 3 — Legend

```
Frame: Legend  (600 × 900, background: #FAFAFA)
├── Title: "Legend"
├── Shape key
│   ├── Rectangle with rounded corners → Service / Container
│   ├── Rectangle (sharp corners) → Data table / Dataset
│   ├── Cylinder shape (or icon) → Database node
│   └── Diamond → Decision point (granularity / dataSource)
├── Color key (Layer colors)
│   ├── #E3F2FD — Frontend Layer
│   ├── #E8F5E9 — Backend / Service Layer
│   ├── #FFF8E1 — Data Layer
│   └── #F3E5F5 — Infrastructure / Cross-cutting
├── Arrow key
│   ├── Solid → → Synchronous call / data flow
│   ├── Dashed --> → Async / ETL / FDW
│   └── Bold → → Critical path (report query)
└── Icon key (if icons used)
    ├── 🔒  Security boundary
    ├── 📊  Observability / Metrics
    └── ⚡  Caching / Performance
```

### 2.4 Frame 4 — Cross-cutting Concerns

```
Frame: Cross-cutting Concerns  (1440 × 900, background: #F8F9FA)
├── Title: "Cross-cutting Concerns"
├── Card: Security
│   ├── DAO-layer tenant isolation
│   ├── Dimension ID authorization check
│   └── SQL errors not exposed to client
├── Card: Observability
│   ├── p50 / p95 latency
│   ├── Error rate
│   └── DAO query duration
└── Card: Performance & Caching
    ├── Default query: aggregated_data_table
    └── Short TTL cache for Today / Yesterday ranges
```

---

## 3. Auto-layout & Spacing Settings

| Element | Setting |
|---|---|
| Page canvas background | `#F0F2F5` |
| Frame padding (inner) | `48 px` all sides |
| Gap between sub-boxes inside a layer row | `24 px` |
| Gap between layer rows (vertical) | `48 px` |
| Arrow label font | Inter · 12 px · `#616161` |
| Section title (layer label) | Inter · 16 px · Bold · `#37474F` |
| Box border | `1 px solid #CFD8DC`, radius `8 px` |
| Box shadow | `0 2px 8px rgba(0,0,0,0.08)` |

---

## 4. Typography

| Role | Font | Size | Weight | Color |
|---|---|---|---|---|
| Page title (title bar) | Inter | 24 px | Bold | `#FFFFFF` |
| Frame section heading | Inter | 20 px | SemiBold | `#1B2A4A` |
| Box primary label | Inter | 14 px | SemiBold | `#212121` |
| Box sub-label / annotation | Inter | 12 px | Regular | `#616161` |
| Arrow / connector label | Inter | 11 px | Regular | `#9E9E9E` |
| Legend label | Inter | 13 px | Regular | `#424242` |

> **Fallback font stack:** `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

---

## 5. Color Palette

| Token name | Hex | Usage |
|---|---|---|
| `layer-frontend` | `#E3F2FD` | Frontend layer background |
| `layer-backend` | `#E8F5E9` | Backend / Service layer background |
| `layer-data` | `#FFF8E1` | Data layer background |
| `layer-infra` | `#F3E5F5` | Infrastructure / cross-cutting strip |
| `title-bar` | `#1B2A4A` | Title bar fill, primary heading |
| `box-border` | `#CFD8DC` | All component box borders |
| `arrow-line` | `#90A4AE` | Connector / arrow stroke |
| `text-primary` | `#212121` | Box labels, body text |
| `text-secondary` | `#616161` | Sub-labels, annotations |
| `text-muted` | `#9E9E9E` | Arrow labels, helper text |
| `page-canvas` | `#F0F2F5` | Figma page background |
| `card-white` | `#FFFFFF` | Component box fill |

---

## 6. Paste-ready Mermaid Diagram

Copy the block below into any Mermaid-compatible renderer (e.g., [mermaid.live](https://mermaid.live), Confluence, GitLab, GitHub) to generate a PNG/SVG export for the **Architecture Diagram** frame.

````mermaid
graph TD
  subgraph FE["Frontend Layer"]
    WC["Web Client\n(Dashboard & Report Builder)\nVue/React/Angular · TypeScript\nDrag-and-drop Layout\nVisualization Components (ECharts)"]
  end

  subgraph BE["Backend / Report Service Layer"]
    AT["Apache Tomcat\n/ Reverse Proxy"]
    subgraph JRS["Java Report Service Container (Spring)"]
      CTL["Controller\nInput validation\nTenant/User context injection"]
      SVC["Service Layer\nGranularity selection (AUTO: hour/day/month)\nDataSource decision (aggregated vs raw)"]
      TSE["TimeSeries Engine\nTime bucket alignment (timezone-aware)\nabscissaValues & values array alignment"]
      DAO["DAO Layer\nQuery aggregated tables (default)\nQuery raw tables (detail export / debug)\nTenant scoping & dimension auth"]
      RPT["Report Output\nEChart → PNG/JPEG\nPDFBox → PDF\nApache POI → Excel"]
    end
    AT --> CTL
    CTL --> SVC
    SVC --> TSE
    TSE --> DAO
    DAO --> RPT
  end

  subgraph DL["Data Layer"]
    PG["PostgreSQL Master Gateway\nSingle logical entry · HA"]
    SH["PostgreSQL Shard Nodes (Optional)\nSharding: device ID / sdb_id\nTime-based partitioning"]
    subgraph DS["Datasets & Tables"]
      ADS["ADS-layer System-wide Dataset\nSystem fixed attributes table\nEnergy consumption attributes table"]
      AGG["aggregated_data_table\nhour / day / month aggregation\nDefault for dashboards & reports"]
      RAW["raw_data_table\nDetailed time-series data\nUsed for exports & debugging"]
    end
    ETL["ETL — blss-telegraf container\nExtract from source systems\nTransform & aggregate\nLoad into ADS + aggregated tables"]
    PG -->|FDW| SH
    PG --> ADS
    PG --> AGG
    PG --> RAW
    ETL -->|writes| ADS
    ETL -->|writes| AGG
  end

  subgraph INFRA["Infrastructure (Docker-based)"]
    D1["Frontend container"]
    D2["Java Report Service container"]
    D3["blss-telegraf (ETL) container"]
    D4["PostgreSQL containers / cluster"]
  end

  WC -->|REST API Calls| AT
  DAO -->|SQL / FDW Queries| PG

  style FE fill:#E3F2FD,stroke:#90CAF9
  style BE fill:#E8F5E9,stroke:#A5D6A7
  style DL fill:#FFF8E1,stroke:#FFE082
  style INFRA fill:#F3E5F5,stroke:#CE93D8
  style JRS fill:#F1F8E9,stroke:#C5E1A5
  style DS fill:#FFFDE7,stroke:#FFF176
````

---

## 7. Exported Image Placeholder

Once the diagram is rendered and exported from Mermaid Live or Figma, embed it here:

```
[IMAGE PLACEHOLDER]
File name: blss-report-platform-architecture-diagram.png
Resolution: 2x (1920 × 1080 px minimum)
Format: PNG (preferred) or SVG
Export from: Figma Frame "Architecture Diagram" → Export → 2x PNG
             OR mermaid.live → Download PNG/SVG
Alt text: "BLSS Report Platform three-layer architecture diagram showing Frontend, Backend, and Data layers with infrastructure overlay."
```

> **To insert in Figma:** Use **Place image** (Ctrl+Shift+K / ⌘+Shift+K) and drop into the `Architecture Diagram` frame. Scale to fit the inner canvas area (subtract 48 px padding on all sides).

---

## 8. Designer Checklist

Use this checklist when replicating the structure in Figma.

### Page Setup
- [ ] Create a new Figma page named **"BLSS Report Platform — Architecture"**
- [ ] Set canvas background to `#F0F2F5`
- [ ] Add page thumbnail (screenshot of Architecture Diagram frame)

### Frame Creation
- [ ] Create Frame 1: **Overview** (1440 × 900)
- [ ] Create Frame 2: **Architecture Diagram** (1920 × 1080)
- [ ] Create Frame 3: **Legend** (600 × 900)
- [ ] Create Frame 4: **Cross-cutting Concerns** (1440 × 900)
- [ ] Arrange frames left → right with 80 px horizontal gap

### Architecture Diagram Frame
- [ ] Add title bar strip (full width, fill `#1B2A4A`, height 56 px)
- [ ] Create layer row containers (Frontend / Backend / Data / Infra) with correct background fills
- [ ] Add component boxes per **Section 2.2** using rounded rectangle (radius 8 px)
- [ ] Add connector arrows (solid for sync, dashed for async/FDW)
- [ ] Label all arrows (font: Inter 11 px `#9E9E9E`)
- [ ] Insert Mermaid-rendered diagram image as a reference layer (locked, 50% opacity) OR redraw natively
- [ ] Export frame at 2× PNG: `blss-report-platform-architecture-diagram.png`

### Legend Frame
- [ ] Add shape samples with labels for each shape type
- [ ] Add color swatches with hex values for all layer colors
- [ ] Add arrow samples (solid / dashed / bold)
- [ ] Add icon samples if icons are used

### Cross-cutting Concerns Frame
- [ ] Add Security card with 3 bullet points
- [ ] Add Observability card with 3 bullet points
- [ ] Add Performance & Caching card with 2 bullet points
- [ ] Apply consistent card style: white fill, `#CFD8DC` border, 8 px radius, shadow

### Typography & Spacing
- [ ] Verify all text uses **Inter** (install from Google Fonts if not already in team library)
- [ ] Apply typography tokens from **Section 4** to all text layers
- [ ] Set auto-layout padding to 48 px on all top-level frames
- [ ] Set sub-box gap to 24 px, layer row gap to 48 px

### Review & Handoff
- [ ] Share the Figma page link with PO and Tech Lead for sign-off
- [ ] Add Figma link to the Confluence Architecture page
- [ ] Add Figma link to the relevant Jira Epic
- [ ] Set page status to **"Ready for Review"** in Figma (use cover page label or page description)
- [ ] Archive or mark as **Draft** any earlier ad-hoc sketches

---

## 9. Useful Links

| Resource | URL |
|---|---|
| Mermaid Live Editor | https://mermaid.live |
| Inter font (Google Fonts) | https://fonts.google.com/specimen/Inter |
| Figma — Place Image shortcut | Ctrl+Shift+K (Win) · ⌘+Shift+K (Mac) |
| Figma — Auto Layout docs | https://help.figma.com/hc/en-us/articles/5731482952599 |
| Figma — Export docs | https://help.figma.com/hc/en-us/articles/360040028114 |

---

*This document was generated as a Figma-ready design specification for the BLSS Report Platform Architecture (PI12). All structural decisions, color tokens, and typography settings must be validated with the BLSS Design System lead before final handoff.*
