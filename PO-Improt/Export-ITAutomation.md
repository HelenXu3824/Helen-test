# IT Automation Export/Import (Excel Templates) — PO Summary (2026-03-22)

## Output Type Declaration (Required)
- Requirement Analysis (Business requirements in English)
- Feature Description (English)
- UI/UX Design Specifications (English)
- Acceptance Criteria
- Export/Import Template Design (Excel)
- User Story Decomposition (per PO.md constraints)
- Release Notes

---

## 0. Key Decisions (Final)
1. **Template format**: Excel (`.xlsx`) for both export and import.
2. **Parameters**: **Fixed columns as primary interface + limited fallback free-text** via `extra_params`.
3. **Duplicate naming on import**: If `automation_name` conflicts, the system **auto-appends suffixes** to generate a unique name.
   - Recommended rule: `{name} (Imported)`, then `{name} (Imported) (2)`, `(3)`… until unique.
4. **Execute Script**: Template exports **script reference only** (no script body/content). Import requires **mapping** the script reference to the destination site’s script repository.
5. **Non-negotiable constraint**: **No cross-server references**. All mapped assets/objects must belong to the **current server context**.

---

## 1. Requirement Analysis — Business Requirements (English)

### 1. Business Context
BLSS is a large-scale platform whose **IT Automation** module enables SMBs to monitor, manage, and control power/environmental devices across physical and virtual IT environments. The module supports **Linux Servers, Windows Servers, VMware ESX/ESXi, VMware vCenter, and Microsoft SCVMM**.

IT Automation provides:
- **Automation Wizard** (guided, user-friendly)
- **Advanced Custom Actions** (power-user capability)

Customers define an **Automation** with:
- **Triggers**: power issue, environment issue, custom trigger, schedule timer, manual run.
- **Actions**: Send Message, Execute Script, IT Action command, Recovery, Timer, Hardware actions, If/Else.

A critical operational constraint:
- An Automation may be distributed to multiple servers, but each server instance contains only devices managed by that server.
- **Cross-server device references are not supported and must be prevented.**

### 2. Business Problem
Lack of standardized export/import for IT Automation results in:
- High replication cost across sites/servers
- Increased operational risk due to manual reconfiguration
- Limited scalability for multi-site rollouts and MSP delivery
- Inconsistent governance and policy baselines

### 3. Target Users / Stakeholders
- IT Administrators / Site Operators
- Implementation / Deployment Engineers
- Managed Service Providers (MSPs)

### 4. User Needs (Jobs-to-be-Done)
- Portability of proven automation policies
- Bulk creation via templates
- Readability and editability (Excel preferred)
- Safe re-binding via reference mapping
- Enforce server-local bindings (no cross-server)

### 5. Business Outcomes / Success Criteria
- Reduce rollout time to “import + map + confirm”
- Improve consistency and reduce errors
- Enable scalable delivery for multi-site customers and MSPs
- Maintain wizard-like guided experience with auditable steps

### 6. Scope
**In Scope**: requirements, functional definition, UX flow, acceptance criteria, release notes, Excel template design.

**Out of Scope**: technical architecture, implementation, database design.

### 7. Constraints and Non-negotiables
- Server-scoped bindings only (block cross-server)
- Execute Script reference-only export/import mapping
- Duplicate naming handled via auto-suffixing

### 8. Explicit Assumptions
- Destination environment has discoverable inventory and script repository
- Import primarily creates **new** automations (no overwrite in MVP)

---

## 2. Feature Description (English)

### Feature Name
**IT Automation Export/Import via Excel Templates (Portable & Bulk Provisioning)**

### 2.1 Overview
This feature enables administrators to export an existing IT Automation definition into an Excel template and import it into another site/server context to migrate or bulk-create automations.

### 2.2 Key Capabilities
- Export automation to `.xlsx` with normalized Triggers/Actions and centralized References.
- Import `.xlsx` via guided workflow: upload → validate → map references → confirm & create.
- Reference-based portability using `ref_key` and References mapping.

### 2.3 Non-negotiable Constraints
- No cross-server bindings.
- Execute Script exports references only; must map to destination script repository.
- Duplicate names auto-suffixed (no hard block).

### 2.4 Template Principles
- Fixed columns for common parameters (readable, Excel-friendly, precise validation).
- `extra_params` fallback (`key=value;key2=value2`) with allow-list validation.

---

## 3. UI/UX Design Specifications (English)

### 3.1 UX Goals
- Wizard-like simplicity
- High clarity and actionable errors
- Excel-native bulk workflow
- Safety guardrails and auditable mapping

