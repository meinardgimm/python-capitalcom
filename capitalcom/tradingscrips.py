import statistics
import backtrader as bt

# include cases for 
# return 'CLOSE' | return 'BUY' | return 'SELL' | return 'nix machen'

class Scripts():
     
    def AllAlerts(prices, positions, balance):
        if positions != []:
            for index in range(0,len(positions[0])):
                if prices['ticker'] == positions[0][index]:
                    open_positions = positions[1][index]
                    break
                else:
                    open_positions = 'NONE'
        else:
            open_positions = 'NONE'

        ma = pine_wma(prices['close'], length = 20)
        slope_period1 = 1
        slope_period2 = 3
        slope_period3 = 4
        slope1 = (ma[-1] - ma[-slope_period1]) / slope_period1 # these lines I 'fixed' from ma[0]
        slope2 = (ma[-1] - ma[-slope_period2]) / slope_period2
        slope3 = (ma[-1] - ma[-slope_period3]) / slope_period3
        if slope1 < 0 and open_positions == 'BUY':
            return 'CLOSE'
        elif slope1 > 0 and open_positions == 'SELL':
            return 'CLOSE'
        elif slope1 > 0 and slope2 > 0 and slope3 > 0 and open_positions == 'NONE' and balance > 5:
            return 'BUY'
        elif slope1 < 0 and slope2 < 0 and slope3 < 0 and open_positions == 'NONE' and balance > 5:
            return 'SELL'
        else: 
            return 'Nix machen'

def pine_wma(source, length):
# so far just gives out one single value. Need to make it a list.
    wma = []
    norm = 0.0
    total_sum = 0.0
    for i in range(length):
        weight = (length - i) * length
        norm += weight
        total_sum += source[i] * weight
        wma.append(total_sum / norm)
    return wma

def GPT_intuitive(prices, positions, balance):
    if positions != []:
        for index in range(0,len(positions[0])):
            if prices['ticker'] == positions[0][index]:
                open_positions = positions[1][index]
                break
            else:
                open_positions = 'NONE'
    else:
        open_positions = 'NONE'
    # Calculate the short-term (fast) moving average (e.g., 20 minutes)
    short_ma = sum(prices[-5:]) / 5
    # Calculate the long-term (slow) moving average (e.g., 50 minutes)
    long_ma = sum(prices[-10:]) / 10
    # Generate trading signals based on the moving average crossover
    if short_ma > long_ma and open_positions == 'NONE':
        return "BUY"  # Short-term MA crosses above long-term MA, generate a buy signal
    elif short_ma < long_ma and open_positions == 'NONE':
        return "SELL"  # Short-term MA crosses below long-term MA, generate a sell signal
    elif short_ma > long_ma and open_positions == 'SELL':
        return 'CLOSE'
    elif short_ma < long_ma and open_positions == 'BUY':
        return 'CLOSE'
    else:
        return "Nix machen"  # No crossover, hold position