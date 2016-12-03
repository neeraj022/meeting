frappe.listview_settings['Meeting'] = {

get_indicator: function(doc) {
		return [__(doc.status), {"Draft":"grey", "Completed":"green", "Planned":"yellow"}[doc.status],
			"status,=," + doc.status];
	}
};