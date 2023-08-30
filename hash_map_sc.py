# Name: Hailey Stoudt
# OSU Email: stoudth@oregonstate.edu
# Course: CS261 - Data Structures - Section 400
# Assignment: Assignment 6- HashMap (Portfolio Assignment)
# Due Date: 6/9/2023
# Description: Contains HashMap class with its associated methods that utilized an
#              underlying linked list.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Takes a key and value as parameters and add them to the hashtable.
        If the hash table's load factor is 1 or greater, it resizes the hash table accordingly.
        """
        #Resizes hash table if load factor is 1 or greater
        if self._size/self._capacity >= 1:
            self.resize_table(self._capacity*2)
        #Locates where key goes in hash table
        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]
        #Checks if key already exists in order to replace value
        match = bucket.contains(key)
        if match is not None:
            match.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns how many buckets in a hash table
        are empty.
        """
        #Initialized variables
        counter = 0
        hash_length = self._capacity-1
        #Walks through each bucket in table and if it's length is 0 increments counter by 1
        while hash_length >= 0:
            if self._buckets[hash_length].length() == 0:
                counter += 1
            hash_length -= 1
        return counter

    def table_load(self) -> float:
        """
        Takes no parameters and returns the current load factor of the hashtable.
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Takes no parameters and clear the hashtable of all current contents. The
        hash table's capacity does not change.
        """
        #Resets dynamic array, linked lists, and size.
        self._buckets = DynamicArray()
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes the new capacity as a parameter and resizes the hashtable accordingly.
        If the new capacity is less than 1, the method does nothing.
        If the new capacity is not prime, it finds the next prime number after that number. It then
        rehashes all key's into the newly resized hashtable.
        """
        #Does nothing if new capacity is less than 1
        if new_capacity < 1:
            return
        #Makes capacity the next close prime if it is not prime already
        if not self._is_prime(new_capacity):
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
        #Gets all keys and values from table
        key_value_pairs = self.get_keys_and_values()
        #Resets table to resized table
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        for num in range(new_capacity):
            self._buckets.append(LinkedList())
        #Rehashes all elements in table
        for num in range(key_value_pairs.length()):
            key, value = key_value_pairs[num]
            self.put(key, value)

    def get(self, key: str):
        """
        Takes a key as a parameter and returns its associated value if it
        is in the hash table. If it does not exist, method returns None.
        """
        #Initializes variables
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #Gets key's value if it exists and returns accordingly
        match = bucket.contains(key)
        if match:
            return match.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter and return True if the key exists
        in the hash table and False if it doesn't.
        """
        if self._size != 0:
            #Initializes variables
            index = self._hash_function(key) % self._capacity
            bucket = self._buckets[index]
            #checks if a match is found and returns accordingly
            match = bucket.contains(key)
            if match:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter and removes it from the hash table if it
        exists. Nothing is returned.
        """
        #Initializes variables
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #Removes key and decrements size
        match = bucket.remove(key)
        if match:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters and returns a dynamic array containing tuples of the keys and values
        from the hash table.
        """
        #Initializes variables
        keys_and_values_array = DynamicArray()
        length = self._capacity-1
        size = self._size
        #Walks through each bucket while all elements have not been visitd
        while size > 0:
            bucket = self._buckets[length]
            #Checks that bucket is not empty and appends node values to return array
            if bucket.length() != 0:
                for node in bucket:
                    if node is not None:
                        keys_and_values_array.append((node.key, node.value))
                        size -= 1
            length -= 1
        return keys_and_values_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a Dynamic array as a parameter and determines the mode values of it
    by using a HashMap. Returns a tuple containing a Dynamic Array of the mode
    values and then their frequency.
    """
    # HashMap given by skeleton code + Initializes variables to identify mode
    map = HashMap()
    element_array = DynamicArray()
    mode = 1
    #Walk through passed Dynamic Array - Element added to HashMap - Element is key and Frequency is value
    for index in range(da.length()):
        value = 1
        match = map.get(da[index])
        #If element in Hash Map, increments element's current value to compare to mode - Updates mode if necessary
        if match:
            value += match
            if value > mode:
                mode = value
        #If element not in Hash Map, adds to element_array - Tracks each unique element
        else:
            element_array.append(da[index])
        map.put(da[index], value)
    mode_key_array = DynamicArray()
    #Walk through element_array which holds each unique value from the passed array and gets its frequency value
    for index in range(element_array.length()):
        match = map.get(element_array[index])
        #If the elements frequency is equal to the calculated mode, it is appended to the return Dynamic Array
        if match == mode:
            mode_key_array.append(element_array[index])
    return mode_key_array, mode

