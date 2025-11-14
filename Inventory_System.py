"""
Question 2 and 3: Command-Line Inventory System (User Interface)

This file provides the user interface for the baby products inventory system.

"""

from Baby_Shop_Storage import BabyShopStorage
from Performance_Comparator import PerformanceComparator
import re

class InventorySystem:
    def __init__(self):
        self.shop_storage = BabyShopStorage(10)
        self.shop_storage.preload_sample_data()

    # ==========================================================================
    # MENU DISPLAY SECTION
    # ==========================================================================
    def display_menu(self):
        """Display the main menu options for the inventory system"""
        print("\n" + "=" * 40)
        print("      Baby Products Inventory System")
        print("=" * 40)
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Manage Categories")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Show All Products")
        print("7. Performance Test")
        print("8. Exit System")
        print("=" * 40)

    def get_input_with_exit(self, prompt):
        """Get user input with option to cancel operation by pressing 'E'"""
        user_input = input(prompt).strip()
        if user_input.upper() == 'E':
            return None
        return user_input

    # ==========================================================================
    # ADD PRODUCT SECTION
    # ==========================================================================
    def add_product_interactive(self):
        """Interactive process to add a new product to inventory"""
        print("\n--- Add New Product ---")
        print("* Press 'E' at any time to cancel and return to main menu")

        # Display suggested product IDs
        latest_id = self.shop_storage.get_latest_product_id()
        next_id = self.shop_storage.get_next_product_id()
        print(f"Latest Product ID: {latest_id}")
        print(f"Suggested Next ID: {next_id}")
        print("-" * 40)

        # Get Product ID input
        product_id = self.get_input_with_exit("Enter Product ID: ")
        if product_id is None:
            print("Operation cancelled.")
            return

        if not product_id:
            print("\033[31mProduct ID cannot be empty!\033[0m")
            return

        product_id = product_id.upper()

        # Validate Product ID format
        if not re.match(r'^BP\d+$', product_id):
            print("\033[31mInvalid Product ID format! Please use BP001, BP002, etc.\033[0m")
            return

        # Check if Product ID already exists
        if self.shop_storage.get_product(product_id):
            print(f"\033[31mProduct ID '{product_id}' already exists! Please use a different ID\033[0m")
            return

        # Get Product Name
        name = self.get_input_with_exit("Enter Product Name: ")
        if name is None:
            print("Operation cancelled.")
            return
        if not name:
            print("\033[31mProduct name cannot be empty!\033[0m")
            return

        # Select or create category
        category = self.select_category()
        if category is None:
            return

        # Get Price input
        price_input = self.get_input_with_exit("Enter Price: ")
        if price_input is None:
            print("Operation cancelled.")
            return
        try:
            price = float(price_input)
        except ValueError:
            print("\033[31mInvalid price format!\033[0m")
            return

        # Get Stock Quantity input
        quantity_input = self.get_input_with_exit("Enter Stock Quantity: ")
        if quantity_input is None:
            print("Operation cancelled.")
            return
        try:
            quantity = int(quantity_input)
        except ValueError:
            print("\033[31mInvalid quantity format!\033[0m")
            return

        # Get optional remarks
        remarks = self.get_input_with_exit("Enter Remarks (Optional): ")
        if remarks is None:
            print("Operation cancelled.")
            return
        if not remarks:
            remarks = "(no remark)"

        # Add product to storage
        success, message = self.shop_storage.add_product(product_id, name, category, price, quantity, remarks)
        if success:
            print('-' * 120)
            print(f"\033[32mNew Product created: {message}\033[0m")
            print('-' * 120)
        else:
            print(f"\033[31m{message}\033[0m")

    def select_category(self):
        """Allow user to select existing category or create new one"""
        category_count = self.shop_storage.category_manager.show_categories()
        print(f"{category_count + 1}. Add New Category")
        print("-" * 30)

        choice_input = self.get_input_with_exit(f"Choose category (1-{category_count + 1}): ")
        if choice_input is None:
            return None

        try:
            choice = int(choice_input)

            if 1 <= choice <= category_count:
                return self.shop_storage.category_manager.categories[choice - 1]
            elif choice == category_count + 1:
                print(f"\n--- Add New Category ---")
                print("* Enter 'E' to cancel add new category")
                new_category = input("\nEnter new category name: ")
                if new_category.upper() == 'E':
                    print("Add new category cancelled.")
                    return self.select_category()

                if new_category:
                    if self.shop_storage.category_manager.add_new_category(new_category):
                        return new_category
                    else:
                        return self.select_category()
                else:
                    print("Category name cannot be empty!")
                    return self.select_category()
            else:
                print("Invalid choice! Please try again.")
                return self.select_category()
        except ValueError:
            print("Please enter a valid number!")
            return self.select_category()

    # ==========================================================================
    # SEARCH PRODUCT SECTION
    # ==========================================================================
    def search_product_interactive(self):
        """Interactive product search by ID or keyword"""
        print("\n--- Search Product ---")
        print("* Press 'E' at any time to cancel and return to main menu")
        print("Search Options:")
        print("1. Search by ID")
        print("2. Search All Fields")

        search_choice = self.get_input_with_exit("Choose search method (1-2): ")
        if search_choice is None:
            print("Operation cancelled.")
            return

        if search_choice == '1':
            # Search by Product ID
            product_id = self.get_input_with_exit("Enter Product ID to search: ")
            if product_id is None:
                print("Operation cancelled.")
                return
            if not product_id:
                print("\033[31mProduct ID cannot be empty!\033[0m")
                return

            product_id = product_id.upper()
            product = self.shop_storage.get_product(product_id)

            if product:
                print(f"\033[32mProduct found: {product}\033[0m")
            else:
                print(f"\033[31mProduct not found: {product_id}\033[0m")

        elif search_choice == '2':
            # Search all fields by keyword
            keyword = self.get_input_with_exit("Enter search keyword: ")
            if keyword is None:
                print("Operation cancelled.")
                return
            if not keyword:
                print("\033[31mSearch keyword cannot be empty!\033[0m")
                return

            results = self.shop_storage.search_products(keyword)

            if results:
                print(f"\n\033[32mFound {len(results)} matching products:\033[0m")
                print("-" * 80)
                for i, product in enumerate(results, 1):
                    print(f"{i}. {product}")
            else:
                print("\033[31mNo matching products found.\033[0m")
        else:
            print("Invalid choice!")

    # ==========================================================================
    # DISPLAY PRODUCTS SECTION
    # ==========================================================================
    def show_all_products(self):
        """Display all products in a formatted table"""
        print("\n--- All Products List ---")
        print(f"\n｜{'ID':<10}｜{'Name':<30}｜{'Category':<20}｜{'Price':<12}｜{'Stock':<10}｜{'Remarks':<20}")
        print('-' * 120)

        products = self.shop_storage.get_all_products()
        if products:
            for i, product in enumerate(products, 1):
                print(f"{product}")

            print(f"\nTotal: {len(products)} products")
        else:
            print("No products available")

    # ==========================================================================
    # EDIT PRODUCT SECTION
    # ==========================================================================
    def edit_product_interactive(self):
        """Interactive product editing process"""
        print("\n--- Edit Product ---")
        print("* Press 'E' at any time to cancel and return to main menu")

        products = self.shop_storage.get_all_products()
        if not products:
            print("No products available for editing")
            return

        # Display available products for editing
        print("\nAvailable Products:")
        print(f"\n｜{'ID':<10}｜{'Name':<30}｜{'Category':<20}｜{'Price':<12}｜{'Stock':<10}｜{'Remarks':<20}")
        print('-' * 120)
        for product in products:
            print(f"{product}")
        print('-' * 120)

        # Get product ID to edit
        product_id = self.get_input_with_exit("\nEnter Product ID to edit: ")
        if product_id is None:
            print("Operation cancelled.")
            return

        if not product_id:
            print("\033[31mProduct ID cannot be empty!\033[0m")
            return

        product_id = product_id.upper()
        product_to_edit = self.shop_storage.get_product(product_id)
        if not product_to_edit:
            print(f"\033[31mProduct with ID '{product_id}' not found!\033[0m")
            return

        self.edit_product_details(product_id, product_to_edit)

    def edit_product_details(self, product_id, product):
        """Edit specific product details"""
        print("-" * 120)
        print(f"\nEditing Product: {product}")
        print("-" * 120)
        print("\nNote: Press Enter to keep current value")
        print("* Press 'E' at any time to cancel")
        print("-" * 50)

        # Edit product name
        new_name = self.get_input_with_exit(f"Product Name [{product.name}]: ")
        if new_name is None:
            print("Operation cancelled.")
            return
        if not new_name:
            new_name = product.name

        # Edit category
        print(f"\nCurrent Category: {product.category}")
        change_category = self.get_input_with_exit("Change category? (Y/N): ")
        if change_category is None:
            print("Operation cancelled.")
            return
        if change_category.lower() == 'y':
            new_category = self.select_category()
            if new_category is None:
                return
        else:
            new_category = product.category

        # Edit price
        new_price_input = self.get_input_with_exit(f"Price [${product.price}]: ")
        if new_price_input is None:
            print("Operation cancelled.")
            return
        if new_price_input:
            try:
                new_price = float(new_price_input)
            except ValueError:
                print("\033[31mInvalid price format, keeping original value\033[0m")
                new_price = product.price
        else:
            new_price = product.price

        # Edit stock quantity
        new_quantity_input = self.get_input_with_exit(f"Stock Quantity [{product.quantity}]: ")
        if new_quantity_input is None:
            print("Operation cancelled.")
            return
        if new_quantity_input:
            try:
                new_quantity = int(new_quantity_input)
            except ValueError:
                print("\033[31mInvalid quantity format, keeping original value\033[0m")
                new_quantity = product.quantity
        else:
            new_quantity = product.quantity

        # Edit remarks
        new_remarks = self.get_input_with_exit(f"Remarks [{product.remarks}]: ")
        if new_remarks is None:
            print("Operation cancelled.")
            return
        if not new_remarks:
            new_remarks = product.remarks

        # Update product in storage
        success, message = self.shop_storage.update_product(product_id, new_name, new_category, new_price, new_quantity, new_remarks)
        if success:
            print(f"\033[32m{message}\033[0m")
        else:
            print(f"\033[31m{message}\033[0m")

    # ==========================================================================
    # DELETE PRODUCT SECTION
    # ==========================================================================
    def delete_product_interactive(self):
        """Interactive product deletion process"""
        print("\n--- Delete Product ---")
        print("* Press 'E' at any time to cancel and return to main menu")

        products = self.shop_storage.get_all_products()
        if not products:
            print("No products available for deletion")
            return

        # Display available products for deletion
        print("\nAvailable Products:")
        print(f"\n｜{'ID':<10}｜{'Name':<30}｜{'Category':<20}｜{'Price':<12}｜{'Stock':<10}｜{'Remarks':<20}")
        print('-' * 120)
        for product in products:
            print(f"{product}")
        print('-' * 120)

        # Get product ID to delete
        product_id = self.get_input_with_exit("\nEnter Product ID to delete: ")
        if product_id is None:
            print("Operation cancelled.")
            return

        if not product_id:
            print("\033[31mProduct ID cannot be empty!\033[0m")
            return

        product_id = product_id.upper()

        # Confirm deletion
        confirm = self.get_input_with_exit(f"Are you sure you want to delete product '{product_id}'? This cannot be undone. (Y/N): ")
        if confirm is None:
            print("Operation cancelled.")
            return

        if confirm.lower() == 'y':
            success, message = self.shop_storage.delete_product(product_id)
            if success:
                print(f"\033[32m{message}\033[0m")
            else:
                print(f"\033[{message}31m\033[0m")
        else:
            print("Deletion cancelled.")

    # ==========================================================================
    # CATEGORY MANAGEMENT SECTION
    # ==========================================================================
    def show_products_in_category(self, category):
        """Display all products in a specific category"""
        products = self.shop_storage.get_products_by_category(category)
        if products:
            print(f"\n--- Products in Category '{category}' ---")
            for product in products:
                print(f"\n｜{'ID':<10}｜{'Name':<30}｜{'Category':<20}｜{'Price':<12}｜{'Stock':<10}｜{'Remarks':<20}")
                print('-' * 120)
                print(f"{product}")
                print('-' * 120)
        else:
            print(f"\nNo products in category '{category}'")

    def manage_categories(self):
        """Manage product categories (add, delete, view)"""
        print("\n--- Manage Categories ---")
        print("* Press 'E' at any time to cancel and return to main menu")

        choice = 0

        while choice != 3:
            category_count = self.shop_storage.category_manager.show_categories()

            print("\n--- Category Management Options ---")
            menu_options = self.shop_storage.category_manager.get_category_management_menu()
            for i, option in enumerate(menu_options, 1):
                print(f"{i}. {option}")
            print("3. Exit Category Management")
            print("-" * 36)

            choice_input = self.get_input_with_exit("Choose operation (1-3): ")
            if choice_input is None:
                print("Operation cancelled.")
                break

            try:
                choice = int(choice_input)

                if choice == 1 and "Delete Existing Category" in menu_options:
                    if category_count > 0:
                        try:
                            delete_choice_input = self.get_input_with_exit(
                                f"Enter category number to delete (1-{category_count}): ")
                            if delete_choice_input is None:
                                continue
                            delete_choice = int(delete_choice_input)
                            if 1 <= delete_choice <= category_count:
                                category_to_delete = self.shop_storage.category_manager.categories[delete_choice - 1]

                                if not self.shop_storage.category_manager.delete_category(delete_choice):
                                    self.show_products_in_category(category_to_delete)
                            else:
                                print("\033[31mInvalid category number!\033[0m")
                        except ValueError:
                            print("\033[31mPlease enter a valid number!\033[0m")
                    else:
                        print("No categories available to delete!")

                elif (choice == 2 and "Delete Existing Category" in menu_options) or (
                        choice == 1 and "Add New Category" in menu_options):
                    new_category = self.get_input_with_exit("Enter new category name: ")
                    if new_category is None:
                        continue
                    if new_category:
                        self.shop_storage.category_manager.add_new_category(new_category)
                    else:
                        print("\033[31mCategory name cannot be empty!\033[0m")

                elif choice == 3:
                    print("Returning to main menu...")

                else:
                    print("\033[31mInvalid choice! Please try again.\033[0m")

            except ValueError:
                print("\033[31mPlease enter a valid number!\033[0m")

    # ==========================================================================
    # PERFORMANCE TEST SECTION
    # ==========================================================================
    def run_performance_test(self):
        """Run performance comparison tests"""
        print("\n--- Performance Comparison Test ---")
        comparator = PerformanceComparator(self.shop_storage)
        comparator.load_data_for_comparison()
        comparator.compare_search_performance(1000)

    # ==========================================================================
    # MAIN APPLICATION LOOP SECTION
    # ==========================================================================
    def run(self):
        """Main application loop to handle user interactions"""
        choice = ""

        while choice != '8':
            self.display_menu()
            choice = input("Choose operation (1-8): ").strip()

            if choice.upper() == 'E':
                print("Thank you for using Baby Products Inventory System!")
                break

            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                if choice == '1':
                    self.add_product_interactive()
                elif choice == '2':
                    self.edit_product_interactive()
                elif choice == '3':
                    self.manage_categories()
                elif choice == '4':
                    self.delete_product_interactive()
                elif choice == '5':
                    self.search_product_interactive()
                elif choice == '6':
                    self.show_all_products()
                elif choice == '7':
                    self.run_performance_test()
            elif choice == '8':
                print("Thank you for using Baby Products Inventory System!")
            else:
                print("\033[31mInvalid choice! Please enter a number between 1-8.\033[0m")