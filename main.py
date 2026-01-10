from Stock import Stock
from Portfolio import Portfolio

if __name__ == "__main__":
    # Testing Stock class
    AAPL = Stock("aapl")
    META = Stock("meta")
    print(AAPL.symbol)                 # AAPL
    print(AAPL.current_price(259.37))  # 259.37

    # Testing portfolio class
    portfolio = Portfolio(
        positions={AAPL: 8, META: 2},
        target_allocations={META: 0.40, AAPL: 0.60},
    )

    print(portfolio.positions)
    print(portfolio.target_allocations)
