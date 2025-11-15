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
            print("-" * 150)
            return True, f"Product updated: {updated_product}"
            print("-" * 150)
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
            ("BP001", "Enfamil Baby Milk Powder (900g)", "Milk Powder", 25.99, 50, "For 0-6 months, iron fortified"),
            ("BP002", "Pampers Baby Diapers (Size S, 64pcs)", "Diapers", 15.50, 100,
             "Hypoallergenic, wetness indicator"),
            ("BP003", "Huggies Baby Wipes (80pcs)", "Care", 5.99, 200, "Alcohol-free, gentle on skin"),
            ("BP004", "Philips Avent Feeding Bottle (240ml)", "Feeding", 8.99, 30, "BPA-free, anti-colic system"),
            ("BP005", "Johnson's Baby Shampoo (400ml)", "Bath", 12.99, 40, "Tear-free formula, pH balanced"),
            ("BP006", "Graco Baby Stroller Lite", "Travel", 199.99, 10, "Lightweight, foldable, one-hand close"),
            ("BP007", "NUK Pacifier Orthodontic", "Feeding", 4.99, 60, "Orthodontic, silicone, 0-6 months"),
            ("BP008", "Carter's Baby Blanket (100x120cm)", "Nursery", 29.99, 25,
             "Soft cotton material, machine washable"),
            ("BP009", "Motorola Baby Monitor HD", "Safety", 89.99, 15, "Video and audio monitoring, night vision"),
            ("BP010", "BabyBjorn Baby Carrier One", "Travel", 59.99, 20, "Ergonomic design, 4 carrying positions"),
            ("BP011", "Sophie la Girafe Teething Ring", "Health", 6.99, 45, "Soothing gel filled, natural rubber"),
            ("BP012", "Aveeno Baby Lotion (227g)", "Bath", 8.99, 35, "Hypoallergenic formula, oatmeal enriched"),
            ("BP013", "Burt's Bees Baby Oil (118ml)", "Bath", 7.49, 40, "Natural ingredients, 100% natural"),
            ("BP014", "Johnson's Baby Powder (200g)", "Bath", 5.99, 50, "Talc-free, corn starch based"),
            ("BP015", "Dove Baby Soap (100g x 3)", "Bath", 4.99, 60, "Gentle on skin, 1/4 moisturizing cream"),
            ("BP016", "Hudson Baby Towel with Hood", "Bath", 12.99, 30, "Hooded towel, 100% cotton"),
            ("BP017", "Summer Infant Baby Bathtub", "Bath", 24.99, 18, "Non-slip surface, built-in support"),
            ("BP018", "Boppy Nursing Pillow", "Feeding", 34.99, 22, "Supportive design, removable cover"),
            ("BP019", "Tommee Tippee Bottle Warmer", "Feeding", 29.99, 25, "Fast heating, auto shut-off"),
            ("BP020", "Beaba Baby Food Maker", "Feeding", 49.99, 12, "Multi-function, steam and blend"),
            ("BP021", "Stokke High Chair Tripp Trapp", "Feeding", 79.99, 8, "Adjustable height, grows with child"),
            ("BP022", "Munchkin Baby Spoon (4pcs)", "Feeding", 3.99, 80, "Soft tip, heat sensitive"),
            ("BP023", "Aden + Anais Baby Bib (3pcs)", "Feeding", 2.99, 100, "Waterproof, adjustable snap"),
            ("BP024", "Skip Hop Diaper Bag Backpack", "Travel", 39.99, 20, "Multiple compartments, insulated pocket"),
            ("BP025", "Britax Car Seat Marathon", "Travel", 129.99, 10, "Safety certified, side impact protection"),
            ("BP026", "UPPAbaby Stroller Vista", "Travel", 199.99, 6, "All-terrain wheels, reversible seat"),
            ("BP027", "Hanes Baby Socks (6 pairs)", "Clothing", 5.99, 70, "Non-slip bottoms, cotton blend"),
            ("BP028", "iPlay Baby Hat Sun Protection", "Clothing", 8.99, 40, "Sun protection UPF 50+"),
            ("BP029", "Gerber Onesies Bodysuit (Pack of 3)", "Clothing", 12.99, 55, "100% cotton, snap closure"),
            ("BP030", "The Children's Place Pajamas", "Clothing", 15.99, 35, "Cotton material, flame resistant"),
            ("BP031", "Columbia Baby Jacket", "Clothing", 24.99, 25, "Weather resistant, Omni-Heat thermal"),
            ("BP032", "Stride Rite Baby Shoes", "Clothing", 19.99, 30, "Soft sole, flexible, machine washable"),
            ("BP033", "Zutano Baby Mittens", "Clothing", 4.99, 60, "Scratch prevention, stay-on design"),
            ("BP034", "Kate Quinn Baby Romper", "Clothing", 18.99, 28, "Easy to wear, organic cotton"),
            ("BP035", "Braun Thermometer Digital", "Health", 14.99, 40, "Digital display, forehead scanning"),
            ("BP036", "Fridababy Nasal Aspirator", "Health", 9.99, 45, "Bulb type, hospital grade"),
            ("BP037", "Safety 1st Baby Nail Clipper", "Health", 3.99, 65, "Safety guard, magnifying glass"),
            ("BP038", "Little Remedies Medicine Dropper", "Health", 2.99, 75, "Accurate dosage, markings in ml"),
            ("BP039", "Zwilling Baby Brush Set", "Care", 6.99, 50, "Soft bristles, natural wood handle"),
            ("BP040", "Tangle Teezer Baby Comb", "Care", 3.49, 55, "Gentle on scalp, detangling"),
            ("BP041", "Jordan Baby Toothbrush Step 1", "Care", 4.99, 48, "Finger brush, soft silicone"),
            ("BP042", "Desitin Diaper Rash Cream (113g)", "Health", 8.49, 38, "Zinc oxide, maximum strength"),
            ("BP043", "Neutrogena Baby Sunscreen SPF 50", "Health", 11.99, 32, "SPF 50, water resistant 80min"),
            ("BP044", "Babyganics Insect Repellent", "Health", 9.49, 36, "Natural formula, DEET-free"),
            ("BP045", "Mustela Baby Shampoo (500ml)", "Bath", 7.99, 42, "Tear-free, avocado perseose"),
            ("BP046", "California Baby Conditioner (192ml)", "Bath", 7.99, 40, "Detangling, organic ingredients"),
            ("BP047", "Mr. Bubble Bubble Bath (532ml)", "Bath", 6.99, 45, "Fun bubbles, tear-free formula"),
            ("BP048", "Munchkin Bath Toys Set", "Bath", 12.99, 28, "Floating animals, 8 pieces set"),
            ("BP049", "Pottery Barn Kids Baby Robe", "Bath", 22.99, 20, "Plush material, hooded"),
            ("BP050", "Fisher-Price Bath Thermometer", "Bath", 8.99, 35, "Duck shape, easy to read")
        ]

        # Add all sample products to the system
        for product in sample_products:
            success, message = self.add_product(*product)
