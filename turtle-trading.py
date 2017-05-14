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
        
        average_true_range = compute_average_true_range(
            context,
            context.markets[0]
        )

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

def compute_average_true_range(context, market):
    """
    Compute average true range, or N.
    """
    rolling_window = 21
    moving_average = 20
    
    return ATR(
        context.prices[market].high[-rolling_window:],
        context.prices[market].low[-rolling_window:],
        context.prices[market].close[-rolling_window:],
        timeperiod=moving_average
    )[-1]