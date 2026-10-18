frappe.ui.form.on("Gas Station Shift Report", {
    refresh(frm) {
        if (frm.is_new()) return;
        const state = frm.doc.status;
        if (["Submitted", "Approved"].includes(state)) {
            frm.disable_save();
        }
        frappe.call({
            method: "gas_station_mis.api.report_actions",
            args: { name: frm.doc.name }
        }).then(r => {
            const actions = r.message || {};
            if (actions.can_submit) {
                frm.add_custom_button(__("Submit for Approval"), () => {
                    frappe.confirm(__("Submit this shift report?"), () => {
                        frappe.call({
                            method: "gas_station_mis.api.submit_report",
                            type: "POST",
                            args: { name: frm.doc.name }
                        }).then(() => frm.reload_doc());
                    });
                });
            }
            if (actions.can_approve) {
                frm.add_custom_button(__("Approve"), () => {
                    frappe.confirm(__("Approve and lock this report?"), () => {
                        frappe.call({
                            method: "gas_station_mis.api.approve_report",
                            type: "POST",
                            args: { name: frm.doc.name }
                        }).then(() => frm.reload_doc());
                    });
                });
                frm.add_custom_button(__("Return for Correction"), () => {
                    frappe.prompt(
                        [{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }],
                        values => frappe.call({
                            method: "gas_station_mis.api.return_report",
                            type: "POST",
                            args: { name: frm.doc.name, reason: values.reason }
                        }).then(() => frm.reload_doc()),
                        __("Return Report"),
                        __("Return")
                    );
                });
            }
        });
    },
    shift_schedule(frm) {
        if (frm.doc.shift_schedule) {
            frappe.db.get_value("Gas Station Shift Schedule", frm.doc.shift_schedule, "station")
                .then(r => {
                    if (r.message && r.message.station && !frm.doc.station) {
                        frm.set_value("station", r.message.station);
                    }
                });
        }
    }
});
