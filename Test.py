import unittest
import SelvaDB
import os
import json
import time

class TestSum(unittest.TestCase):
    db = SelvaDB.SelvaDB("testdb.txt")

    def test_fileCreated(self):
        self.assertEqual(os.path.isfile("testdb.txt"),True)
    
    def test_keySize(self):
        self.assertEqual(self.db.add("selva",{"college":"TCE", "branch":"CSE","ttl":100}),None)
        with self.assertRaises(Exception) as excep:
            self.db.add("abcdefghijklmnopqrstabcdefghijklmnopqrst",{"college":"psg"})
    
    def test_keyExists(self):
        self.db.add("siva",{"college":"TCE", "branch":"CSE","ttl":100})
        with self.assertRaises(Exception) as excep:
            self.db.add("siva",{"college":"TCE", "branch":"CSE","ttl":100})

    def test_readFromDB(self):
        value = {"college":"CEG", "branch":"EEE","ttl":100}
        self.db.add("ram",value)
        valueResp = self.db.get("ram")
        self.assertEqual(valueResp,value)
        self.assertTrue(isinstance(valueResp,dict))

    def test_delete(self):
        value = {"college":"VIT", "branch":"MECH","ttl":100}
        self.db.add("varun",value)
        self.db.delete("varun")
        with self.assertRaises(Exception) as excep:
            self.db.get("varun")

    def test_timeToLive(self):
        value = {"college":"IIMC", "branch":"MECH","ttl":2}
        self.db.add("rachit",value)
        self.assertEqual(self.db.get("rachit"),value)
        time.sleep(3)
        with self.assertRaises(Exception) as excep:
            self.db.get("rachit")


if __name__ == '__main__':
    unittest.main()