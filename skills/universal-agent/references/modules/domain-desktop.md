# Desktop & Operating-System Automation

## Trigger
Use for authorized desktop app inspection and interaction, including semantic Windows UI Automation.

## Workflow
1. Confirm device, app, user goal, and exact permission scope.
2. Prefer accessibility trees, UI Automation identifiers, and documented APIs over screenshots and coordinate guessing.
3. Begin with read-only snapshots. Do not change display settings, virtual desktops, window positions, overlays, or screen configuration merely to observe.
4. Identify target control and expected result before interaction.
5. Keep observation separate from click/type/submit actions; gate consequential actions with approval.
6. Avoid collecting passwords, private messages, financial records, or unrelated window content.
7. Verify the resulting app state and restore only changes made during the authorized task.
8. Record OS requirements and unsupported controls.

Read-only observation is the default. Do not hide activity, bypass restrictions, or interact with unrelated accounts.
