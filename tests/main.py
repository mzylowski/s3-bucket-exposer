import unittest

if __name__ == "__main__":
    print("Starting tests scenarios...")
    loader = unittest.TestLoader()
    tests = loader.discover('scenarios')
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(tests)
    print(":)") if result.wasSuccessful() else print(":(")
