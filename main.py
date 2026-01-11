from Stock import Stock
from Portfolio import Portfolio

if __name__ == "__main__":
    # Testing Stock class
    AAPL = Stock("aapl")
    META = Stock("meta")
    print(AAPL.symbol)                 # AAPL
    print(AAPL.current_price(259.37))  # 259.37
    print(AAPL.get_current_price())

    # Testing portfolio class
    print("Testing portfolio class")
    print("Portfolio positions: {AAPL: 8, META: 2}")
    print("Portfolio allocations: {META: 0.40, AAPL: 0.60}")

    portfolio = Portfolio(
        positions={AAPL: 8, META: 2},
        target_allocations={META: 0.40, AAPL: 0.60},
    )

    # Testing rebalance
    # Let's assume the prices of APPL USD259.37 and META USD 653.06
    # The "order" will be printed, specifyng which to BUY or SELL and how many units
    print("Testing portfolio rebalance")
    print("Portfolio rebalance: {'AAPL': 259.37, 'META': 653.06}")
    orders = portfolio.rebalance({"AAPL": 259.37, "META": 653.06})
    for o in orders:
        print(o.stock.symbol, o.side, o.shares)