from Stock import Stock, Order
from typing import Dict

class Portfolio:
    """
    Portfolio contains:
      - positions: {Stock -> shares}
      - target_allocations: {Stock -> weight}  (weights sum to 1.0)

    rebalance(prices):
      prices: dict[str, float] with latest price per symbol ({"AAPL": 200, ...})
      -> returns BUY/SELL orders to reach target allocation.
    """
    def __init__(
        self,
        positions: Dict[Stock, float],
        target_allocations: Dict[Stock, float],
    ):
        self.positions = {stock: float(shares) for stock, shares in positions.items()}
        self.target_allocations = {stock: float(w) for stock, w in target_allocations.items()}
        self._validate_target()

    def _validate_target(self) -> None:
        """
        Validate that target allocations are valid:
        - All weights must be positive
        - Weights must sum to 1.0
        
        Raises:
            ValueError: If weights are not all positive or don't sum to 1.0
        """
        for stock, weight in self.target_allocations.items():
            if weight <= 0:
                raise ValueError(f"Weight for {stock.symbol} must be positive, got {weight}")
        
        total_weight = sum(self.target_allocations.values())
        if not abs(total_weight - 1.0) < 1e-9:
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

    def rebalance(self, prices: Dict[str, float]) -> list[Order]:
        """
        Calculate orders to rebalance portfolio to target allocations.
        
        Args:
            prices: Dict mapping stock symbol to current price (e.g., {"AAPL": 200.5, ...})
        
        Returns:
            List of Order objects (BUY/SELL) to reach target allocations
        
        Raises:
            ValueError: If a required stock price is missing
        """
        # Calculate current portfolio value
        portfolio_value = 0.0
        for stock, shares in self.positions.items():
            if stock.symbol not in prices:
                raise ValueError(f"Missing price for {stock.symbol}")
            stock.current_price(prices[stock.symbol])   # Store last price
            portfolio_value += shares * prices[stock.symbol]
        
        if portfolio_value <= 0:
            raise ValueError("Portfolio value must be positive")
        
        orders = []
        
        # Calculate orders for each stock in target allocations
        for stock, target_weight in self.target_allocations.items():
            if stock.symbol not in prices:
                raise ValueError(f"Missing price for {stock.symbol}")
            
            price = prices[stock.symbol]
            current_shares = self.positions.get(stock, 0.0)
            
            # Calculate target value and shares needed
            target_value = target_weight * portfolio_value
            target_shares = target_value / price
            
            # Calculate difference
            shares_diff = target_shares - current_shares
            
            # Create order if there's a difference
            if abs(shares_diff) > 1e-9:
                side = "BUY" if shares_diff > 0 else "SELL"
                orders.append(Order(stock=stock, side=side, shares=abs(shares_diff)))
        
        return orders