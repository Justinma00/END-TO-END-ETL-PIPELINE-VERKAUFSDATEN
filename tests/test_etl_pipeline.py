"""
Unit tests for the ETL pipeline module.
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import sqlite3

from etl_pipeline import SalesETLPipeline


class TestSalesETLPipeline(unittest.TestCase):
    """Test cases for SalesETLPipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = Path(self.temp_dir) / "test_sales.csv"
        self.db_file = Path(self.temp_dir) / "test_sales.db"
        
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'order_id': [1, 2, 3, 4],
            'customer_name': ['John Doe', 'Jane Smith', 'John Doe', 'Bob Johnson'],
            'product': ['Laptop', 'Phone', 'Tablet', 'Laptop'],
            'quantity': [1, 2, 1, 3],
            'unit_price': [1000.0, 500.0, 300.0, 1000.0],
            'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
        })
        
        # Save sample data to CSV
        self.sample_data.to_csv(self.csv_file, index=False)
        
        self.pipeline = SalesETLPipeline(str(self.csv_file), str(self.db_file))
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.pipeline.close_connection()
        # Clean up temp files
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
        """Test pipeline initialization."""
        self.assertEqual(self.pipeline.csv_file, self.csv_file)
        self.assertEqual(self.pipeline.db_file, self.db_file)
        self.assertIsNone(self.pipeline.connection)
        self.assertIsInstance(self.pipeline.queries, dict)
        self.assertIn("revenue_by_product", self.pipeline.queries)
    
    def test_extract_data_success(self):
        """Test successful data extraction."""
        result = self.pipeline.extract_data()
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)
        self.assertListEqual(list(result.columns), list(self.sample_data.columns))
    
    def test_extract_data_file_not_found(self):
        """Test data extraction with non-existent file."""
        pipeline = SalesETLPipeline("nonexistent.csv", str(self.db_file))
        
        with self.assertRaises(FileNotFoundError):
            pipeline.extract_data()
    
    def test_extract_data_empty_file(self):
        """Test data extraction with empty CSV file."""
        empty_csv = Path(self.temp_dir) / "empty.csv"
        empty_df = pd.DataFrame()
        empty_df.to_csv(empty_csv, index=False)
        
        pipeline = SalesETLPipeline(str(empty_csv), str(self.db_file))
        
        with self.assertRaises(ValueError):
            pipeline.extract_data()
    
    def test_transform_data_success(self):
        """Test successful data transformation."""
        result = self.pipeline.transform_data(self.sample_data)
        
        self.assertIn('total_price', result.columns)
        expected_total_prices = [1000.0, 1000.0, 300.0, 3000.0]
        self.assertListEqual(list(result['total_price']), expected_total_prices)
    
    def test_transform_data_missing_columns(self):
        """Test data transformation with missing required columns."""
        incomplete_data = pd.DataFrame({
            'order_id': [1, 2],
            'customer_name': ['John', 'Jane']
        })
        
        with self.assertRaises(ValueError):
            self.pipeline.transform_data(incomplete_data)
    
    def test_transform_data_negative_values(self):
        """Test data transformation with negative values."""
        negative_data = pd.DataFrame({
            'order_id': [1, 2],
            'customer_name': ['John', 'Jane'],
            'product': ['Laptop', 'Phone'],
            'quantity': [-1, 2],
            'unit_price': [1000.0, -500.0],
            'order_date': ['2023-01-01', '2023-01-02']
        })
        
        with self.assertLogs(level='WARNING') as log:
            result = self.pipeline.transform_data(negative_data)
            
        self.assertIn('Negative quantities found in data', str(log.output))
        self.assertIn('Negative unit prices found in data', str(log.output))
    
    def test_load_data_success(self):
        """Test successful data loading."""
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        self.assertIsNotNone(self.pipeline.connection)
        
        # Verify data was loaded correctly
        cursor = self.pipeline.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 4)
    
    def test_execute_query_success(self):
        """Test successful query execution."""
        # Load data first
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        # Test revenue by product query
        result = self.pipeline.execute_query("revenue_by_product")
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # 3 unique products
        self.assertIn('product', result.columns)
        self.assertIn('total_revenue', result.columns)
    
    def test_execute_query_invalid_query(self):
        """Test query execution with invalid query name."""
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        with self.assertRaises(KeyError):
            self.pipeline.execute_query("invalid_query")
    
    def test_execute_query_no_connection(self):
        """Test query execution without database connection."""
        with self.assertRaises(RuntimeError):
            self.pipeline.execute_query("revenue_by_product")
    
    def test_run_pipeline_success(self):
        """Test successful pipeline execution."""
        results = self.pipeline.run_pipeline()
        
        self.assertIsInstance(results, dict)
        self.assertIn("revenue_by_product", results)
        self.assertIn("average_order_value", results)
        self.assertIn("top_customer", results)
        self.assertIn("total_sales", results)
        
        # Verify all results are DataFrames
        for result in results.values():
            self.assertIsInstance(result, pd.DataFrame)
    
    def test_close_connection(self):
        """Test connection closing."""
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        self.assertIsNotNone(self.pipeline.connection)
        self.pipeline.close_connection()
        self.assertIsNone(self.pipeline.connection)
    
    @patch('matplotlib.pyplot.show')
    def test_plot_revenue_by_product(self, mock_show):
        """Test revenue plotting functionality."""
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        # Should not raise an exception
        self.pipeline.plot_revenue_by_product()
        mock_show.assert_called_once()
    
    def test_plot_revenue_by_product_with_save(self):
        """Test revenue plotting with save functionality."""
        transformed_data = self.pipeline.transform_data(self.sample_data)
        self.pipeline.load_data(transformed_data)
        
        save_path = Path(self.temp_dir) / "test_plot.png"
        
        with patch('matplotlib.pyplot.show'), patch('matplotlib.pyplot.savefig') as mock_save:
            self.pipeline.plot_revenue_by_product(str(save_path))
            mock_save.assert_called_once_with(str(save_path), dpi=300, bbox_inches='tight')


