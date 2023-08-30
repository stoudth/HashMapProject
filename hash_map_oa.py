# Name: Hailey Stoudt
# OSU Email: stoudth@oregonstate.edu
# Course: CS261 - Data Structures - Section 400
# Assignment: Assignment 6- HashMap (Portfolio Assignment)
# Due Date: 6/9/2023
# Description: Contains HashMap class and its associated methods that utilizes an underlying Dynamic Array.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and value as a parameter and hashes it into the correct location
        in the HashMap. If it determines that the load factor is 0.5 or greater, it will
        resize the Hashmap. Utilizes open addressing with quadratic probing if hashed index
        is already occupied.
        """
        #Checks if resize is necessary
        if self._size/self._capacity >= 0.5:
            self.resize_table(self._capacity*2)
        #Initializes variables to determine final hashed index
        index = self._hash_function(key) % self._capacity
        quadratic_prob_index = 0
        quadratic_num = 1
        tombstone = None
        #Checks that initial hashed index does not work
        if self._buckets[index] is not None:
            if self._buckets[index].is_tombstone is False:
                if self._buckets[index].key != key:
                    #iterates through list until a matching key or an empty slot is reached
                    while quadratic_prob_index >= 0:
                        #Initializes variables for quadratic probing
                        quadratic_prob_index = (index + quadratic_num**2) % self._capacity
                        bucket = self._buckets[quadratic_prob_index]
                        #When an empty slot is reached, assigns final index to either that slot or previously visited tombstone
                        if bucket is None:
                            if tombstone is None:
                                index = quadratic_prob_index
                            else:
                                index = tombstone
                            quadratic_prob_index = -1
                        #If matching key in active HashEntry is found, then reassigns the value to new value
                        elif self._buckets[quadratic_prob_index].key == key and self._buckets[quadratic_prob_index].is_tombstone is False:
                            self._buckets[quadratic_prob_index].value = value
                            return
                        #If the first tombstone is reached, index is saved for later - keeps searching for an existing key
                        elif bucket.is_tombstone is True and tombstone is None:
                            tombstone = quadratic_prob_index
                        quadratic_num += 1
                #If initial index is the key then reassigns value
                elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                    self._buckets[index].value = value
                    return
        #Adds new HashEntry at final index and increments size
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Takes no parameters and returns the current load factor of the table.
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns the current number of empty buckets in the hash table.
        """
        #Initializes variables for list walk through
        counter = 0
        hash_length = 0
        #Walks through each index of list
        while hash_length < self._capacity:
            #Adds to empty bucket counter if an index is empty or tombstone
            if self._buckets[hash_length] is None or self._buckets[hash_length].is_tombstone is True:
                counter += 1
            hash_length += 1
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity as a parameter. If the new capacity is less than the
        current number of elements in the table, then the method does nothing. If
        the new capacity is not prime, it finds the next highest prime number. It
        then rehashes all elements back into the hash table.
        """
        #Checks that new capacity is greater than number of elements
        if new_capacity < self._size:
            return
        #Check if new capacity is prime and if not makes it prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        #Initializes variables for rehashing
        old_map = self._buckets
        self._buckets = DynamicArray()
        for num in range(new_capacity):
            self._buckets.append(None)
        size = self._size
        self._size = 0
        self._capacity = new_capacity
        length = 0
        #Walks through prior hash map and rehashes keys and values into new hash map
        while size > 0:
            entry = old_map[length]
            if entry is not None:
                if entry.is_tombstone is False:
                    key = entry.key
                    value = entry.value
                    self.put(key, value)
                    size -= 1
            length += 1

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter and returns its associated
        value if it is in the hash table. If it does not exist
        in the hash table, then None is returned.
        """
        #Initialized variables to locate key
        index = self._hash_function(key) % self._capacity
        index_copy = index
        prob_num = 1
        #Walks through hash table using quadratic probing until key is found or Empty bucket is found
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                if self._buckets[index].is_tombstone is False:
                    return self._buckets[index].value
            index = (index_copy+prob_num**2) % self._capacity
            prob_num += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter and return True if the key is in the
        hash table and False if it is not.
        """
        if self._size != 0:
            #Initializes variables to locate key
            index = self._hash_function(key) % self._capacity
            index_copy = index
            prob_num = 1
            #Walks through hash map until key is found or empty index is located
            while self._buckets[index] is not None:
                if self._buckets[index].key == key:
                    if self._buckets[index].is_tombstone is False:
                        return True
                index = (index_copy+prob_num**2) % self._capacity
                prob_num += 1
        return False

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter and removes it from the
        hash map.
        """
        #Initializes variables to search hash map for key
        index = self._hash_function(key) % self._capacity
        index_copy = index
        prob_num = 1
        #Searches Hash Map until key is found or an empty index is found
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                if self._buckets[index].is_tombstone is False:
                    #Updates tombstone data member and decrements size
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return
            index = (index_copy+prob_num**2) % self._capacity
            prob_num += 1

    def clear(self) -> None:
        """
        Takes no parameters and clears the current hash map.
        Capacity remains the same.
        """
        self._buckets = DynamicArray()
        for num in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters and returns a Dynamic Array Filled with
        tuples containing all the key value pairs in the current hash map.
        """
        #Initializes variables to walk through Hash Map to obtain key/value pairs
        keys_and_values_array = DynamicArray()
        size = self._size
        length = 0
        #Walks through hash map and add any active key/value pairs to Dynamic Array
        while size > 0:
            bucket = self._buckets[length]
            if bucket is not None:
                if bucket.is_tombstone is False:
                    keys_and_values_array.append((bucket.key, bucket.value))
                    size -= 1
            length += 1
        return keys_and_values_array

    def __iter__(self):
        """
        Creates the iterator for loop.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Obtains the next active value and advances the iterator.
        This will skip over empty indices and tombstone values.
        """
        stop = 0
        #Walkthrough list until it finds an active index or it reaches the end of the list
        while stop == 0:
            if self._index >= self._capacity:
                raise StopIteration
            value = self._buckets[self._index]
            if value is None:
                self._index += 1
            elif value.is_tombstone is True:
                self._index += 1
            else:
                stop = -1
        self._index += 1
        return value
