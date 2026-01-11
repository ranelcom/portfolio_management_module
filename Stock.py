from dataclasses import dataclass
from typing import Literal

Side = Literal["BUY", "SELL"]

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper().strip()
        self._current_price = 0.0

    def __post_init__(self) -> None:
        # Normalize symbol to avoid inconsistencies (meta vs META).
        object.__setattr__(self, "symbol", self.symbol.upper().strip())

    def get_current_price(self) -> float:
        return self._current_price
    
    def current_price(self, last_available_price: float) -> float:
        """
        Returns the "current price" based on the last available price.
        """
        if last_available_price <= 0:
            raise ValueError(
                f"Invalid price for {self.symbol}: {last_available_price}. "
                "Must be > 0."
            )
        self._current_price = float(last_available_price)
        return self._current_price

@dataclass(frozen=True)
class Order:
    stock: Stock
    side: Side
    shares: float