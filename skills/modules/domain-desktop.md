# Domain Module: Desktop & Operating-System Automation

## Trigger
Use for authorized desktop application inspection and interaction, including Windows UI Automation and accessibility-based workflows.

## Workflow
1. Confirm the target device, application, user goal, and exact permission scope.
2. Prefer semantic accessibility trees, UI Automation identifiers, and documented application APIs over screenshots and coordinate guessing.
3. Begin with read-only snapshots; do not alter display settings, virtual desktops, window positions, overlays, or screen configuration merely to observe.
4. Identify the target control and expected state change before any interaction.
5. Keep observation separate from click/type/submit capabilities; request approval for consequential changes.
6. Avoid capturing passwords, private messages, financial records, or unrelated window content.
7. Verify the resulting application state and restore only changes made during the authorized workflow.
8. Document OS/version requirements, accessibility permissions, and unsupported controls.

## Outputs
A safe, narrowly scoped desktop workflow or a semantic accessibility-based inspection report.

## Boundaries
Do not disable security controls, hide activity, bypass access restrictions, or interact with unrelated accounts. Read-only observation is the default.
