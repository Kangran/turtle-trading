from talib import ATR

def initialize(context):
    """
    Initialize algorithm.
    """
    context.symbols = [
        'BP',
        'CD',
        'CL',
        'ED',
        'GC',
        'HG',
        'HO',
        'HU',
        'JY',
        'SB',
        'SF',
        'SP',
        'SV',
        'TB',
        'TY',
        'US'
    ]
    context.markets = None
    context.prices = None
    context.contracts = None
    context.capital = context.portfolio.starting_cash
    context.capital_risk_per_trade = 0.01
    context.capital_multiplier = 2
    context.is_debug = True
    
    schedule_function(
        func=validate_markets,
        time_rule=time_rules.market_open(minutes=1)
    )
    
    if context.is_debug:
        assert(len(context.symbols) == 16)

def handle_data(context, data):
    """
    Process data every minute.
    """
    if context.markets is not None:
        get_prices(context, data)
        validate_prices(context)
        
        context.prices = context.prices.transpose(2, 1, 0)
        context.prices = context.prices.reindex()
        
        get_contracts(context, data)
        
        average_true_range = compute_average_true_range(
            context,
            context.markets[0]
        )
        
        dollar_volatility = compute_dollar_volatility(
            context,
            context.markets[0],
            average_true_range
        )
        
        profit = context.portfolio.portfolio_value\
            - context.portfolio.starting_cash
            
        if profit < 0:
            context.capital = context.portfolio.starting_cash\
                + profit\
                * context.capital_multiplier
                
        trade_size = context.capital\
            * context.capital_risk_per_trade\
            / dollar_volatility

def validate_markets(context, data):
    """
    Drop markets that stopped trading.
    """
    context.markets = map(
        lambda market: continuous_future(market),
        context.symbols
    )
    
    markets = context.markets[:]
    
    for market in markets:
        if market.end_date < get_datetime():
            context.markets.remove(market)
            
            if context.is_debug:
                log.debug(
                    '%s stopped trading. Dropped.'
                    % market.root_symbol
                )
            
    if context.is_debug:
        assert(len(context.markets) == 14)

def get_prices(context, data):
    """
    Get prices.
    """
    fields = ['high', 'low', 'close']
    bars = 22
    frequency = '1d'
    
    context.prices = data.history(
        context.markets,
        fields,
        bars,
        frequency
    )
    
    if context.is_debug:
        assert(context.prices.shape[0] == 3)
        assert(context.prices.shape[1] == 22)
        assert(context.prices.shape[2] > 8)

def validate_prices(context):
    """
    Drop markets with null prices.
    """
    context.prices.dropna(axis=2, inplace=True)
    
    validated_markets = map(
        lambda market: market.root_symbol,
        context.prices.axes[2]
    )
    
    markets = map(
        lambda market: market.root_symbol,
        context.markets
    )
    
    dropped_markets = list(
        set(markets) - set(validated_markets)
    )
    
    if context.is_debug and dropped_markets:
        log.debug(
            'Null prices for %s. Dropped.'
            % ', '.join(dropped_markets)
        )
        
    context.markets = map(
        lambda market: continuous_future(market),
        validated_markets
    )
    
    if context.is_debug:
        assert(context.prices.shape[0] == 3)
        assert(context.prices.shape[1] == 22)
        assert(context.prices.shape[2] > 8)

def get_contracts(context, data):
    """
    Get contracts.
    """
    fields = 'contract'
    
    context.contracts = data.current(
        context.markets,
        fields
    )
    
    if context.is_debug:
        assert(context.contracts.shape[0] > 8)

def compute_average_true_range(context, market):
    """
    Compute average true range, or N.
    """
    rolling_window = 21
    moving_average = 20
    
    average_true_range = ATR(
        context.prices[market].high[-rolling_window:],
        context.prices[market].low[-rolling_window:],
        context.prices[market].close[-rolling_window:],
        timeperiod=moving_average
    )[-1]
    
    if context.is_debug:
        assert(average_true_range > 0)
        
    return average_true_range

def compute_dollar_volatility(context, market, average_true_range):
    """
    Compute dollar volatility.
    """
    contract = context.contracts[market]
    
    dollar_volatility = contract.tick_size * average_true_range
    
    if context.is_debug:
        assert(dollar_volatility > 0)
        
    return dollar_volatility