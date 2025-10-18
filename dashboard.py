"""
Sales Data Dashboard

An interactive Streamlit dashboard for analyzing sales data from SQLite database.
Provides comprehensive visualizations and analytics for sales performance.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Sales Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


class SalesDashboard:
    """
    Interactive dashboard for sales data analysis.
    
    This class provides a comprehensive dashboard interface for visualizing
    and analyzing sales data stored in SQLite database.
    """
    
    def __init__(self, db_file: str = "sales.db"):
        """
        Initialize the dashboard.
        
        Args:
            db_file: Path to the SQLite database file
        """
        self.db_file = Path(db_file)
        self.connection: Optional[sqlite3.Connection] = None
        self.data: Optional[pd.DataFrame] = None
    
    def connect_database(self) -> bool:
        """
        Connect to the SQLite database.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if not self.db_file.exists():
                st.error(f"Database file not found: {self.db_file}")
                return False
            
            self.connection = sqlite3.connect(self.db_file)
            logger.info(f"Connected to database: {self.db_file}")
            return True
            
        except sqlite3.Error as e:
            st.error(f"Database connection error: {e}")
            logger.error(f"Database connection failed: {e}")
            return False
    
    def load_data(self) -> bool:
        """
        Load sales data from database.
        
        Returns:
            True if data loaded successfully, False otherwise
        """
        try:
            if not self.connection:
                st.error("No database connection")
                return False
            
            self.data = pd.read_sql_query("SELECT * FROM sales", self.connection)
            
            if self.data.empty:
                st.warning("No data found in the database")
                return False
            
            # Convert order_date to datetime if it exists
            if 'order_date' in self.data.columns:
                self.data['order_date'] = pd.to_datetime(self.data['order_date'])
            
            logger.info(f"Loaded {len(self.data)} records from database")
            return True
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            logger.error(f"Data loading failed: {e}")
            return False
    
    def display_summary_metrics(self) -> None:
        """Display key performance indicators."""
        if self.data is None:
            return
        
        st.header("📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = self.data['total_price'].sum()
            st.metric(
                label="Total Revenue",
                value=f"€{total_revenue:,.2f}",
                delta=None
            )
        
        with col2:
            avg_order_value = self.data['total_price'].mean()
            st.metric(
                label="Average Order Value",
                value=f"€{avg_order_value:.2f}",
                delta=None
            )
        
        with col3:
            total_orders = len(self.data)
            st.metric(
                label="Total Orders",
                value=f"{total_orders:,}",
                delta=None
            )
        
        with col4:
            unique_customers = self.data['customer_name'].nunique()
            st.metric(
                label="Unique Customers",
                value=f"{unique_customers:,}",
                delta=None
            )
    
    def display_revenue_by_product(self) -> None:
        """Display revenue analysis by product."""
        if self.data is None:
            return
        
        st.header("📊 Revenue by Product")
        
        revenue_by_product = (
            self.data.groupby('product')['total_price']
            .sum()
            .sort_values(ascending=False)
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(revenue_by_product)
        
        with col2:
            st.dataframe(
                revenue_by_product.reset_index().rename(
                    columns={'total_price': 'Revenue (€)'}
                ),
                use_container_width=True
            )
    
    def display_customer_analysis(self) -> None:
        """Display customer analysis and rankings."""
        if self.data is None:
            return
        
        st.header("👥 Customer Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Customers by Revenue")
            revenue_by_customer = (
                self.data.groupby('customer_name')['total_price']
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )
            
            st.dataframe(
                revenue_by_customer.reset_index().rename(
                    columns={'total_price': 'Total Revenue (€)'}
                ),
                use_container_width=True
            )
        
        with col2:
            st.subheader("Customer Order Distribution")
            customer_orders = self.data['customer_name'].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(
                x=customer_orders.values,
                y=customer_orders.index,
                ax=ax,
                hue=customer_orders.index,
                palette='viridis',
                legend=False
            )
            ax.set_xlabel('Number of Orders')
            ax.set_ylabel('Customer')
            ax.set_title('Orders per Customer (Top 10)')
            st.pyplot(fig)
    
    def display_product_analysis(self) -> None:
        """Display product performance analysis."""
        if self.data is None:
            return
        
        st.header("📦 Product Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orders per Product")
            order_counts = self.data['product'].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(
                x=order_counts.index,
                y=order_counts.values,
                ax=ax,
                hue=order_counts.index,
                palette='Set2',
                legend=False
            )
            ax.set_xlabel('Product')
            ax.set_ylabel('Number of Orders')
            ax.set_title('Order Count by Product')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            st.subheader("Average Order Value by Product")
            avg_value_by_product = (
                self.data.groupby('product')['total_price']
                .mean()
                .sort_values(ascending=False)
            )
            
            st.dataframe(
                avg_value_by_product.reset_index().rename(
                    columns={'total_price': 'Avg Order Value (€)'}
                ),
                use_container_width=True
            )
    
    def display_time_analysis(self) -> None:
        """Display time-based analysis if date data is available."""
        if self.data is None or 'order_date' not in self.data.columns:
            return
        
        st.header("📅 Time Analysis")
        
        # Add date filters
        col1, col2 = st.columns(2)
        
        with col1:
            min_date = self.data['order_date'].min().date()
            max_date = self.data['order_date'].max().date()
            
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        with col2:
            if len(date_range) == 2:
                filtered_data = self.data[
                    (self.data['order_date'].dt.date >= date_range[0]) &
                    (self.data['order_date'].dt.date <= date_range[1])
                ]
                
                st.metric(
                    "Revenue in Period",
                    f"€{filtered_data['total_price'].sum():,.2f}"
                )
        
        # Daily revenue trend
        if len(date_range) == 2:
            daily_revenue = (
                filtered_data.groupby(filtered_data['order_date'].dt.date)['total_price']
                .sum()
                .reset_index()
            )
            daily_revenue.columns = ['Date', 'Revenue']
            
            st.line_chart(daily_revenue.set_index('Date'))
    
    def display_customer_filter(self) -> None:
        """Display customer-specific analysis with filtering."""
        if self.data is None:
            return
        
        st.header("🔍 Customer Detail Analysis")
        
        selected_customer = st.selectbox(
            "Select Customer",
            options=self.data['customer_name'].unique(),
            key="customer_filter"
        )
        
        if selected_customer:
            customer_data = self.data[self.data['customer_name'] == selected_customer]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Orders for {selected_customer}")
                st.dataframe(
                    customer_data[['order_id', 'product', 'quantity', 'unit_price', 'total_price']],
                    use_container_width=True
                )
            
            with col2:
                st.subheader("Customer Summary")
                total_spent = customer_data['total_price'].sum()
                order_count = len(customer_data)
                avg_order = customer_data['total_price'].mean()
                
                st.metric("Total Spent", f"€{total_spent:.2f}")
                st.metric("Number of Orders", order_count)
                st.metric("Average Order Value", f"€{avg_order:.2f}")
    
    def display_raw_data(self) -> None:
        """Display raw data with filtering options."""
        if self.data is None:
            return
        
        st.header("🗂️ Raw Data Explorer")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_products = st.multiselect(
                "Filter by Product",
                options=self.data['product'].unique(),
                default=self.data['product'].unique()
            )
        
        with col2:
            selected_customers = st.multiselect(
                "Filter by Customer",
                options=self.data['customer_name'].unique(),
                default=self.data['customer_name'].unique()
            )
        
        with col3:
            min_price = st.number_input(
                "Minimum Order Value",
                min_value=0.0,
                value=0.0,
                step=10.0
            )
        
        # Apply filters
        filtered_data = self.data[
            (self.data['product'].isin(selected_products)) &
            (self.data['customer_name'].isin(selected_customers)) &
            (self.data['total_price'] >= min_price)
        ]
        
        st.dataframe(filtered_data, use_container_width=True)
        
        # Download button
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )
    
    def run_dashboard(self) -> None:
        """Run the complete dashboard."""
        st.title("📊 Sales Data Dashboard")
        st.markdown("---")
        
        # Initialize dashboard
        if not self.connect_database():
            st.stop()
        
        if not self.load_data():
            st.stop()
        
        # Display dashboard sections
        self.display_summary_metrics()
        st.markdown("---")
        
        self.display_revenue_by_product()
        st.markdown("---")
        
        self.display_customer_analysis()
        st.markdown("---")
        
        self.display_product_analysis()
        st.markdown("---")
        
        self.display_time_analysis()
        st.markdown("---")
        
        self.display_customer_filter()
        st.markdown("---")
        
        self.display_raw_data()
    
    def close_connection(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None


def main():
    """Main function to run the dashboard."""
    try:
        dashboard = SalesDashboard()
        dashboard.run_dashboard()
        
    except Exception as e:
        st.error(f"Dashboard error: {e}")
        logger.error(f"Dashboard execution failed: {e}")
    finally:
        if 'dashboard' in locals():
            dashboard.close_connection()


if __name__ == "__main__":
    main()
