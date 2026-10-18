# Move this code-only branch to its own GitHub repository

This custom Frappe app currently lives on the `gas-station-mis` branch of `bertrandrusa/Web-Application`. The main Java project remains unchanged.

Once you create a repository called `gas-station-mis` in GitHub (GitHub UI → New repository, **do not initialize with a README**), run:

```bash
git clone --single-branch --branch gas-station-mis \
    https://github.com/bertrandrusa/Web-Application.git gas-station-mis
cd gas-station-mis
git remote rename origin legacy
git remote add origin https://github.com/bertrandrusa/gas-station-mis.git
git push -u origin HEAD:main
```

GitHub authentication will be required for the push. Your new `gas-station-mis` repository will contain only the custom app code, docs and tests. The old repository and its main branch will not change.

Then install from the dedicated repo:

```bash
cd ~/frappe-bench
bench get-app --branch main gas_station_mis \
    https://github.com/bertrandrusa/gas-station-mis.git
bench --site your-site.local install-app gas_station_mis
```

The new repository URL above is an **example expected after you create it**; it does not exist automatically.
