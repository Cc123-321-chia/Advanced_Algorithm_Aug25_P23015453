"""
Question 4: Performance Comparison Module

This file implements performance testing functionality to compare
the search efficiency between hash table and linear array search.

"""
import time
import random

class PerformanceComparator:
    # ==========================================================================
    # INITIALIZATION SECTION - DATA STRUCTURE SETUP
    # ==========================================================================
    def __init__(self, shop_storage):
        """
        Initialize PerformanceComparator with shop storage reference

        Args:
            shop_storage: Reference to the main shop storage system using hash table
        """
        self.shop_storage = shop_storage
        self.array_storage = []  # Array for linear search comparison
        self.all_product_ids = []  # Store all product IDs for test case generation

    # ==========================================================================
    # DATA LOADING SECTION - PREPARING TEST DATA
    # ==========================================================================
    def load_data_for_comparison(self):
        """Load the same data into both hash table and array for fair comparison"""
        all_products = self.shop_storage.get_all_products()
        for product in all_products:
            self.array_storage.append(product)
            self.all_product_ids.append(product.product_id)

        print(f"Loaded {len(self.array_storage)} products for performance comparison")

    # ==========================================================================
    # SEARCH IMPLEMENTATION SECTION - BOTH METHODS
    # ==========================================================================
    def hash_table_search(self, product_id):
        """Search using hash table - O(1) average case complexity"""
        return self.shop_storage.get_product(product_id)

    def array_linear_search(self, product_id):
        """Search using linear array search - O(n) worst case complexity"""
        for product in self.array_storage:
            if product.product_id == product_id:
                return product
        return None

    # ==========================================================================
    # PERFORMANCE TESTING SECTION - COMPARISON LOGIC
    # ==========================================================================
    def compare_search_performance(self, search_times=1000):
        """
        Compare search performance between hash table and array linear search

        Args:
            search_times (int): Number of search operations to perform for testing

        Analysis:
        - Hash Table: O(1) average time complexity due to direct indexing via hash function
        - Array Linear Search: O(n) time complexity as it checks each element sequentially
        - Expected Result: Hash table should be significantly faster, especially with large datasets
        """
        print("\n" + "=" * 50)
        print("Performance Comparison Experiment")
        print("=" * 50)

        # Generate test cases with 80% existing IDs and 20% random IDs
        test_cases = []
        for _ in range(search_times):
            if random.random() > 0.2:  # 80% chance to search existing products
                product_id = random.choice(self.all_product_ids)
            else:  # 20% chance to search non-existent products
                product_id = f"BP{random.randint(100, 999)}"
            test_cases.append(product_id)

        # ==========================================================================
        # HASH TABLE SEARCH TESTING
        # ==========================================================================
        print("Testing hash table search...")
        hash_table_start = time.time()
        hash_table_results = []
        for product_id in test_cases:
            result = self.hash_table_search(product_id)
            hash_table_results.append(result)
        hash_table_end = time.time()
        hash_table_time = hash_table_end - hash_table_start

        # ==========================================================================
        # ARRAY LINEAR SEARCH TESTING
        # ==========================================================================
        print("Testing array linear search...")
        array_start = time.time()
        array_results = []
        for product_id in test_cases:
            result = self.array_linear_search(product_id)
            array_results.append(result)
        array_end = time.time()
        array_time = array_end - array_start

        # ==========================================================================
        # RESULTS ANALYSIS SECTION
        # ==========================================================================
        print("\n" + "=" * 50)
        print("Performance Comparison Results")
        print("=" * 50)
        print(f"Test data volume: {search_times} searches")
        print(f"Total products: {len(self.array_storage)}")
        print(f"Hash table search time: {hash_table_time:.6f} seconds")
        print(f"Array linear search time: {array_time:.6f} seconds")
        print(f"Performance improvement: {array_time / hash_table_time:.2f} times")

        # Verify both methods return the same results
        results_match = all(h == a for h, a in zip(hash_table_results, array_results))
        print(f"Search result consistency: {results_match}")

        # ==========================================================================
        # PERFORMANCE ANALYSIS EXPLANATION
        # ==========================================================================
        print("\n" + "=" * 50)
        print("Performance Analysis")
        print("=" * 50)
        print("Hash Table Advantages:")
        print("- O(1) average time complexity for search operations")
        print("- Direct access via hash function computation")
        print("- Performance remains constant regardless of dataset size")
        print("- Ideal for frequent search operations")

        print("\nArray Linear Search Limitations:")
        print("- O(n) time complexity in worst case")
        print("- Must check each element sequentially")
        print("- Performance degrades linearly with dataset size")
        print("- Suitable only for small datasets or infrequent searches")

        print(f"\nConclusion: Hash table is {array_time / hash_table_time:.2f}x faster ")
        print("for search operations in this inventory system.")

        return hash_table_time, array_time