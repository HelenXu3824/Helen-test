# BLSS Report Platform — Architecture Diagram

The BLSS Report Platform enables non-developer users to design, publish, and consume customer-specific reports through a self-service designer built on the existing Dashboard module. It is delivered by the BLSS ART Tiger Team in PI12 and spans a web client, a Java-based report service, and a PostgreSQL data layer — all containerised and governed by shared observability and security controls.

---

## Architecture Diagram

```mermaid
flowchart TD
    %% ─────────────────────────────────────────────────────
    %%  FRONTEND LAYER
    %% ─────────────────────────────────────────────────────
    subgraph FE["Frontend Layer"]
        WC["Web Client\n(Dashboard & Report Builder)\n───────────────────────\n• TypeScript framework\n  (Vue / React / Angular)\n• Drag-and-drop layout\n• Visualization components\n  (Apache ECharts – front-end)"]
    end

    %% ─────────────────────────────────────────────────────
    %%  BACKEND / REPORT SERVICE LAYER
    %% ─────────────────────────────────────────────────────
    subgraph BE["Backend / Report Service Layer"]
        RP["Apache Tomcat\n/ Reverse Proxy"]

        subgraph JRS["Java Report Service Container (Spring)"]
            CTL["Controller\n───────────\n• Input & param validation\n• Tenant / User context injection"]
            SVC["Service Layer\n───────────────────────\n• Reporting business logic\n• Granularity selection\n  (AUTO: hour / day / month)\n• DataSource decision\n  (aggregated vs. raw)"]
            TSE["TimeSeries Engine\n───────────────────────\n• Time-bucket alignment\n• abscissaValues / values\n  array alignment"]
            DAO["DAO Layer\n───────────────────────\n• Query aggregated_data_table\n  (default)\n• Query raw_data_table\n  (detail export / debug)\n• Tenant scoping &\n  dimension auth enforcement"]
            OUT["Report Output\n───────────────────────\n• Apache ECharts → PNG / JPEG\n• Apache PDFBox → PDF\n• Apache POI → Excel"]
        end

        RP -->|Forward API requests| CTL
        CTL --> SVC
        SVC --> TSE
        TSE --> DAO
        SVC --> OUT
    end

    %% ─────────────────────────────────────────────────────
    %%  DATA LAYER
    %% ─────────────────────────────────────────────────────
    subgraph DL["Data Layer"]
        PGM["PostgreSQL Master Gateway\n(Single logical entry point — HA)"]

        subgraph SN["PostgreSQL Shard Nodes (Optional)"]
            SH["Shard Node(s)\n───────────────────────\n• Sharding: device ID / sdb_id\n• Time-based partitioning"]
        end

        subgraph DS["Datasets & Tables"]
            ADS["ADS-layer System-wide Dataset\n───────────────────────\n• Fixed monitor attributes table\n• Energy consumption attributes table\n  (reserved columns, auto-discovery)"]
            AGG["aggregated_data_table\n───────────────────────\n• Hour / Day / Month aggregation\n• Default dataSource for\n  dashboards & reports"]
            RAW["raw_data_table\n───────────────────────\n• Detailed time-series data\n• Used for detail export & debug"]
        end

        ETL["ETL\n(blss-telegraf container)\n───────────────────────\n• Extract from source systems\n• Transform / aggregate\n• Load → ADS dataset &\n  aggregated_data_table"]

        PGM -->|FDW| SH
        PGM --- ADS
        PGM --- AGG
        PGM --- RAW
    end

    %% ─────────────────────────────────────────────────────
    %%  INFRASTRUCTURE / CROSS-CUTTING
    %% ─────────────────────────────────────────────────────
    subgraph INFRA["Infrastructure & Cross-cutting Concerns"]
        direction LR
        OBS["Observability\n───────────────\n• p50 / p95 latency\n• Error rate\n• DAO duration"]
        SEC["Security\n───────────────\n• Tenant isolation (DAO)\n• Dimension ID auth\n• SQL errors not\n  exposed to client"]
        PERF["Performance & Caching\n───────────────\n• Default: aggregated table\n• Short TTL cache for\n  hot ranges (Today / Yesterday)"]
    end

    %% ─────────────────────────────────────────────────────
    %%  KEY DATA FLOWS
    %% ─────────────────────────────────────────────────────
    WC -->|"① REST API calls"| RP
    DAO -->|"② SQL queries (default: aggregated)"| PGM
    DAO -.->|"② SQL / FDW queries (shard access)"| SH
    ETL -->|"③ Source systems → ETL → datasets"| ADS
    ETL --> AGG

    %% Infra annotations (logical association, not physical arrows)
    INFRA -.->|"applied to all layers"| FE
    INFRA -.-> BE
    INFRA -.-> DL
```

---

## Legend & Notes

| Symbol | Meaning |
|--------|---------|
| Solid arrow `→` | Primary data / request flow |
| Dashed arrow `-.->` | Optional path or cross-cutting association |
| `①` REST API calls | HTTP/HTTPS requests from the Web Client to the Reverse Proxy / Report Service |
| `②` SQL / FDW queries | DAO queries to PostgreSQL Master; FDW-forwarded queries to optional shard nodes |
| `③` ETL flow | blss-telegraf container extracts from source systems, transforms, and writes to ADS-layer datasets and aggregated tables |

### Optional Components
- **PostgreSQL Shard Nodes** — deployed only when data volume or multi-tenancy requires horizontal partitioning; accessed by the Master Gateway via Foreign Data Wrapper (FDW).
- **Report Output sub-modules** (PDFBox / POI) — invoked only on explicit export actions (PDF / Excel); Apache ECharts image generation is also used for scheduled report previews.

### Key Design Decisions
- The DAO Layer enforces **tenant isolation and dimension-level authorisation** at query time; SQL error details are never surfaced to the client.
- The Service Layer applies an **AUTO granularity strategy** (hour → day → month) based on the requested time range, defaulting queries to `aggregated_data_table` for performance.
- A **short-TTL cache** covers hot time ranges (Today / Yesterday) to reduce database load on frequent dashboard refreshes.
- All runtime components (Frontend, Java Report Service, blss-telegraf ETL, PostgreSQL) are deployed as **Docker containers** to ensure consistent environments across stages.
