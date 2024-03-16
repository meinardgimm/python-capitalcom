import statistics
import backtrader as bt

class Scripts():

    def simpletest(prices, positions):
        # initializing 'open_positions' as 'SELL', 'BUY' an 'NONE' if no trade is open
        for index in range(0,len(positions[0])):
            if prices['ticker'] == positions[0][index]:
                open_positions = positions[1][index]
            else:
                open_positions = 'NONE'

        avg_price = statistics.mean(prices['low'])
        prices = prices['low']
        above_avg_count = sum(1 for price in prices if price > avg_price)
        below_avg_count = len(prices) - above_avg_count

        if above_avg_count > below_avg_count:
            return "HOLD"
        else:
            return "HOLD"
        

    def GPT_intuitive(prices, positions):
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
        
    def AllAlerts(prices, positions):
        if positions != []:
            for index in range(0,len(positions[0])):
                if prices['ticker'] == positions[0][index]:
                    open_positions = positions[1][index]
                else:
                    open_positions = 'NONE'
        else:
            open_positions = 'NONE'

        ma = pine_wma(prices['close'], length = 20)
        slope_period1 = 1
        slope_period2 = 3
        slope_period3 = 4
        slope1 = (ma - ma(-slope_period1)) / slope_period1
        slope2 = (ma - ma(-slope_period2)) / slope_period2
        slope3 = (ma - ma(-slope_period3)) / slope_period3
        if slope1 < 0 and open_positions == 'BUY':
            return 'CLOSE'
        elif slope1 > 0 and open_positions == 'SELL':
            return 'CLOSE'
        elif slope1 > 0 and slope2 > 0 and slope3 > 0 and open_positions == 'NONE':
            return 'BUY'
        elif slope1 < 0 and slope2 < 0 and slope3 < 0 and open_positions == 'NONE':
            return 'SELL'

def pine_wma(source, length):
    norm = 0.0
    total_sum = 0.0
    for i in range(length):
        weight = (length - i) * length
        norm += weight
        total_sum += source[i] * weight
    return total_sum / norm