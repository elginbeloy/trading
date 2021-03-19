from tests.download_trade_data_tests import verify_trade_data_authenticity, verify_trade_data_downloads

print("Running tests!")

print("Running verify_trade_data_downloads...")
verify_trade_data_downloads()
print("Success!")

print("Running verify_trade_data_authenticity...")
verify_trade_data_authenticity()
print("Success!")
