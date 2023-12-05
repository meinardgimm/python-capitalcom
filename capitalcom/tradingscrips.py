import statistics

class Scripts():

    def simpletest(prices):
        if not prices:
            return 0  # Return 0 if the list is empty

        avg_price = statistics.mean(prices)
        above_avg_count = sum(1 for price in prices if price > avg_price)
        below_avg_count = len(prices) - above_avg_count

        if above_avg_count > below_avg_count:
            return "HOLD"
        else:
            return "HOLD"
        

    def GPT_intuitive(prices):
        # Check if we have enough data points
        if len(prices) < 100:
            return "HOLD"  # Not enough data for a decision, hold position

        # Calculate the short-term (fast) moving average (e.g., 20 minutes)
        short_ma = sum(prices[-20:]) / 20

        # Calculate the long-term (slow) moving average (e.g., 50 minutes)
        long_ma = sum(prices[-50:]) / 50

        # Generate trading signals based on the moving average crossover
        if short_ma > long_ma:
            return "BUY"  # Short-term MA crosses above long-term MA, generate a buy signal
        elif short_ma < long_ma:
            return "SELL"  # Short-term MA crosses below long-term MA, generate a sell signal
        else:
            return "HOLD"  # No crossover, hold position


