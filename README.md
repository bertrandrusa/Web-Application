# Gas Station MIS — Frappe + ERPNext + Frappe HR

**Status:** MVP starter implementation, **not production-certified**. This branch contains the Frappe app at the Git root, independently of the older Java application on `main`. The repository is still named `Web-Application` because a new repository could not be created through the connected GitHub tool.

## Purpose

A gas station operations app that reuses **ERPNext** for business records and **Frappe HR** for employees, shift types and attendance, while adding station-specific shift close processes.

### Implemented in this starter

- Stations linked to an ERPNext Company
- Station Staff Assignment linked to Frappe users and optionally HRMS Employees
- Station-specific permission checks; membership is administered by System Manager
- Expected shift-end schedules with grace periods
- One shift report per station, schedule and date
- Sales totals, expected closing cash and cash variance calculations
- Draft → Submitted → Approved / Returned workflow with server-side validation
- Approved reports locked from edits
- In-app approval and missing-report alerts; hourly scheduled overdue checks
- Responsive Frappe Desk **Station Dashboard** with current-day metrics
- Basic schema verification tests and setup instructions

### Out of scope

No live POS/pump integration, automatic bank reconciliation, fuel tank control, payroll, SMS, email delivery, multiple currencies per shift, or production-grade finance posting. Shift-close values are **self-reported**, not verified transactions.

## Compatibility

Target **Frappe / ERPNext / HRMS version 15** (matching major-version branches). The app has **not been integration tested against a live Bench** in this delivery. Test in a development site before using business data. Versions 16+ may require adjustments.

## Development installation

Install and configure a working Frappe Bench with **ERPNext** and **HRMS** already installed. Use the same major version for all components, follow official Frappe documentation for infrastructure installation, and back up existing sites before installing apps.

From this standalone Git branch, install the app directly via Bench:

```bash
cd ~/frappe-bench
bench get-app --branch gas-station-mis gas_station_mis \\
  https://github.com/bertrandrusa/Web-Application.git
bench --site your-site.local install-app gas_station_mis
bench --site your-site.local migrate
```

Use a test Bench first, with compatible Frappe 15, ERPNext 15, and HRMS 15 already installed.

For a dedicated repository later, follow `docs/MOVE_TO_OWN_REPOSITORY.md` to copy this branch's root contents into a new `gas-station-mis` repository.

### Configure

1. Create ERPNext **Company** and finish setup (including site timezone and currency; for Kigali use `Africa/Kigali` and RWF if appropriate).
2. Install Frappe HR and configure Employees, Shift Types and Attendance under HRMS.
3. In Desk, as **System Manager**, open **Gas Station**, create a station and choose its Company.
4. Open **Gas Station Staff Assignment**. Assign each System User to a station, with role **Manager**, **Supervisor**, or **Employee**. Assignments automatically grant the base Desk role `Gas Station User`.
5. Open **Gas Station Shift Schedule** and configure e.g. Morning 14:00, Evening 22:00, with reporting grace periods. Times follow the site's configured timezone.
6. A manager/supervisor creates a **Gas Station Shift Report**, saves it as Draft, and uses **Submit for Approval**. A station manager can Approve or Return.
7. Open `/app/station-dashboard` (or search **Station Dashboard** in Desk). Allow Bench scheduler to run for hourly missing-report checks.

### Report cash formula

- `total_sales = cash_sales + mobile_money_sales + card_sales + other_sales`
- `expected_closing_cash = opening_cash + cash_sales - cash_expenses - cash_removed`
- `cash_difference = counted_cash - expected_closing_cash`

All amounts must be nonnegative. A negative *expected closing cash* can indicate an inconsistent report; managers should investigate. These are management figures, **not accounting journal entries**.

### Alert rules

- **Approval Required:** created on submission, resolved when approved or returned.
- **Missing Report:** generated hourly when a configured shift reaches its due time with no submitted/returned/approved report; scans today and yesterday to handle midnight.
- **Cash Variance:** generated at approval when the absolute discrepancy reaches the station threshold, if configured.

Alerts are stored in **Gas Station Alert**. This starter only creates **in-app records**; no emails or SMS are sent.

### Authorization

- Global `Gas Station User` is only a Desk role; **station membership** determines accessible stations.
- Managers can approve/return reports and resolve alerts for their stations.
- Supervisors can create and submit shift reports for their stations.
- Employee-level memberships can view their station only; permissions for HRMS Employee/Attendance remain governed by HRMS.
- **System Manager** administers memberships.
- All dashboard selectors and workflow API calls validate membership server-side.
- Direct changes to approved reports or status fields are rejected by the DocType controller.

For larger deployments, consider separate site tenants per business owner, stronger segregated duties, scheduled backups with restore tests, and independent security review.

## Local static validation

```bash
python -m compileall -q gas_station_mis
python -m unittest discover -s gas_station_mis/tests -p 'test_*.py'
```

These tests validate metadata only. Run live Bench integration tests for permissions and workflows before production.

## Roadmap

- [ ] Validate migrations and screens on a Frappe 15 + ERPNext 15 + HRMS 15 test site
- [ ] Comprehensive station-isolation and workflow integration tests
- [ ] Link actual HRMS shift assignments/attendance to schedules and reports
- [ ] Email alert delivery and configurable alert rules
- [ ] Inventory and POS integration with safe, idempotent synchronization
- [ ] Cash corrections, documented approvals and immutable business ledger
- [ ] CI, security scans, monitored backup/restore and production deployment

## License

MIT for this custom app code (see LICENSE). The ERPNext and HRMS upstream projects have **their own licenses**; installing this app does not change those obligations.
