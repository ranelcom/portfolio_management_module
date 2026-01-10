from dataclasses import dataclass
from typing import Literal

Side = Literal["BUY", "SELL"]

@dataclass(frozen=True)
class Stock:
    """
    dataclass Stock. Uso un dataclass porque en realidad una accion es un contenedor de datos
    con un poco de validacion. Metodo current_price.
    """
    symbol: str

    def __post_init__(self) -> None:
        # Normalizamos el símbolo para evitar inconsistencias (meta vs META).
        object.__setattr__(self, "symbol", self.symbol.upper().strip())

    def current_price(self, last_available_price: float) -> float:
        """
        Retorna el "precio actual" basado en el último precio disponible.
        """
        if last_available_price <= 0:
            raise ValueError(
                f"Precio inválido para {self.symbol}: {last_available_price}. "
                "Debe ser > 0."
            )
        return float(last_available_price)

@dataclass(frozen=True)
class Order:
    stock: Stock
    side: Side
    shares: float