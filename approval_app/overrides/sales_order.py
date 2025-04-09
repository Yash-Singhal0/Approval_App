import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as ERPNextSalesOrder

class CustomSalesOrder(ERPNextSalesOrder):

    def calculate_custom_discount(self):
        if self.discount_amount and self.items:
            total_discount = self.discount_amount

            for i, item in enumerate(self.items):
                # Resetting the values first, before custonm logic
                item.discount_amount = 0
                item.net_rate = item.rate
                item.net_amount = item.rate * item.qty
                item.base_net_rate = item.rate
                item.base_net_amount = item.net_amount

                if i == 0:
                    # Applying full discount to first item here
                    item.discount_amount = total_discount
                    discount_per_unit = total_discount / item.qty

                    # Updating net rate and amount values after discount here
                    item.net_rate = item.rate - discount_per_unit
                    item.net_amount = item.net_rate * item.qty
                    item.base_net_rate = item.net_rate
                    item.base_net_amount = item.net_amount

    def calculate_taxes_and_totals(self):
        # Calling ERPNext original method here, it will do calculations as normal it do
        super().calculate_taxes_and_totals()

        # here i am applying my custom logic after the default function has calculated everything
        self.calculate_custom_discount()

        # Recalculating the fields based on updated items now, after applying discounts
        self.net_total = sum(item.net_amount for item in self.items)
        self.base_net_total = sum(item.base_net_amount for item in self.items)
        self.grand_total = self.net_total + self.total_taxes_and_charges
        self.base_grand_total = self.base_net_total + self.base_total_taxes_and_charges
