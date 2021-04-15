from tests.download_trade_data_tests import verify_trade_data_authenticity, verify_trade_data_downloads
from tests.get_aggregate_bars_tests import verify_tick_interval_bars

print("Running tests!")

print("Running verify_trade_data_downloads...")
verify_trade_data_downloads()
print("Success!")

print("Running verify_trade_data_authenticity...")
verify_trade_data_authenticity()
print("Success!")

print("Running verify_tick_interval_bars...")
verify_tick_interval_bars()
print("Success!")
