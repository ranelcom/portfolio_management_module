import pytest
from Stock import Stock, Order
from Portfolio import Portfolio


class TestStock:
    """Unit tests for Stock class"""
    
    def test_stock_creation(self):
        """Test basic stock creation"""
        stock = Stock("AAPL")
        assert stock.symbol == "AAPL"
        assert stock.get_current_price() == 0.0
    
    def test_stock_symbol_normalization(self):
        """Test that symbol is normalized to uppercase and stripped"""
        stock = Stock("  aapl  ")
        assert stock.symbol == "AAPL"
    
    def test_current_price_valid(self):
        """Test setting current price with valid value"""
        stock = Stock("AAPL")
        price = stock.current_price(150.5)
        assert price == 150.5
        assert stock.get_current_price() == 150.5
    
    def test_current_price_invalid_zero(self):
        """Test that zero price raises ValueError"""
        stock = Stock("AAPL")
        with pytest.raises(ValueError, match="Invalid price"):
            stock.current_price(0)
    
    def test_current_price_invalid_negative(self):
        """Test that negative price raises ValueError"""
        stock = Stock("AAPL")
        with pytest.raises(ValueError, match="Invalid price"):
            stock.current_price(-50.0)
    
    def test_current_price_multiple_updates(self):
        """Test updating current price multiple times"""
        stock = Stock("GOOGL")
        stock.current_price(2800.0)
        assert stock.get_current_price() == 2800.0
        stock.current_price(2900.0)
        assert stock.get_current_price() == 2900.0


