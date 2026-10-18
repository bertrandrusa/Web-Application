/* Lightweight Frappe Desk dashboard; all metrics come from scoped server APIs. */
frappe.pages["station-dashboard"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Gas Station Dashboard"),
        single_column: true
    });
    const $body = $(page.body);
    $body.html(`
        <div class="gas-dashboard" style="padding:18px 0;max-width:1100px">
            <div class="alert alert-info" id="gas-dash-message">Loading stations…</div>
            <div id="gas-dash-data" style="display:none">
                <div style="margin-bottom:20px">
                    <strong id="gas-dash-station"></strong>
                    <span class="text-muted" id="gas-dash-date" style="margin-left:8px"></span>
                </div>
                <div class="row" id="gas-dash-cards"></div>
                <h4 style="margin-top:24px">Recent alerts</h4>
                <div id="gas-dash-alerts" class="list-group"></div>
                <div style="margin-top:20px">
                    <button class="btn btn-primary" id="gas-dash-reports">Open shift reports</button>
                    <button class="btn btn-default" id="gas-dash-alert-list">View alerts</button>
                </div>
            </div>
        </div>
    `);
    $body.find("#gas-dash-reports").on("click", () => frappe.set_route("List", "Gas Station Shift Report"));
    $body.find("#gas-dash-alert-list").on("click", () => frappe.set_route("List", "Gas Station Alert"));

    async function refresh(station) {
        $body.find("#gas-dash-message").text("Loading dashboard…").show();
        $body.find("#gas-dash-data").hide();
        try {
            const response = await frappe.call({
                method: "gas_station_mis.api.get_dashboard",
                args: { station }
            });
            const data = response.message;
            $body.find("#gas-dash-station").text(data.station);
            $body.find("#gas-dash-date").text(data.date);
            const cards = [
                ["Assigned staff", data.staff_count],
                ["Today's reports", data.shift_reports],
                ["Pending approvals", data.pending_reports],
                ["Approved reports", data.approved_reports],
                ["Approved reported sales", format_currency(data.reported_sales_approved)],
                ["Open alerts", data.open_alert_count]
            ];
            const $cards = $body.find("#gas-dash-cards").empty();
            cards.forEach(([label, value]) => {
                const $col = $("<div>").addClass("col-sm-6 col-md-4").css("margin-bottom", "14px");
                const $panel = $("<div>").addClass("card").css({ padding: "18px", height: "100%" });
                $("<div>").addClass("text-muted").text(label).appendTo($panel);
                $("<div>").css({ fontSize: "23px", fontWeight: "600", marginTop: "8px" }).text(value).appendTo($panel);
                $col.append($panel).appendTo($cards);
            });
            const $alerts = $body.find("#gas-dash-alerts").empty();
            if (!data.recent_alerts.length) {
                $("<div>").addClass("list-group-item text-muted").text("No recent alerts visible.").appendTo($alerts);
            }
            data.recent_alerts.forEach(alert => {
                const $link = $("<a>").addClass("list-group-item list-group-item-action")
                    .attr("href", "#").on("click", (event) => {
                        event.preventDefault();
                        frappe.set_route("Form", "Gas Station Alert", alert.name);
                    });
                $("<strong>").text(alert.alert_type + ": ").appendTo($link);
                $("<span>").text(alert.message).appendTo($link);
                $link.appendTo($alerts);
            });
            $body.find("#gas-dash-message").hide();
            $body.find("#gas-dash-data").show();
        } catch (error) {
            $body.find("#gas-dash-message").text("Unable to load station metrics. Check station permissions.").show();
        }
    }

    frappe.call({ method: "gas_station_mis.api.available_stations" })
        .then(response => {
            const stations = response.message || [];
            if (!stations.length) {
                $body.find("#gas-dash-message").text("No station access assigned. Ask a System Manager to create a staff assignment.");
                return;
            }
            const field = page.add_field({
                fieldtype: "Select",
                fieldname: "station",
                label: __("Station"),
                options: stations.map(s => s.value).join("\n"),
                change: () => refresh(field.get_value())
            });
            field.set_value(stations[0].value);
            refresh(stations[0].value);
            page.set_primary_action(__("Refresh"), () => refresh(field.get_value()));
        })
        .catch(() => $body.find("#gas-dash-message").text("Failed to load permitted stations."));
};
