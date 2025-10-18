"""
Pytest configuration and fixtures for the test suite.
"""

import tempfile
from pathlib import Path

import pandas as pd
import pytest
import sqlite3


@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    import shutil
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_sales_data():
    """Create sample sales data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3, 4, 5],
        'customer_name': ['John Doe', 'Jane Smith', 'John Doe', 'Bob Johnson', 'Jane Smith'],
        'product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone'],
        'quantity': [1, 2, 1, 3, 1],
        'unit_price': [1000.0, 500.0, 300.0, 1000.0, 500.0],
        'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
    })


@pytest.fixture
def sample_csv_file(temp_directory, sample_sales_data):
    """Create a sample CSV file for testing."""
    csv_file = temp_directory / "sample_sales.csv"
    sample_sales_data.to_csv(csv_file, index=False)
    return csv_file


@pytest.fixture
def sample_database(temp_directory, sample_sales_data):
    """Create a sample SQLite database for testing."""
    db_file = temp_directory / "sample_sales.db"
    
    # Add total_price column
    sample_data_with_total = sample_sales_data.copy()
    sample_data_with_total['total_price'] = (
        sample_data_with_total['quantity'] * sample_data_with_total['unit_price']
    )
    
    conn = sqlite3.connect(db_file)
    sample_data_with_total.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    
    return db_file


@pytest.fixture
def large_dataset():
    """Create a larger dataset for integration testing."""
    return pd.DataFrame({
        'order_id': range(1, 101),
        'customer_name': [f'Customer_{i % 20}' for i in range(100)],
        'product': [f'Product_{i % 10}' for i in range(100)],
        'quantity': [1, 2, 3, 1, 2] * 20,
        'unit_price': [100.0, 200.0, 300.0, 400.0, 500.0] * 20,
        'total_price': [100.0, 400.0, 900.0, 400.0, 1000.0] * 20,
        'order_date': pd.date_range('2023-01-01', periods=100, freq='D')
    })


@pytest.fixture
def large_database(temp_directory, large_dataset):
    """Create a larger SQLite database for integration testing."""
    db_file = temp_directory / "large_sales.db"
    
    conn = sqlite3.connect(db_file)
    large_dataset.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    
    return db_file


# Markers for different test types
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.slow = pytest.mark.slow