class TestPortfolio:
    """Unit tests for Portfolio class"""
    
    @pytest.fixture
    def sample_stocks(self):
        """Create sample stocks for testing"""
        return {
            "AAPL": Stock("AAPL"),
            "GOOGL": Stock("GOOGL"),
            "MSFT": Stock("MSFT"),
        }
    
    def test_portfolio_creation_valid(self, sample_stocks):
        """Test valid portfolio creation"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: 1.0}
        portfolio = Portfolio(positions, allocations)
        assert sample_stocks["AAPL"] in portfolio.positions
        assert portfolio.positions[sample_stocks["AAPL"]] == 10.0
    
    def test_validate_target_negative_weight(self, sample_stocks):
        """Test that negative weights raise ValueError"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: -0.5}
        with pytest.raises(ValueError, match="must be positive"):
            Portfolio(positions, allocations)
    
    def test_validate_target_zero_weight(self, sample_stocks):
        """Test that zero weight raises ValueError"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: 0.0}
        with pytest.raises(ValueError, match="must be positive"):
            Portfolio(positions, allocations)
    
    def test_validate_target_sum_not_one(self, sample_stocks):
        """Test that weights not summing to 1.0 raise ValueError"""
        positions = {
            sample_stocks["AAPL"]: 10.0,
            sample_stocks["GOOGL"]: 5.0,
        }
        allocations = {
            sample_stocks["AAPL"]: 0.4,
            sample_stocks["GOOGL"]: 0.4,  # Sums to 0.8, not 1.0
        }
        with pytest.raises(ValueError, match="must sum to 1.0"):
            Portfolio(positions, allocations)
    
    def test_validate_target_valid_sum(self, sample_stocks):
        """Test valid weights that sum to 1.0"""
        positions = {
            sample_stocks["AAPL"]: 10.0,
            sample_stocks["GOOGL"]: 5.0,
        }
        allocations = {
            sample_stocks["AAPL"]: 0.6,
            sample_stocks["GOOGL"]: 0.4,
        }
        portfolio = Portfolio(positions, allocations)
        assert portfolio is not None
    
    def test_validate_target_floating_point_tolerance(self, sample_stocks):
        """Test that small floating-point errors are tolerated"""
        positions = {
            sample_stocks["AAPL"]: 10.0,
            sample_stocks["GOOGL"]: 5.0,
        }
        allocations = {
            sample_stocks["AAPL"]: 1.0 / 3.0,
            sample_stocks["GOOGL"]: 2.0 / 3.0,
        }
        portfolio = Portfolio(positions, allocations)
        assert portfolio is not None
    
    def test_rebalance_no_change_needed(self, sample_stocks):
        """Test rebalance when portfolio is already at target"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: 1.0}
        portfolio = Portfolio(positions, allocations)
        prices = {"AAPL": 150.0}
        orders = portfolio.rebalance(prices)
        assert len(orders) == 0
    
    def test_rebalance_multi_stock(self, sample_stocks):
        """Test rebalance with multiple stocks"""
        aapl = sample_stocks["AAPL"]
        googl = sample_stocks["GOOGL"]
        
        positions = {aapl: 10.0, googl: 0.0}
        allocations = {aapl: 0.5, googl: 0.5}
        portfolio = Portfolio(positions, allocations)
        prices = {"AAPL": 100.0, "GOOGL": 200.0}
        orders = portfolio.rebalance(prices)
        
        # Check that we have orders
        assert len(orders) > 0
        
        # Check order types and stocks
        buy_orders = [o for o in orders if o.side == "BUY"]
        sell_orders = [o for o in orders if o.side == "SELL"]
        
        assert len(buy_orders) > 0 or len(sell_orders) > 0
    
    def test_rebalance_missing_price(self, sample_stocks):
        """Test rebalance raises error when price is missing"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: 1.0}
        portfolio = Portfolio(positions, allocations)
        prices = {}  # Missing price for AAPL
        
        with pytest.raises(ValueError, match="Missing price"):
            portfolio.rebalance(prices)
    
    def test_rebalance_zero_portfolio_value(self, sample_stocks):
        """Test rebalance raises error for zero portfolio value"""
        positions = {sample_stocks["AAPL"]: 0.0}
        allocations = {sample_stocks["AAPL"]: 1.0}
        portfolio = Portfolio(positions, allocations)
        prices = {"AAPL": 100.0}
        
        with pytest.raises(ValueError, match="Portfolio value must be positive"):
            portfolio.rebalance(prices)
    
    def test_rebalance_updates_stock_price(self, sample_stocks):
        """Test that rebalance updates stock current prices"""
        positions = {sample_stocks["AAPL"]: 10.0}
        allocations = {sample_stocks["AAPL"]: 1.0}
        portfolio = Portfolio(positions, allocations)
        prices = {"AAPL": 150.5}
        
        assert sample_stocks["AAPL"].get_current_price() == 0.0
        portfolio.rebalance(prices)
        assert sample_stocks["AAPL"].get_current_price() == 150.5


class TestOrder:
    """Unit tests for Order class"""
    
    def test_order_creation(self):
        """Test basic order creation"""
        stock = Stock("AAPL")
        order = Order(stock=stock, side="BUY", shares=10.0)
        assert order.stock.symbol == "AAPL"
        assert order.side == "BUY"
        assert order.shares == 10.0
    
    def test_order_sell(self):
        """Test SELL order creation"""
        stock = Stock("GOOGL")
        order = Order(stock=stock, side="SELL", shares=5.5)
        assert order.side == "SELL"
        assert order.shares == 5.5


class TestIntegration:
    """Integration tests for complete portfolio rebalancing workflow"""
    
    def test_full_rebalance_workflow(self):
        """Test complete rebalance workflow"""
        # Create stocks
        aapl = Stock("AAPL")
        googl = Stock("GOOGL")
        msft = Stock("MSFT")
        
        # Create portfolio with initial positions
        positions = {
            aapl: 100.0,
            googl: 50.0,
            msft: 75.0,
        }
        
        # Define target allocations
        allocations = {
            aapl: 0.5,
            googl: 0.3,
            msft: 0.2,
        }
        
        portfolio = Portfolio(positions, allocations)
        
        # Define prices
        prices = {
            "AAPL": 150.0,
            "GOOGL": 2800.0,
            "MSFT": 310.0,
        }
        
        # Execute rebalance
        orders = portfolio.rebalance(prices)
        
        # Verify orders were generated
        assert isinstance(orders, list)
        for order in orders:
            assert isinstance(order, Order)
            assert order.side in ["BUY", "SELL"]
            assert order.shares > 0
    
    def test_rebalance_convergence(self):
        """Test that applying rebalance orders moves portfolio toward target"""
        aapl = Stock("AAPL")
        googl = Stock("GOOGL")
        
        positions = {aapl: 100.0, googl: 0.0}
        allocations = {aapl: 0.5, googl: 0.5}
        portfolio = Portfolio(positions, allocations)
        
        prices = {"AAPL": 100.0, "GOOGL": 100.0}
        
        # Current portfolio value: 100 * 100 = 10000
        # Target: AAPL = 5000 (50 shares), GOOGL = 5000 (50 shares)
        
        orders = portfolio.rebalance(prices)
        
        # Should have a BUY order for GOOGL
        googl_orders = [o for o in orders if o.stock.symbol == "GOOGL"]
        assert len(googl_orders) > 0
        assert googl_orders[0].side == "BUY"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
