{
  "name": "Edu Billing",
  "summary": "Учёт оплат студентов: части платежей, водопад, пеня 1%/день",
  "version": "16.0.1.0.0",
  "category": "Education",
  "author": "UPSOFT",
  "license": "LGPL-3",
  "depends": [
    "base"
  ],
  "data": [
    "data/edu_sequence.xml",
    "security/ir.model.access.csv",
    "data/edu_cron.xml",
    "views/edu_menus.xml",
    "views/edu_student_views.xml",
    "views/edu_contract_views.xml",
    "views/edu_payment_views.xml"
  ],
  "assets": {},
  "installable": true,
  "application": true
}