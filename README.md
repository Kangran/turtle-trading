# turtle-trading
Profit using trend trading

# strategy
See https://github.com/vyq/turtle-trading/raw/master/the-original-turtle-trading-rules.pdf

# backtest
Parameters
- Start date: 2017-02-27
- End date: 2017-03-31
- Cash: USD 1,000,000
- Trading calendar: US Futures

Suppress null warnings after first log message: https://www.quantopian.com/posts/warn-numpy-slash-lib-slash-nanfunctions-dot-py-319-runtimewarning-all-nan-slice-encountered

# initialize
Set up algorithm. Executes at 1970-01-01 7 PM UTC-4. Intersect Quantopian futures universe with Turtle Trading markets. Set markets as continuous futures to allow access to a rolling window of futures contracts.

# before-trading-start
Process data before every market open. Executes at 8:45 AM UTC-4.

# handle-data
Process data every minute. Executes from 6:31 AM to 5 PM UTC-4.

# set-markets
Set markets for trading. Remove markets that stopped trading.

Universe: https://www.quantopian.com/help#available-futures

# get-prices
Get historical prices. Get high, low, and close. Get 22 daily bars for computing average true range.

# validate-prices
Drop markets with null prices.

# compute-average-true-range
Compute average true range, or N, using ATR in TA-Lib.

Average true range: https://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html
Modules: https://www.quantopian.com/help#ide-module-import

# who
- More people making money selling ways to make money trading than there are people actually making money trading
- Investigate sellers before taking advice or buying courses

# what
- Components of a complete trading system
    - Markets: What to buy or sell
        - High trading volume
        - Trend well
    - Position sizing: How much to buy or sell
        - Diversification
        - Money management
        - Risk limit
            - Single market: 4 units
            - Closely correlated markets: 6 units
            - Loosely correlated markets: 10 units
            - Single direction: 12 units
    - Entries: When to buy or sell
        - Exact price and market conditions to enter
        - Consistent in taking entry signals
    - Stops: When to get out of a losing position
        - Cut loss
        - Define point to get out before entering
        - Tighten stops based on 2 times volatility from previous fill price, or use 0.5 times volatility for each unit
    - Exits: When to get out of a winning position
        - Maintain discipline to exit
        - Do not exit early
    - Tactics: How to buy or sell
        - Do not place stop orders
        - Use limit orders
        - Wait for temporary price reversal before placing orders
        - If multiple signals
            - Rank markets that moved the most in terms of volatility
            - Long strongest market
            - Short weakest market
        - Do not roll over expiring contract unless breakout
        - Roll over into new contract month a few weeks before expiration, unless current position performs better
            - Review volume and open interest
        - Have discipline to follow the rules
- Further study
    - Trading psychology
    - Money management
    - Trading research
- Warning
    - Best advice comes from those who are not selling it and are making money trading

# reflect
Markets are fixed or dynamic
- Fixed markets allow consistency over time
- Dynamic markets generate ideas over time

Context has limitations
- Cannot get 3-dimensional array (3, 22, 14) in `handle_data`, though it was saved to context in `before_trading_start`