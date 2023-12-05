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
        



