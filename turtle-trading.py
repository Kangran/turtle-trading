# https://www.quantopian.com/help#ide-module-import
from talib import ATR

def initialize(context):
    """
    Set up algorithm.
    """
    set_markets(context)
    schedule_function(
        func=get_prices,
        time_rule=time_rules.market_open(
            hours=0,
            minutes=1
        )
    )

def before_trading_start(context, data):
    """
    Process data before market open.
    """
    pass

def handle_data(context, data):
    """
    Process data every minute.
    """
    compute_average_true_range(context)

def set_markets(context):
    """
    Set markets for trading.
    """
    # https://www.quantopian.com/help#available-futures
    symbols = [
        'US',
        'TY',
        'SB',
        'SF',
        'BP',
        'JY',
        'CD',
        'SP',
        'ED',
        'TB',
        'GC',
        'SV',
        'HG',
        'CL',
        'HO',
        'HU'
    ]
    
    context.markets = map(
        lambda market: continuous_future(market),
        symbols
    )
    
    markets = context.markets[:]
    
    for market in markets:
        if market.end_date < get_datetime():
            context.markets.remove(market)
            
            log.info(
                '%s stopped trading. Deleted from markets.'
                % market.root_symbol
            )
            
    assert(len(context.markets) == 14)

def get_prices(context, data):
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
    
    validate_prices(context)

def validate_prices(context):
    """
    Validate prices.
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
            'Null prices for %s. Dropped from prices.'
            % ', '.join(dropped_markets)
        )

def compute_average_true_range(context):
    """
    Compute average true range, or N.
    """
    pass