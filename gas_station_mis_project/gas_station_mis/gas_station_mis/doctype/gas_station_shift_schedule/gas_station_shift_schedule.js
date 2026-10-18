frappe.ui.form.on("Gas Station Shift Schedule", {
    refresh(frm) {
        frm.set_query("station", () => ({ filters: { active: 1 } }));
    }
});
