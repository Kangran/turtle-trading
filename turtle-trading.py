# https://www.quantopian.com/help#ide-module-import
from talib import ATR

def initialize(context):
    """
    Set up algorithm.
    """
    # https://www.quantopian.com/help#available-futures
    markets = [
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
        markets
    )
    
    assert(len(context.markets) == 16)

def before_trading_start(context, data):
    """
    Process data before every market open.
    """
    set_markets(context)
    get_prices(context, data)
    validate_prices(context)
    compute_volatility(context)

def handle_data(context, data):
    """
    Process data every minute.
    """
    pass

def set_markets(context):
    """
    Set markets for trading.
    """
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

def validate_prices(context):
    """
    Validate prices.
    """
    context.prices.dropna(axis=2, inplace=True)

def compute_volatility(context):
    """
    Compute volatility, or N.
    """
    pass