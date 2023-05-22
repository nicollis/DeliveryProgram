from algorithms.linkedlist import LinkedList

class HashTable:
    _bucket_size = 61 # rule of thumb is to use a prime number between 1.5 and 2 times the number of expected entries

    def __init__(self, bucket_size=_bucket_size):
        self._bucket_size = bucket_size
        self._buckets = [ LinkedList() for _ in range(bucket_size)]

    def __str__(self):
        return "\n".join([str(bucket) for bucket in self._buckets if bucket.head is not None])

    # for our hash table we are going to expect the key to be the id of the object
    # however to create a well rounded hash function we will use the key as a string
    # in addition to the key as an integer. Providing two hashing methods allowing the
    # user to pass in either a string or an integer, for the option of a hash function that
    # will provide a highly unique hash value but cost O(n) time complexity where n is the length of the key;
    # or a hash function that will provide a less unique hash value but cost O(1) time complexity.
    # O(n) or O(1) time complexity based on the key type (string or integer)
    def _hash(self, key):
        if isinstance(key, str):
            hash_multiplier = 31
            hash_value = 0
            for char in key:
                # ord() returns an integer representing the Unicode character
                hash_value = (hash_value * hash_multiplier + ord(char)) % self._bucket_size
            return hash_value
        else:
          return key % self._bucket_size
    
    # O(n) where n is the number of hash collisions
    def get(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]
        try: 
          return bucket.get(key)
        except KeyError as e:
          # Catch the exception and re-raise it
          raise e
    
    # O(1)
    def append(self, key, data):
        index = self._hash(key)
        bucket = self._buckets[index]
        bucket.append(key, data)

    # O(n) where n is the number of hash collisions
    def update(self, key, data):
      index = self._hash(key)
      bucket = self._buckets[index]
      # we want to check if the key already exists in the bucket so we can update existing packages
      try:
        bucket.update(key, data)
      except KeyError as e:
        # Catch the exception and re-raise it
        raise e

    # O(n) where n is the number of hash collisions
    def remove(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]
        try:
          bucket.remove(key)
        except KeyError as e:
          # Catch the exception and re-raise it
          raise e