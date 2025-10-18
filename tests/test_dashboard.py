"""
Unit tests for the dashboard module.
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import sqlite3

from dashboard import SalesDashboard


class TestSalesDashboard(unittest.TestCase):
    """Test cases for SalesDashboard class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_file = Path(self.temp_dir) / "test_dashboard.db"
        
        # Create sample database with test data
        self.sample_data = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'customer_name': ['John Doe', 'Jane Smith', 'John Doe', 'Bob Johnson', 'Jane Smith'],
            'product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone'],
            'quantity': [1, 2, 1, 3, 1],
            'unit_price': [1000.0, 500.0, 300.0, 1000.0, 500.0],
            'total_price': [1000.0, 1000.0, 300.0, 3000.0, 500.0],
            'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
        })
        
        # Create database and load data
        conn = sqlite3.connect(self.db_file)
        self.sample_data.to_sql('sales', conn, if_exists='replace', index=False)
        conn.close()
        
        self.dashboard = SalesDashboard(str(self.db_file))
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.dashboard.close_connection()
        import shutil
        import time
        # Wait a moment for file handles to be released on Windows
        time.sleep(0.1)
        try:
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # On Windows, sometimes files are still in use
            pass
    
    def test_init(self):
        """Test dashboard initialization."""
        self.assertEqual(self.dashboard.db_file, self.db_file)
        self.assertIsNone(self.dashboard.connection)
        self.assertIsNone(self.dashboard.data)
    
    def test_connect_database_success(self):
        """Test successful database connection."""
        result = self.dashboard.connect_database()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.dashboard.connection)
    
    def test_connect_database_file_not_found(self):
        """Test database connection with non-existent file."""
        dashboard = SalesDashboard("nonexistent.db")
        
        with patch('streamlit.error') as mock_error:
            result = dashboard.connect_database()
            
        self.assertFalse(result)
        self.assertIsNone(dashboard.connection)
        mock_error.assert_called_once()
    
    def test_load_data_success(self):
        """Test successful data loading."""
        self.dashboard.connect_database()
        result = self.dashboard.load_data()
        
        self.assertTrue(result)
        self.assertIsInstance(self.dashboard.data, pd.DataFrame)
        self.assertEqual(len(self.dashboard.data), 5)
    
    def test_load_data_no_connection(self):
        """Test data loading without database connection."""
        with patch('streamlit.error') as mock_error:
            result = self.dashboard.load_data()
            
        self.assertFalse(result)
        mock_error.assert_called_once_with("No database connection")
    
    def test_load_data_empty_database(self):
        """Test data loading with empty database."""
        empty_db = Path(self.temp_dir) / "empty.db"
        conn = sqlite3.connect(empty_db)
        # Create empty table
        conn.execute("CREATE TABLE sales (order_id INTEGER)")
        conn.close()
        
        dashboard = SalesDashboard(str(empty_db))
        dashboard.connect_database()
        
        with patch('streamlit.warning') as mock_warning:
            result = dashboard.load_data()
            
        self.assertFalse(result)
        mock_warning.assert_called_once_with("No data found in the database")
    
    def test_display_summary_metrics(self):
        """Test summary metrics display."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric:
            
            # Mock columns to return list of mock columns
            mock_cols = [MagicMock() for _ in range(4)]
            mock_columns.return_value = mock_cols
            
            self.dashboard.display_summary_metrics()
            
            # Verify metrics were called
            self.assertEqual(mock_metric.call_count, 4)
    
    def test_display_revenue_by_product(self):
        """Test revenue by product display."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.bar_chart'), \
             patch('streamlit.dataframe'):
            
            mock_cols = [MagicMock(), MagicMock()]
            mock_columns.return_value = mock_cols
            
            # Should not raise an exception
            self.dashboard.display_revenue_by_product()
    
    def test_display_customer_analysis(self):
        """Test customer analysis display."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.pyplot'):
            
            mock_cols = [MagicMock(), MagicMock()]
            mock_columns.return_value = mock_cols
            
            # Should not raise an exception
            self.dashboard.display_customer_analysis()
    
    def test_display_product_analysis(self):
        """Test product analysis display."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.pyplot'):
            
            mock_cols = [MagicMock(), MagicMock()]
            mock_columns.return_value = mock_cols
            
            # Should not raise an exception
            self.dashboard.display_product_analysis()
    
    def test_display_time_analysis_no_date_column(self):
        """Test time analysis when date column is missing."""
        # Create data without date column
        data_no_date = self.sample_data.drop('order_date', axis=1)
        conn = sqlite3.connect(self.db_file)
        data_no_date.to_sql('sales', conn, if_exists='replace', index=False)
        conn.close()
        
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        # Should return early without error
        self.dashboard.display_time_analysis()
    
    def test_display_customer_filter(self):
        """Test customer filter functionality."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.subheader'), \
             patch('streamlit.dataframe'), \
             patch('streamlit.metric'):
            
            mock_selectbox.return_value = 'John Doe'
            mock_cols = [MagicMock(), MagicMock()]
            mock_columns.return_value = mock_cols
            
            # Should not raise an exception
            self.dashboard.display_customer_filter()
    
    def test_display_raw_data(self):
        """Test raw data display functionality."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        with patch('streamlit.header'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.multiselect') as mock_multiselect, \
             patch('streamlit.number_input') as mock_number_input, \
             patch('streamlit.dataframe'), \
             patch('streamlit.download_button'):
            
            # Mock multiple columns
            mock_cols = [MagicMock() for _ in range(3)]
            mock_columns.return_value = mock_cols
            
            mock_multiselect.return_value = ['Laptop', 'Phone']
            mock_number_input.return_value = 0.0
            
            # Should not raise an exception
            self.dashboard.display_raw_data()
    
    def test_close_connection(self):
        """Test connection closing."""
        self.dashboard.connect_database()
        self.assertIsNotNone(self.dashboard.connection)
        
        self.dashboard.close_connection()
        self.assertIsNone(self.dashboard.connection)
    
    @patch('streamlit.stop')
    def test_run_dashboard_connection_failure(self, mock_stop):
        """Test dashboard run with connection failure."""
        dashboard = SalesDashboard("nonexistent.db")
        
        with patch('streamlit.error'):
            dashboard.run_dashboard()
        
        mock_stop.assert_called()
    
    @patch('streamlit.stop')
    def test_run_dashboard_data_loading_failure(self, mock_stop):
        """Test dashboard run with data loading failure."""
        empty_db = Path(self.temp_dir) / "empty_run.db"
        conn = sqlite3.connect(empty_db)
        conn.close()
        
        dashboard = SalesDashboard(str(empty_db))
        
        with patch('streamlit.error'):
            dashboard.run_dashboard()
        
        mock_stop.assert_called()