### 3.2 Entry Points
- Automation Detail: **Export (Excel)**
- Automations List: **Import (Excel)**

### 3.3 Export UX
- Export modal with summary, editable filename, and note: “Execute Script exports references only.”
- Success toast and automatic download.

### 3.4 Import Wizard
**Step 1: Upload** — Accept `.xlsx` only.

**Step 2: Validate** — Show errors/warnings with precise location: `Sheet!RowColumn (field)`.
- Errors block Next.

**Step 3: Map References** — Table with filters (Assets/Scripts/Notification targets).
- Auto-match button; confidence indicators.
- Script mapping required when referenced.
- Cross-server selection triggers blocking error.

**Step 4: Confirm & Create**
- Show final resolved name (after auto-suffix).
- Create Automation.
- Success page with “Go to Automation” and “Import another template”.

### 3.5 Required States
- Empty states: no scripts/assets available.
- Blocking errors: invalid template, unmapped required references, cross-server mappings.
- Warnings: low-confidence auto-match.

---

## 4. Export/Import Template Design (Excel)

### 4.1 Workbook Sheets
1. README
2. Automation
3. References
4. Triggers
5. Actions

### 4.2 README Sheet
Columns: `key`, `value`.
Required keys: `template_type`, `template_version`, `generated_at_utc`, `source_automation_name`, `notes`.

### 4.3 Automation Sheet
Columns:
- `automation_name` (required)
- `description`
- `trigger_logic` (required: AND/OR)
- `enabled` (required: TRUE/FALSE)

### 4.4 References Sheet
Columns:
- `ref_key` (required, unique)
- `ref_type` (required: asset/notification_target/script/it_object)
- `source_display_name` (required)
- `source_type_hint`
- `source_unique_hint_1`
- `source_unique_hint_2`
- `mapping_mode` (required: AUTO/MANUAL)
- `target_lookup_type` (name/ip/uuid/serial)
- `target_lookup_value`
- `mapping_required` (required: TRUE/FALSE)

### 4.5 Triggers Sheet
Columns:
- `trigger_id` (required)
- `trigger_type` (required: power_issue/environment_issue/custom/schedule_timer/manual_run)
- `condition_name`
- `asset_ref_key`
- `comparator`
- `threshold`
- `schedule_cron`
- `enabled` (required)

### 4.6 Actions Sheet
Common columns:
- `action_id` (required)
- `parent_action_id`
- `branch` (THEN/ELSE)
- `sequence` (required)
- `action_type` (required)
- `on_error` (continue/stop)
- `extra_params`

Fixed columns by type:
- Timer: `timer_seconds`
- Send Message: `message_target_ref_key`, `message_subject`, `message_body`
- Execute Script (reference only): `script_ref_key`, `script_args`
- If/Else: `if_left`, `if_operator`, `if_right`, `if_asset_ref_key`
- IT Action (placeholder): `it_action_command`, `it_target_ref_key`

---

## 5. Acceptance Criteria (High-Level)
- Export downloads a valid `.xlsx` with required sheets and headers.
- Import validates structure and cell-level errors with actionable locations.
- Required references must be mapped; unmapped required references block creation.
- Execute Script requires script reference mapping; no script content is exported.
- Cross-server mappings are blocked.
- Duplicate automation names are auto-suffixed and shown in Confirm step.

---

## 6. User Story Decomposition (per PO.md sizing principles)
> Stories are decomposed to be independently deliverable and verifiable; target ~2 points and ≤800 lines of net production code per story.

1. Add Import/Export entry points with permission gating.
2. Export Excel skeleton with 5 sheets + headers + template version.
3. Export Automation metadata to Automation sheet.
4. Export Triggers to Triggers sheet (fixed columns).
5. Export Actions for Timer/Send Message + extra_params.
6. Export If/Else hierarchy (parent_action_id/branch/sequence).
7. Export Execute Script reference only + References rows.
8. Import Step 1 (Upload) + structure/header validation.
9. Import Step 2 (Row parsing) + fixed-column validation + ref_key integrity checks.
10. Import Step 3 (Reference mapping UI) including script mapping.
11. Import Create New + duplicate name auto-suffixing and final-name preview.
12. Enforce no cross-server references (blocking rule).

---

## 7. Release Notes (Draft)
- Added IT Automation **Export/Import via Excel templates** to support cross-site portability and bulk provisioning.
- Import includes guided validation and **reference mapping** to local assets/scripts/notification targets.
- Execute Script templates export **script references only** (no script content).
- Import automatically resolves name conflicts by generating a unique automation name.