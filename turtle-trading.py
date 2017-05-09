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

def handle_data(context, data):
    """
    Process data every minute.
    """
    log.info(context.markets)