@pytest.mark.integration
class TestETLPipelineIntegration(unittest.TestCase):
    """Integration tests for the ETL pipeline."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = Path(self.temp_dir) / "integration_test.csv"
        self.db_file = Path(self.temp_dir) / "integration_test.db"
        
        # Create larger sample dataset
        self.large_dataset = pd.DataFrame({
            'order_id': range(1, 101),
            'customer_name': [f'Customer_{i % 10}' for i in range(100)],
            'product': [f'Product_{i % 5}' for i in range(100)],
            'quantity': [1, 2, 3, 1, 2] * 20,
            'unit_price': [100.0, 200.0, 300.0, 400.0, 500.0] * 20,
            'order_date': pd.date_range('2023-01-01', periods=100, freq='D')
        })
        
        self.large_dataset.to_csv(self.csv_file, index=False)
        self.pipeline = SalesETLPipeline(str(self.csv_file), str(self.db_file))
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        self.pipeline.close_connection()
        import shutil
        import time
        # Wait a moment for file handles to be released on Windows
        time.sleep(0.1)
        try:
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # On Windows, sometimes files are still in use
            pass
    
    def test_full_pipeline_integration(self):
        """Test complete pipeline with larger dataset."""
        results = self.pipeline.run_pipeline()
        
        # Verify all queries returned results
        for query_name, result in results.items():
            self.assertIsInstance(result, pd.DataFrame)
            self.assertFalse(result.empty, f"Query {query_name} returned empty result")
        
        # Verify revenue by product has correct number of products
        revenue_result = results["revenue_by_product"]
        self.assertEqual(len(revenue_result), 5)  # 5 unique products
        
        # Verify top customer query returns single result
        top_customer_result = results["top_customer"]
        self.assertEqual(len(top_customer_result), 1)
        
        # Verify average order value is reasonable
        avg_order_result = results["average_order_value"]
        avg_value = avg_order_result.iloc[0]['avg_order_value']
        self.assertGreater(avg_value, 0)
        self.assertLess(avg_value, 2000)  # Reasonable upper bound
    
    def test_database_performance(self):
        """Test database performance with indexes."""
        results = self.pipeline.run_pipeline()
        
        # Verify indexes were created - need to reconnect since connection was closed
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.assertIn('idx_product', indexes)
        self.assertIn('idx_customer', indexes)
        self.assertIn('idx_order_date', indexes)


if __name__ == '__main__':
    unittest.main()
