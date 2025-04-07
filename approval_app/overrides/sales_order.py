import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as ERPNextSalesOrder

class CustomSalesOrder(ERPNextSalesOrder):
    def apply_discount_on_first_item_only(self):
        if self.discount_amount and self.items:
            total_discount = self.discount_amount
            for i, item in enumerate(self.items):
                if i == 0:
                    item.discount_amount = total_discount
                else:
                    item.discount_amount = 0

            # adding line to confirm my custom is working.
            frappe.msgprint("Custom discount logic (on first item only) applied from Approval App!")

    def validate(self):
        self.apply_discount_on_first_item_only()
        super().validate()
