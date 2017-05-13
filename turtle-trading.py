# https://www.quantopian.com/help#ide-module-import
from talib import ATR

def initialize(context):
    """
    Initialize algorithm.
    """
    # https://www.quantopian.com/help#available-futures
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
    schedule_function(
        func=get_historical_prices,
        time_rule=time_rules.market_open(minutes=1)
    )
    schedule_function(
        func=validate_prices,
        time_rule=time_rules.market_open(minutes=1)
    )
    
    if context.is_debug:
        assert(len(context.symbols) == 16)

def handle_data(context, data):
    """
    Process data every minute.
    """
    pass
    # if context.markets is not None:
    #     current_prices = data.current(
    #         context.markets,
    #         fields=['high', 'low', 'close']
    #     )
    
    # context.prices = context.prices.transpose(1, 2, 0)
    # context.prices[get_datetime()] = current_prices
    
    # compute_average_true_range(context)

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
            
            log.info(
                '%s stopped trading. Dropped.'
                % market.root_symbol
            )
            
    if context.is_debug:
        assert(len(context.markets) == 14)

def get_historical_prices(context, data):
    """
    Get historical prices.
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
        assert(context.prices.shape == (3, 22, 14))

def validate_prices(context, data):
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
    
    if dropped_markets:
        log.info(
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

def compute_average_true_range(context):
    """
    Compute average true range, or N.
    """
    pass