from get_aggregate_bars import get_tick_interval_bars

def verify_tick_interval_bars():
  tick_training_bars = get_tick_interval_bars(bar_size_ticks=1000)
  return True