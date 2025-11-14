"""
Question 2: Category Management System

This file handles category management for the baby shop inventory.
It allows to manage, display, and validate product categories.

"""

class CategoryManager:
    # ==========================================================================
    # INITIALIZATION SECTION - CATEGORY SETUP
    # ==========================================================================
    def __init__(self, shop_storage):
        """Initialize CategoryManager with shop storage reference and default categories"""
        self.shop_storage = shop_storage

        # Sample data
        self.categories = [
            "Milk Powder", "Diapers", "Care", "Feeding", "Bath", "Travel"
        ]

    # ==========================================================================
    # DISPLAY CATEGORIES SECTION - CATEGORY VIEWING
    # ==========================================================================
    def show_categories(self):
        """Display all available categories"""
        print("\n--- Available Categories ---")
        if not self.categories:
            print("No categories available")
        else:
            # Display each category with usage indicator
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")
        print("-" * 30)
        return len(self.categories)

    # ==========================================================================
    # CATEGORY VALIDATION SECTION - USAGE CHECKING
    # ==========================================================================
    def is_category_used(self, category):
        """Check if a category is currently being used by any products"""
        all_products = self.shop_storage.get_all_products()
        for product in all_products:
            if product.category == category:
                return True
        return False

    def get_category_by_choice(self, choice):
        """
        Get category name based on user's numerical choice

        Args:
            choice (int): User's category selection number

        Returns:
            str: Category name if valid choice, None otherwise
        """
        if 1 <= choice <= len(self.categories):
            return self.categories[choice - 1]
        return None

    # ==========================================================================
    # ADD CATEGORY SECTION - CATEGORY CREATION
    # ==========================================================================
    def add_new_category(self, new_category):
        """
        Add a new category to the system

        Args:
            new_category (str): Name of the new category to add

        Returns:
            bool: True if category added successfully, False if already exists
        """
        if new_category not in self.categories:
            self.categories.append(new_category)
            print(f"\033[32mNew category '{new_category}' added successfully!\033[0m")
            return True
        else:
            print("\033[31mCategory already exists!\033[0m")
            return False

    # ==========================================================================
    # DELETE CATEGORY SECTION - CATEGORY REMOVAL
    # ==========================================================================
    def delete_category(self, choice):
        """Delete a category from the system if not in use"""
        if 1 <= choice <= len(self.categories):
            category_to_delete = self.categories[choice - 1]

            # Check if category is being used by any products
            if self.is_category_used(category_to_delete):
                print(f"\033[31mCannot delete category '{category_to_delete}', it is being used by products!\033[0m")
                return False
            else:
                # Safe to delete category
                deleted_category = self.categories.pop(choice - 1)
                print(f"\033[32mCategory '{deleted_category}' deleted successfully!\033[0m")
                return True
        return False

    # ==========================================================================
    # MENU MANAGEMENT SECTION - DYNAMIC MENU OPTIONS
    # ==========================================================================
    def get_category_management_menu(self):
        """
        Generate dynamic menu options based on current categories

        Returns:
            list: Available menu options for category management
        """
        category_count = len(self.categories)
        menu_options = []

        # Only show delete option if categories exist
        if category_count > 0:
            menu_options.append("Delete Existing Category")
        # Always show add option
        menu_options.append("Add New Category")

        return menu_options