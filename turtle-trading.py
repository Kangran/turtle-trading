def initialize(context):
    """
    Set up algorithm.
    """
    # https://www.quantopian.com/help#available-futures
    context.markets = [
        continuous_future('US'),
        continuous_future('TY'),
        continuous_future('SB'),
        continuous_future('SF'),
        continuous_future('BP'),
        continuous_future('JY'),
        continuous_future('CD'),
        continuous_future('SP'),
        continuous_future('ED'),
        continuous_future('TB'),
        continuous_future('GC'),
        continuous_future('SV'),
        continuous_future('HG'),
        continuous_future('CL'),
        continuous_future('HO'),
        continuous_future('HU')
    ]
    
    assert(len(context.markets) == 16)

def before_trading_start(context, data):
    """
    Process data before every market open.
    """
    set_markets(context)

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