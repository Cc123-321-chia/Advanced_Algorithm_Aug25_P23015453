"""
Question 2: Baby Product Entity Class

This file shows products in the baby shop inventory system.

"""

class BabyProduct:

    # ==========================================================================
    # CONSTRUCTOR SECTION - PRODUCT INITIALIZATION
    # ==========================================================================
    def __init__(self, product_id, name, category, price, quantity, remarks):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.remarks = remarks

    # ==========================================================================
    # STRING REPRESENTATION SECTION - DISPLAY FORMATTING
    # ==========================================================================
    def __str__(self):
        return (
            f"｜{self.product_id:<10}"
            f"｜{self.name:<30}"
            f"｜{self.category:<20}"
            f"｜RM {self.price:<10}"  
            f"｜{self.quantity:<10}"  
            f"｜{self.remarks:<20}"
        )