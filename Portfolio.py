from Stock import Stock, Order
from typing import Dict

class Portfolio:
    """
    Portfolio contiene:
      - positions: {Stock -> shares}
      - target_allocations: {Stock -> weight}  (pesos suman 1.0)

    rebalance(prices):
      prices: dict[str, float] con último precio por símbolo ({"AAPL": 200, ...})
      -> retorna órdenes BUY/SELL para llegar a la asignación objetivo.
    """
    def __init__(
        self,
        positions: Dict[Stock, float],
        target_allocations: Dict[Stock, float],
    ):
        self.positions = {stock: float(shares) for stock, shares in positions.items()}
        self.target_allocations = {stock: float(w) for stock, w in target_allocations.items()}
        #self._validate_target()