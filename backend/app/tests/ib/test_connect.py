from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook


def test_connect() -> None:
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)

    contract = Forex('EURUSD')
    bars = ib.reqHistoricalData(
        contract, endDateTime='', durationStr='30 D',
        barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

    # convert to pandas dataframe (pandas needs to be installed):
    df = util.df(bars)
    print(df)
