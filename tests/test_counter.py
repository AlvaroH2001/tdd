"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    # Just adding in this comment to be able to commit again
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Test updating a counter increments its value"""
        # Step 1: Create a counter
        self.client.post('/counters/test_update_counter')

        # Step 2: Update the counter and ensure successful return code
        update_response = self.client.put('/counters/test_update_counter')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_read_a_counter(self):
        """Test reading a counter returns the correct value"""
        # Step 1: Create a counter
        self.client.post('/counters/test_read_counter')

        # Step 2: Read the counter
        read_response = self.client.get('/counters/test_read_counter')
        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(read_response.json, {'test_read_counter': 0})
