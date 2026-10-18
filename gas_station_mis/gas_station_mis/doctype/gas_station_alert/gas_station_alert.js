frappe.ui.form.on("Gas Station Alert", {
    refresh(frm) {
        frm.disable_save();
        if (frm.is_new() || frm.doc.status !== "Open") return;
        frappe.call({
            method: "gas_station_mis.api.station_actions",
            args: { station: frm.doc.station }
        }).then(r => {
            if (!r.message || !r.message.can_manage) return;
            frm.add_custom_button(__("Resolve Alert"), () => {
                frappe.call({
                    method: "gas_station_mis.api.resolve_alert",
                    type: "POST",
                    args: { name: frm.doc.name }
                }).then(() => frm.reload_doc());
            });
        });
    }
});
