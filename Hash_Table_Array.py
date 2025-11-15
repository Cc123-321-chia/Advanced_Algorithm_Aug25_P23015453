"""
Question 1: Hash Table

This file implements a hash table data structure that uses separate chaining
for collision resolution. The hash table uses an array of lists (buckets) to
store key-value pairs. It provides insert, search, update, and deletion operations.

"""

class HashTableArray:
    # ==========================================================================
    # ENTRY CLASS SECTION
    # ==========================================================================
    class Entry:
        """Inner class to represent key-value pairs in the hash table"""
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, capacity=100):
        # Initialize hash table with specified capacity
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # Array of buckets (lists)
        self.size = 0  # Track number of elements
        self.insert_order = []  # Maintain insertion order for iteration

    # ==========================================================================
    # HASH FUNCTION SECTION
    # ==========================================================================
    def _hash(self, key):
        """Compute hash value for a given key and map to array index"""
        return hash(key) % self.capacity

    # ==========================================================================
    # INSERT OPERATIONS SECTION (ADD NEW PRODUCT)
    # ==========================================================================
    def insert(self, key, value):
        """Insert or update an entry - if key exists, update value"""
        index = self._hash(key)
        bucket = self.table[index]

        # Search for existing key in bucket
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                # Also update in insert_order to maintain consistency
                for order_entry in self.insert_order:
                    if order_entry.key == key:
                        order_entry.value = value
                        break
                return "updated"  # Return status indicating update

        # Key not found, insert new entry
        new_entry = self.Entry(key, value)
        bucket.append(new_entry)
        self.insert_order.append(new_entry)
        self.size += 1
        return "inserted"  # Return status indicating new insertion

    # ==========================================================================
    # UPDATE OPERATIONS SECTION (EDIT PRODUCT)
    # ==========================================================================
    def update(self, key, value):
        """Explicitly update an existing entry (returns True if updated)"""
        index = self._hash(key)
        bucket = self.table[index]

        for entry in bucket:
            if entry.key == key:
                entry.value = value
                # Also update in insert_order to maintain consistency
                for order_entry in self.insert_order:
                    if order_entry.key == key:
                        order_entry.value = value
                        break
                return True  # Successfully updated

        return False  # Key not found

    # ==========================================================================
    # DELETE OPERATIONS SECTION （DELETE PRODUCT)
    # ==========================================================================
    def delete(self, key):
        """Delete an entry by key, return True if deleted, False if not found"""
        index = self._hash(key)
        bucket = self.table[index]

        # Search for key in bucket
        for i, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(i)  # Remove from bucket
                # Remove from insert_order to maintain consistency
                for j, order_entry in enumerate(self.insert_order):
                    if order_entry.key == key:
                        self.insert_order.pop(j)
                        break
                self.size -= 1
                return True  # Successfully deleted

        return False  # Key not found

    # ==========================================================================
    # SEARCH OPERATIONS SECTION (SEARCH PRODUCT BY ID)
    # ==========================================================================
    def search(self, key):
        """Search for a specific product by key/id and return its value"""
        index = self._hash(key)
        bucket = self.table[index]

        for entry in bucket:
            if entry.key == key:
                return entry.value  # Return product details if found
        return None  # Product not found

    # ==========================================================================
    # BULK DATA RETRIEVAL SECTION (SEARCH/GET ALL PRODUCTS)
    # ==========================================================================
    def get_all_entries(self):
        """Get all product entries with complete details (key-value pairs)"""
        return self.insert_order.copy()

    def get_all_values(self):
        """Get all product values/details (product information only)"""
        return [entry.value for entry in self.insert_order]

    def get_all_keys(self):
        """Get all product IDs/keys (product identifiers only)"""
        return [entry.key for entry in self.insert_order]

    # ==========================================================================
    # UTILITY METHODS SECTION
    # ==========================================================================
    def __len__(self):
        """Return the number of elements in the hash table"""
        return self.size
