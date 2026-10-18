# Gas Station MIS — Deployment playbook

**Deployment state:** The GitHub source branch is prepared, but no cloud server or production site has been provisioned by this project. Never assume the code has passed Bench integration tests just because offline CI is green.

## Preferred development platform

- Ubuntu / WSL2 or the supported Frappe Docker development environment
- Frappe Framework **version-15**
- ERPNext **version-15**
- Frappe HR (app: `hrms`) **version-15**
- MariaDB, Redis and Node versions consistent with the pinned upstream Frappe v15 instructions
- Frappe Bench (local or inside official dev container)

Read upstream docs: https://docs.frappe.io/framework/v15/user/en/tutorial and https://github.com/frappe/frappe_docker

## Bootstrap a local evaluation site

1. Prepare a **fresh** Frappe v15 Bench with MariaDB and Redis (never against production initially).
2. Install matching ERPNext and HRMS apps and create a site.
3. Clone this temporary feature branch (the project folder is nested within the original repository):

```bash
git clone --single-branch --branch feature/gas-station-mis-frappe-mvp \
    https://github.com/bertrandrusa/Web-Application.git
cp -R Web-Application/gas_station_mis_project \
    ~/frappe-bench/apps/gas_station_mis
cd ~/frappe-bench
bench pip install -e apps/gas_station_mis
bench --site your-site.localhost install-app gas_station_mis
bench --site your-site.localhost migrate
bench --site your-site.localhost clear-cache
```

Note: clone inside **your own** machine. The commands above are instructions, not steps already executed.

## Smoke tests — required for release

- [ ] ERPNext, HRMS, and this custom app install without schema/migration errors
- [ ] System Manager creates a Company, Station, and shift schedule
- [ ] Create two users, two station memberships, and a manager for station A
- [ ] A supervisor can draft, save, submit a station A report
- [ ] A station A manager can return a submitted report with a reason
- [ ] The supervisor can revise and resubmit the returned report
- [ ] The manager can approve, and the approved report cannot be edited or deleted
- [ ] A supervisor **cannot** approve their own report
- [ ] A user at station B **cannot** read, create, view alerts, or approve station A records
- [ ] A user with **no** station memberships cannot see dashboard station data
- [ ] New report submission creates a single open approval alert
- [ ] Returned/resubmitted reports reopen the relevant approval alert
- [ ] Overdue reports create one missing-report alert even if the scheduler retries
- [ ] Cash variance thresholds behave correctly
- [ ] End-of-day and across-midnight deadline behavior is correct
- [ ] RWF currency display, site timezone and accounting company are appropriate
- [ ] Backup AND restore tested in nonproduction
- [ ] CSRF protection, rate limits, HTTPS and secure cookies reviewed

## Production hosting

Recommended: official **frappe_docker** production stack or a supported managed Frappe platform that permits custom apps. The standard production topology includes web, backend workers, scheduled job workers, Redis, MariaDB, TLS, backups and monitoring. Do not deploy this as a single Django container; it is a Frappe app, not a Django application.

Custom app sources must be included in the Bench container image or installed through the provider's supported custom-app workflow. Host/domain, DNS, cloud account, secrets, backup destination, and budget must be specified before provisioning. Never commit passwords or tokens.

## Rollout sequence

1. Code review and smoke tests in a disposable evaluation site.
2. Configure minimal real business fields and manager/supervisor access.
3. Run representative sample shifts without real financial exposure.
4. Implement missing compliance, reporting, approval separation and accounting integration as required.
5. Deploy into isolated production tenancy with backups, monitoring and disaster recovery.
6. Train operators and agree acceptance criteria with the owner.

## Known gaps and caveats

- No live production Bench execution was performed from ChatGPT.
- The custom dashboard is a first-cut Desk Page, not a fully designed sales cockpit.
- The station shift schedule is an expected report deadline; it is **not** automatically linked to HRMS Attendance or Shift Assignment.
- Cash and reported sales are operator-entered figures, not reconciled ledger data.
- Employee count counts station assignments, not Frappe HR employees.
- No email/SMS integration is enabled.
- Correction history for approved cash reports still requires a formal append-only amendment workflow.
