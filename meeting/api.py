import frappe
from frappe import _
from datetime import datetime

@frappe.whitelist()
def send_invitation_emails(meeting):
    meeting=frappe.get_doc("Meeting", meeting)
    if meeting.status=="Planned":
        frappe.sendmail(recipients=[d.attendee for d in meeting.attendees], sender=frappe.session.user,
                         subject=meeting.title, message=meeting.invitation_message, reference_doctype=meeting.doctype, reference_name=meeting.name)
        meeting.status='Invitation Sent'
        meeting.save()

        frappe.msgprint(_('Invitation emails have been send'))

    else:
        frappe.msgprint(_('Emails can be send only for Planned Meetings'))


@frappe.whitelist()
def get_calendar_meetings(start, end):
    if not frappe.has_permission('Meeting', 'read'):
        raise frappe.PermissionError

    result=frappe.db.sql('''select 0 as all_day, name, title, status, timestamp(date, from_time) as start, timestamp(date, to_time) as end from `tabMeeting` where date between
    %(start)s and %(end)s''', {"start":start, "end":end}, as_dict=1)
    return result

@frappe.whitelist()
def orientation_meeting(doc, method):
    meeting=frappe.get_doc({
        "doctype": "Meeting",
        "title" : "Orientation for {0}".format(doc.first_name),
        "date" : datetime.now() ,
        "from_time": "09:00",
        "to_time": "09:30",
        "status": "Planned",
        "attendees": [{"attendee": doc.name}]
    })
    meeting.flags.ignore_permissions=True
    meeting.insert()
    frappe.msgprint(_('Orientation meeting has been created'))
