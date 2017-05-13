# https://www.quantopian.com/help#ide-module-import
from talib import ATR

def initialize(context):
    """
    Initialize algorithm.
    """
    set_symbols(context)
    
    context.is_market_stale = True
    context.is_price_stale = True

def before_trading_start(context, data):
    """
    Set flags before market open.
    """
    context.is_market_stale = True
    context.is_price_stale = True

def handle_data(context, data):
    """
    Process data every minute.
    """
    if context.is_market_stale:
        validate_markets(context)
        context.is_market_stale = False
        
    if context.is_price_stale:
        get_historical_prices(context, data)
        validate_prices(context)
        context.is_price_stale = False
        
    current_prices = data.current(
        context.markets,
        fields=['high', 'low']
    )
    
    compute_average_true_range(context)

def set_symbols(context):
    """
    Set symbols.
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
            
    assert(len(context.symbols) == 16)

def validate_markets(context):
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
    
    assert(context.prices.shape == (3, 22, 14))

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
    
    if dropped_markets:
        log.info(
            'Null prices for %s. Dropped.'
            % ', '.join(dropped_markets)
        )
        
    context.markets = map(
        lambda market: continuous_future(market),
        validated_markets
    )

def compute_average_true_range(context):
    """
    Compute average true range, or N.
    """
    pass