@pytest.mark.integration
class TestDashboardIntegration(unittest.TestCase):
    """Integration tests for the dashboard."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_file = Path(self.temp_dir) / "integration_dashboard.db"
        
        # Create larger dataset for integration testing
        self.large_dataset = pd.DataFrame({
            'order_id': range(1, 101),
            'customer_name': [f'Customer_{i % 20}' for i in range(100)],
            'product': [f'Product_{i % 10}' for i in range(100)],
            'quantity': [1, 2, 3, 1, 2] * 20,
            'unit_price': [100.0, 200.0, 300.0, 400.0, 500.0] * 20,
            'total_price': [100.0, 400.0, 900.0, 400.0, 1000.0] * 20,
            'order_date': pd.date_range('2023-01-01', periods=100, freq='D')
        })
        
        conn = sqlite3.connect(self.db_file)
        self.large_dataset.to_sql('sales', conn, if_exists='replace', index=False)
        conn.close()
        
        self.dashboard = SalesDashboard(str(self.db_file))
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        self.dashboard.close_connection()
        import shutil
        import time
        # Wait a moment for file handles to be released on Windows
        time.sleep(0.1)
        try:
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # On Windows, sometimes files are still in use
            pass
    
    def test_dashboard_integration_large_dataset(self):
        """Test dashboard with larger dataset."""
        self.dashboard.connect_database()
        result = self.dashboard.load_data()
        
        self.assertTrue(result)
        self.assertIsInstance(self.dashboard.data, pd.DataFrame)
        self.assertEqual(len(self.dashboard.data), 100)
        
        # Test that date column was converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.dashboard.data['order_date']))
    
    def test_data_aggregations(self):
        """Test data aggregations work correctly."""
        self.dashboard.connect_database()
        self.dashboard.load_data()
        
        # Test revenue calculations
        total_revenue = self.dashboard.data['total_price'].sum()
        self.assertGreater(total_revenue, 0)
        
        # Test customer count
        unique_customers = self.dashboard.data['customer_name'].nunique()
        self.assertEqual(unique_customers, 20)  # 20 unique customers
        
        # Test product count
        unique_products = self.dashboard.data['product'].nunique()
        self.assertEqual(unique_products, 10)  # 10 unique products


if __name__ == '__main__':
    unittest.main()
