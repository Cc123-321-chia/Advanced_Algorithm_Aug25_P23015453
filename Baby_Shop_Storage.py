"""
Question 2: Baby Shop Storage System

This file is the main storage system that uses the hash table.
- Product management (add, search, update and delete)
- Inventory operations (get all products and filter by category)

"""

from Hash_Table_Array import HashTableArray
from Baby_Product import BabyProduct
from Category_Manager import CategoryManager
import re

class BabyShopStorage:
    def __init__(self, capacity=10):
        self.hash_table = HashTableArray(capacity)
        self.category_manager = CategoryManager(self)

    # ==========================================================================
    # ADD PRODUCT SECTION
    # ==========================================================================
    def add_product(self, product_id, name, category, price, quantity, remarks):
        """Add a new product to the inventory storage"""
        product_id = product_id.upper()

        # Check if product ID already exists
        if self.get_product(product_id):
            return False, "Product ID already exists"

        # Create new product and insert into hash table
        product = BabyProduct(product_id, name, category, price, quantity, remarks)
        result = self.hash_table.insert(product_id, product)
        if result == "inserted":
            return True, f"{product}"
        else:
            return False, "Failed to add product"

    # ==========================================================================
    # SEARCH PRODUCT SECTION
    # ==========================================================================
    def get_product(self, product_id):
        """Search for a specific product by ID"""
        product_id = product_id.upper()
        product = self.hash_table.search(product_id)
        if product:
            return product
        else:
            return None

    def get_all_products(self):
        """Get all products from the inventory"""
        return self.hash_table.get_all_values()

    def get_products_by_category(self, category):
        """Get all products belonging to a specific category"""
        products = []
        all_products = self.hash_table.get_all_values()
        for product in all_products:
            if product.category.lower() == category.lower():
                products.append(product)
        return products

    def search_products(self, keyword):
        """Search products across all fields using a keyword"""
        results = []
        keyword_lower = keyword.lower()
        all_products = self.hash_table.get_all_values()

        # Search across all product fields
        for product in all_products:
            if (keyword_lower in product.product_id.lower() or
                    keyword_lower in product.name.lower() or
                    keyword_lower in product.category.lower() or
                    keyword_lower in product.remarks.lower() or
                    keyword_lower in str(product.price) or
                    keyword_lower in str(product.quantity)):
                results.append(product)
        return results

    # ==========================================================================
    # PRODUCT ID MANAGEMENT SECTION
    # ==========================================================================
    def get_latest_product_id(self):
        """Get the highest product ID currently in the system"""
        products = self.get_all_products()
        if not products:
            return "BP000"

        # Extract numeric parts from product IDs
        ids = []
        for product in products:
            match = re.search(r'BP(\d+)', product.product_id)
            if match:
                ids.append(int(match.group(1)))

        if ids:
            latest_num = max(ids)
            return f"BP{latest_num:03d}"
        else:
            return "BP000"

    def get_next_product_id(self):
        """Generate the next available product ID"""
        latest_id = self.get_latest_product_id()
        match = re.search(r'BP(\d+)', latest_id)
        if match:
            next_num = int(match.group(1)) + 1
            return f"BP{next_num:03d}"
        return "BP001"

    # ==========================================================================
    # UPDATE PRODUCT SECTION
    # ==========================================================================
    def update_product(self, product_id, name, category, price, quantity, remarks):
        """Update an existing product's details"""
        existing_product = self.get_product(product_id)
        if not existing_product:
            return False, "Product not found"

        # Create updated product and insert into hash table
        updated_product = BabyProduct(product_id, name, category, price, quantity, remarks)
        result = self.hash_table.insert(product_id, updated_product)
        if result == "updated":
            print("-" * 120)
            return True, f"Product updated: {updated_product}"
            print("-" * 120)
        else:
            return False, "Failed to update product"

    # ==========================================================================
    # DELETE PRODUCT SECTION
    # ==========================================================================
    def delete_product(self, product_id):
        """Delete a product from the inventory"""
        product_id = product_id.upper()

        # Check if product exists before deletion
        if not self.get_product(product_id):
            return False, "Product not found"

        success = self.hash_table.delete(product_id)
        if success:
            return True, f"Product '{product_id}' deleted successfully"
        else:
            return False, "Failed to delete product"

    # ==========================================================================
    # SAMPLE DATA SECTION
    # ==========================================================================
    def preload_sample_data(self):
        """Preload sample baby products for demonstration"""
        sample_products = [
            ("BP001", "Baby Milk Powder", "Milk Powder", 25.99, 50, "For 0-6 months"),
            ("BP002", "Baby Diapers", "Diapers", 15.50, 100, "Size S, hypoallergenic"),
            ("BP003", "Baby Wipes", "Care", 5.99, 200, "Alcohol-free, gentle"),
            ("BP004", "Feeding Bottle", "Feeding", 8.99, 30, "240ml, BPA-free"),
            ("BP005", "Baby Shampoo", "Bath", 12.99, 40, "Tear-free formula"),
            ("BP006", "Baby Stroller", "Travel", 199.99, 10, "Lightweight, foldable"),
            ("BP007", "Pacifier", "Feeding", 4.99, 60, "Orthodontic, silicone")
        ]

        # Add all sample products to the system
        for product in sample_products:
            success, message = self.add_product(*product)