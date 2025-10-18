"""
ETL Pipeline for Sales Data Analysis

This module provides a complete ETL (Extract, Transform, Load) pipeline
for processing sales data from CSV files, storing it in SQLite database,
and performing various analytical queries.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Dict, Optional

import matplotlib.pyplot as plt
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SalesETLPipeline:
    """
    A comprehensive ETL pipeline for sales data processing.
    
    This class handles the extraction of sales data from CSV files,
    transformation of the data (including calculations), and loading
    into a SQLite database for analysis.
    """
    
    def __init__(self, csv_file: str = "sales_data.csv", db_file: str = "sales.db"):
        """
        Initialize the ETL pipeline.
        
        Args:
            csv_file: Path to the CSV file containing sales data
            db_file: Path to the SQLite database file
        """
        self.csv_file = Path(csv_file)
        self.db_file = Path(db_file)
        self.connection: Optional[sqlite3.Connection] = None
        
        # Define analytical queries
        self.queries = {
            "revenue_by_product": """
                SELECT 
                    product,
                    SUM(total_price) AS total_revenue
                FROM sales
                GROUP BY product
                ORDER BY total_revenue DESC
            """,
            "average_order_value": """
                SELECT 
                    ROUND(AVG(total_price), 2) AS avg_order_value
                FROM sales
            """,
            "top_customer": """
                SELECT 
                    customer_name,
                    SUM(total_price) AS customer_revenue
                FROM sales
                GROUP BY customer_name
                ORDER BY customer_revenue DESC
                LIMIT 1
            """,
            "total_sales": """
                SELECT 
                    COUNT(*) AS total_orders,
                    SUM(total_price) AS total_revenue,
                    AVG(total_price) AS avg_order_value
                FROM sales
            """
        }
    
    def extract_data(self) -> pd.DataFrame:
        """
        Extract sales data from CSV file.
        
        Returns:
            DataFrame containing the extracted sales data
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If the CSV file is empty or malformed
        """
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        try:
            df = pd.read_csv(self.csv_file)
            if df.empty:
                raise ValueError("CSV file is empty")
            
            logger.info(f"Successfully extracted {len(df)} records from {self.csv_file}")
            return df
            
        except Exception as e:
            logger.error(f"Error extracting data from {self.csv_file}: {e}")
            raise
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the extracted data by adding calculated fields.
        
        Args:
            df: Raw sales data DataFrame
            
        Returns:
            Transformed DataFrame with additional calculated fields
            
        Raises:
            ValueError: If required columns are missing or data is invalid
        """
        required_columns = ['quantity', 'unit_price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Create a copy to avoid modifying the original
        df_transformed = df.copy()
        
        # Calculate total price
        df_transformed['total_price'] = (
            df_transformed['quantity'] * df_transformed['unit_price']
        )
        
        # Validate data
        if df_transformed['total_price'].isna().any():
            logger.warning("Some total_price calculations resulted in NaN values")
        
        if (df_transformed['quantity'] < 0).any():
            logger.warning("Negative quantities found in data")
        
        if (df_transformed['unit_price'] < 0).any():
            logger.warning("Negative unit prices found in data")
        
        logger.info(f"Successfully transformed {len(df_transformed)} records")
        return df_transformed
    
    def load_data(self, df: pd.DataFrame) -> None:
        """
        Load transformed data into SQLite database.
        
        Args:
            df: Transformed DataFrame to load into database
            
        Raises:
            sqlite3.Error: If database operations fail
        """
        try:
            self.connection = sqlite3.connect(self.db_file)
            
            # Load data into database
            df.to_sql('sales', self.connection, if_exists='replace', index=False)
            
            # Create indexes for better query performance
            cursor = self.connection.cursor()
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_product ON sales(product)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer ON sales(customer_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date)")
            
            self.connection.commit()
            logger.info(f"Successfully loaded {len(df)} records into {self.db_file}")
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def execute_query(self, query_name: str) -> pd.DataFrame:
        """
        Execute a predefined analytical query.
        
        Args:
            query_name: Name of the query to execute
            
        Returns:
            DataFrame containing query results
            
        Raises:
            KeyError: If query_name is not found
            sqlite3.Error: If database query fails
        """
        if query_name not in self.queries:
            available_queries = list(self.queries.keys())
            raise KeyError(f"Query '{query_name}' not found. Available queries: {available_queries}")
        
        if not self.connection:
            raise RuntimeError("No database connection. Run load_data() first.")
        
        try:
            query = self.queries[query_name]
            result = pd.read_sql_query(query, self.connection)
            logger.info(f"Successfully executed query: {query_name}")
            return result
            
        except sqlite3.Error as e:
            logger.error(f"Error executing query '{query_name}': {e}")
            raise
    
    def plot_revenue_by_product(self, save_path: Optional[str] = None) -> None:
        """
        Create a bar chart visualization of revenue by product.
        
        Args:
            save_path: Optional path to save the plot as an image file
        """
        try:
            df_revenue = self.execute_query("revenue_by_product")
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(df_revenue['product'], df_revenue['total_revenue'], 
                          color='skyblue', alpha=0.8)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'€{height:,.0f}', ha='center', va='bottom')
            
            plt.title('Total Revenue by Product', fontsize=16, fontweight='bold')
            plt.xlabel('Product', fontsize=12)
            plt.ylabel('Revenue (€)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Plot saved to: {save_path}")
            
            plt.show()
            
        except Exception as e:
            logger.error(f"Error creating plot: {e}")
            raise
    
    def run_pipeline(self) -> Dict[str, pd.DataFrame]:
        """
        Execute the complete ETL pipeline.
        
        Returns:
            Dictionary containing results of all analytical queries
        """
        logger.info("Starting ETL pipeline...")
        
        try:
            # Extract data
            raw_data = self.extract_data()
            
            # Transform data
            transformed_data = self.transform_data(raw_data)
            
            # Load data
            self.load_data(transformed_data)
            
            # Execute analytical queries
            results = {}
            for query_name in self.queries:
                results[query_name] = self.execute_query(query_name)
                logger.info(f"Query '{query_name}' completed")
            
            # Display results
            self._display_results(results)
            
            logger.info("ETL pipeline completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise
        finally:
            self.close_connection()
    
    def _display_results(self, results: Dict[str, pd.DataFrame]) -> None:
        """
        Display query results in a formatted manner.
        
        Args:
            results: Dictionary containing query results
        """
        query_descriptions = {
            "revenue_by_product": "Revenue by Product",
            "average_order_value": "Average Order Value",
            "top_customer": "Top Customer by Revenue",
            "total_sales": "Total Sales Summary"
        }
        
        for query_name, result_df in results.items():
            description = query_descriptions.get(query_name, query_name)
            print(f"\n{description}:")
            print("-" * 50)
            print(result_df.to_string(index=False))
    
    def close_connection(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")


def main():
    """Main function to run the ETL pipeline."""
    pipeline = SalesETLPipeline()
    try:
        results = pipeline.run_pipeline()
        
        # Reconnect for visualization since connection was closed in run_pipeline
        pipeline.load_data(pipeline.transform_data(pipeline.extract_data()))
        
        # Create visualization
        pipeline.plot_revenue_by_product()
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
    finally:
        pipeline.close_connection()


if __name__ == "__main__":
    main()
