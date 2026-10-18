# Live Bench test plan

Static Python and DocType tests can run without Frappe, but **do not constitute real integration testing**. When a Frappe Bench v15 evaluation site becomes available, use the following scenarios as release gates.

## Identity and isolation
- Create two stations and three non-admin users (Manager A, Supervisor A, Manager B).
- Station A membership is not sufficient to see Station B data.
- Normal Employee role cannot submit or approve shift reports.
- Supervisor cannot approve; manager assigned to wrong station cannot approve.
- Hidden DocType REST resource requests for station B must fail, not merely disappear from the UI.
- Disabling a station membership blocks access without relying on revoking the Desk role.

## Shift closing
- Missing mandatory fields are rejected.
- Duplicate station/schedule/date reports are rejected.
- Partial save stays Draft.
- Reported sales and expected cash compute accurately.
- Submitted reports cannot be edited outside action endpoints.
- Return with comments is only available for a submitted report.
- Resubmission preserves an audit trail and creates an open approval alert.
- An Approved report rejects edits and deletion.

## Alerts and scheduling
- An hourly scheduler job creates a missing report alert only after the due time + grace period.
- A newly configured schedule doesn't trigger missing reports for dates before its creation.
- A missing alert is resolved by report submission.
- Repeated scheduler invocation does not duplicate alerts.
- Cash variance alerts respect the station threshold.

## Dashboard
- Counts are limited to stations the user may access.
- Today's approved reported sales excludes unapproved reports.
- Alert rows are visible to station managers only.
- All displayed dynamic strings use safe text rendering (not untrusted HTML).

**Run as a System Manager on a disposable test site only.** Record outcomes and screenshots before enabling real business users.
