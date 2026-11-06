# Domain Module: Mobile Development

## Trigger
Use for Android/iOS application architecture, mobile UI, Flutter, React Native, native APIs, packaging, permissions, and mobile testing.

## Workflow
1. Inspect framework, app structure, minimum OS version, signing/build pipeline, and supported devices.
2. Define navigation, user states, offline behavior, permissions, notifications, and data storage.
3. Request permissions contextually and only when the feature needs them; explain why and provide graceful denial paths.
4. Keep secrets and sensitive data off the client; use authenticated backend APIs and secure platform storage.
5. Design for lifecycle changes, poor network, retries, battery, accessibility, and device-size differences.
6. Add unit, integration, UI, permission, and upgrade/migration tests.
7. Verify build variants, signing configuration, manifest entitlements, and release artifacts.
8. Document device/OS requirements and store policy constraints.

## Outputs
Mobile implementation or architecture with tested permissions, lifecycle behavior, and build evidence.

## Boundaries
Do not bypass platform permission dialogs or hide sensitive collection. Do not commit signing keys, keystores, or provisioning secrets.
