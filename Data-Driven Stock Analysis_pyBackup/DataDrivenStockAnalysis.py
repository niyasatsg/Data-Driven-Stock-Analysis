import streamlit as st
from streamlit_option_menu import option_menu
import os
import yaml
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


# Function to extract and transform data
def extract_and_transform_data(yaml_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    data_dict = {}
    for root, dirs, files in os.walk(yaml_folder_path):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    if isinstance(yaml_data, list):
                        for item in yaml_data:
                            ticker = item.get('Ticker')
                            if ticker not in data_dict:
                                data_dict[ticker] = []
                            data_dict[ticker].append(item)
                    else:
                        ticker = yaml_data.get('Ticker')
                        if ticker not in data_dict:
                            data_dict[ticker] = []
                        data_dict[ticker].append(yaml_data)
    
    for ticker, ticker_data in data_dict.items():
        df = pd.DataFrame(ticker_data)
        df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'Ticker']]
        output_file_path = os.path.join(output_folder_path, f"{ticker}.csv")
        df.to_csv(output_file_path, index=False)

# Connection string for SQLAlchemy
connection_string = 'mysql+pymysql://root:K00th%40n%40llur@localhost:3306/StockAnalysis'
engine = create_engine(connection_string)

# Function to calculate volatility
def calculate_volatility(csv_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    volatility_dict = {}
    for file in os.listdir(csv_folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file)
            ticker = file.split('.')[0]
            df = pd.read_csv(file_path)
            df['daily_return'] = df['close'].pct_change()
            volatility = df['daily_return'].std()
            volatility_dict[ticker] = volatility
    
    volatility_df = pd.DataFrame(list(volatility_dict.items()), columns=['Ticker', 'Volatility'])
    top_10_volatile_stocks = volatility_df.sort_values(by='Volatility', ascending=False).head(10)
    
    st.dataframe(top_10_volatile_stocks)
    
    output_file_path = os.path.join(output_folder_path, 'top_10_volatile_stocks.csv')
    top_10_volatile_stocks.to_csv(output_file_path, index=False)
    st.success(f"CSV file saved successfully at {output_file_path}")
    
    return output_file_path, top_10_volatile_stocks

# Function to insert volatility data into MySQL using SQLAlchemy with pymysql
def insert_volatility_data_to_mysql(csv_file_path, connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Insert the data into the MySQL table with an upsert (insert or update)
        with engine.connect() as connection:
            for index, row in df.iterrows():
                insert_query = text(f"""
                INSERT INTO VolatilityAnalysis (Ticker, Volatility)
                VALUES ('{row['Ticker']}', {row['Volatility']})
                ON DUPLICATE KEY UPDATE Volatility = VALUES(Volatility);
                """)
                connection.execute(insert_query)
        
        st.success("Volatility data inserted into MySQL successfully!")
        
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to plot the bar chart from the database
def plot_volatility_bar_chart_from_db(connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Query the top 10 most volatile stocks from the database
        query = """
        SELECT Ticker, Volatility
        FROM VolatilityAnalysis
        ORDER BY Volatility DESC
        LIMIT 10;
        """
        top_10_volatile_stocks = pd.read_sql(query, con=engine)
        
        # Plot a bar chart showing the volatility of the top 10 most volatile stocks
        plt.figure(figsize=(12, 8))
        plt.bar(top_10_volatile_stocks['Ticker'], top_10_volatile_stocks['Volatility'], color='skyblue')
        plt.xlabel('Stock Ticker')
        plt.ylabel('Volatility (Standard Deviation of Daily Returns)')
        plt.title('Top 10 Most Volatile Stocks Over the Past Year')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
        
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to calculate cumulative return and save the CSV files
def calculate_and_save_cumulative_return(csv_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    cumulative_return_dict = {}
    
    for file in os.listdir(csv_folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file)
            ticker = file.split('.')[0]
            df = pd.read_csv(file_path)
            df['daily_return'] = df['close'].pct_change()
            df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1
            cumulative_return_dict[ticker] = df['cumulative_return'].iloc[-1]
            
            # Save cumulative return to CSV
            cumulative_return_output_file_path = os.path.join(output_folder_path, f"{ticker}_cumulative_return.csv")
            df.to_csv(cumulative_return_output_file_path, index=False)

    cumulative_return_df = pd.DataFrame(list(cumulative_return_dict.items()), columns=['Ticker', 'Cumulative'])
    # Display cumulative return dataframe
    st.dataframe(cumulative_return_df)
    # Save cumulative return dataframe to CSV
    cumulative_return_df_output_file_path = os.path.join(output_folder_path, 'cumulative_return.csv')
    cumulative_return_df.to_csv(cumulative_return_df_output_file_path, index=False)
    st.success(f"Cumulative return CSV file saved successfully at {cumulative_return_df_output_file_path}")
    return cumulative_return_df_output_file_path, cumulative_return_df

# Function to insert cumulative return data into MySQL using SQLAlchemy with pymysql
def insert_cumulative_return_data_to_mysql(csv_file_path, connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_file_path)
        #st.write("DataFrame loaded from CSV:")
        #st.write(df.head())
        
        # Insert the data into the MySQL table using to_sql
        df.to_sql('cumulativereturnanalysis', con=engine, if_exists='replace', index=False)
        
        st.success("Cumulative return data inserted into MySQL successfully!")
        
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to plot the cumulative return line chart from the database
def plot_cumulative_return_bar_chart_from_db(connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Query the top 5 performing stocks from the database
        query = """
        SELECT Ticker, Cumulative
        FROM CumulativeReturnAnalysis
        ORDER BY Cumulative DESC
        LIMIT 5;
        """
        top_5_performing_stocks = pd.read_sql(query, con=engine)
        
        plt.figure(figsize=(12, 8))
        plt.bar(top_5_performing_stocks['Ticker'], top_5_performing_stocks['Cumulative'], color='skyblue')
        plt.xlabel('Stock Ticker')
        plt.ylabel('Cumulative Return')
        plt.title('Top 5 Performing Stocks by Cumulative Return')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
        
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

def insert_average_sector_returns_to_mysql(csv_file_path, connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_file_path)
        # Insert the data into the MySQL table using to_sql
        df.to_sql('sectorperformance', con=engine, if_exists='replace', index=False)
        st.success("Average sector returns data inserted into MySQL successfully!")
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
  
# Function to plot the bar chart from the database
def plot_average_sector_returns_bar_chart_from_db(connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        # Query the average sector returns from the database
        query = """
        SELECT Sector, `Average Yearly Return`
        FROM SectorPerformance;
        """
        average_sector_returns_df = pd.read_sql(query, con=engine)
        # Plot a bar chart showing the average performance for each sector
        plt.figure(figsize=(12, 8))
        plt.bar(average_sector_returns_df['Sector'], average_sector_returns_df['Average Yearly Return'], color='skyblue')
        plt.xlabel('Sector')
        plt.ylabel('Average Yearly Return')
        plt.title('Average Yearly Return by Sector')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to insert correlation matrix data into MySQL using SQLAlchemy with pymysql
def insert_correlation_matrix_to_mysql(csv_file_path, connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Load the CSV data into a DataFrame
        df = pd.read_csv(csv_file_path, index_col=0)
        
        # Insert the data into the MySQL table using to_sql without creating an index on 'index' column
        df.to_sql('stockpricecorrelation', con=engine, if_exists='replace', index=False)
        
        print("Correlation matrix data inserted into MySQL successfully!")
        
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to plot and display the heatmap from the database using Plotly
def plot_correlation_heatmap_from_db(connection_string):
    try:
        # Create a connection to the MySQL database using SQLAlchemy with pymysql
        engine = create_engine(f'mysql+pymysql://{connection_string}')
        
        # Query the correlation matrix from the database
        query = """
        SELECT *
        FROM stockpricecorrelation;
        """
        correlation_matrix_df = pd.read_sql(query, con=engine)
        
        # Check if the correlation matrix is empty
        if correlation_matrix_df.empty:
            st.warning("The correlation matrix is empty. Cannot show top correlated stocks.")
            return
        
        # Melt the correlation matrix to get pairs of stocks and their correlation values
        melted_df = correlation_matrix_df.reset_index().melt(id_vars='index', var_name='Stock2', value_name='Correlation')
        melted_df.rename(columns={'index': 'Stock1'}, inplace=True)
       
        # Remove self-correlations (correlation of a stock with itself)
        melted_df = melted_df[melted_df['Stock1'] != melted_df['Stock2']]
      
        # Ensure both columns are treated as strings
        melted_df['Stock1'] = melted_df['Stock1'].astype(str)
        melted_df['Stock2'] = melted_df['Stock2'].astype(str)

        # Remove duplicate pairs (e.g., (A, B) and (B, A))
        melted_df['pair'] = melted_df.apply(lambda row: tuple(sorted([row['Stock1'], row['Stock2']])), axis=1)
        melted_df = melted_df.drop_duplicates(subset='pair').drop(columns='pair')
      
        # Filter out perfect correlations (1.0)
        melted_df = melted_df[melted_df['Correlation'] < 1.0]

        # Sort by absolute correlation values in descending order and get the top 10 pairs
        top_10_correlated = melted_df.sort_values(by='Correlation', ascending=False).head(10)
        
        # Plot the heatmap
        fig = px.imshow(correlation_matrix_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig)
      
    except (SQLAlchemyError, IntegrityError, DataError) as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to calculate monthly returns
def calculate_monthly_returns(df):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    monthly_returns = df['close'].resample('ME').ffill().pct_change()
    return monthly_returns

# Function to get top gainers and losers for each month
def get_top_gainers_losers(monthly_returns, n=5):
    top_gainers = monthly_returns.nlargest(n)
    top_losers = monthly_returns.nsmallest(n)
    return top_gainers, top_losers

# Function to plot top gainers and losers with ticker names on the x-axis
def plot_top_gainers_losers(top_gainers, top_losers, month, gainers_tickers, losers_tickers):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    
    top_gainers.plot(kind='bar', ax=ax[0], color='green')
    ax[0].set_title(f'Top {len(top_gainers)} Gainers in {month}')
    ax[0].set_ylabel('Percentage Return')
    ax[0].set_xticklabels(gainers_tickers, rotation=45)
    
    top_losers.plot(kind='bar', ax=ax[1], color='red')
    ax[1].set_title(f'Top {len(top_losers)} Losers in {month}')
    ax[1].set_ylabel('Percentage Return')
    ax[1].set_xticklabels(losers_tickers, rotation=45)
    
    plt.tight_layout()
    return fig
    
# Function to insert data into MySQL using SQLAlchemy
def insert_into_mysql(engine, month, gainers_df, losers_df):
    try:
        with engine.begin() as connection:
            gainers_data = [(month, row['index'], row[0]) for _, row in gainers_df.iterrows()]
            losers_data = [(month, row['index'], row[0]) for _, row in losers_df.iterrows()]
            
            #st.write("Gainers Data:", gainers_data)
            #st.write("Losers Data:", losers_data)
            
            connection.execute(
                text("""
                    INSERT INTO gainers (month, ticker, percentage_return)
                    VALUES (:month, :ticker, :percentage_return)
                    ON DUPLICATE KEY UPDATE
                    percentage_return = VALUES(percentage_return)
                """),
                [{"month": month, "ticker": ticker, "percentage_return": percentage_return} for month, ticker, percentage_return in gainers_data]
            )
            connection.execute(
                text("""
                    INSERT INTO losers (month, ticker, percentage_return)
                    VALUES (:month, :ticker, :percentage_return)
                    ON DUPLICATE KEY UPDATE
                    percentage_return = VALUES(percentage_return)
                """),
                [{"month": month, "ticker": ticker, "percentage_return": percentage_return} for month, ticker, percentage_return in losers_data]
            )
            st.success(f"Data for {month} successfully inserted into the database.")
    except SQLAlchemyError as e:
        st.error(f"Error while connecting to MySQL: {e}")

# Streamlit app
st.title("Stock Analysis Dashboard")

# Customizing the menu
with st.sidebar:
    menu = option_menu(
        "Menu",
        ["Data Cleaning", "Volatility Analysis", "Cumulative Return", "Sector-wise Performance", "Stock Price Correlation", "Top 5 Gainers and Losers"],
        icons=['brush', 'bar-chart', 'graph-up', 'pie-chart', 'graph-up-arrow', 'trophy'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

connection_string = 'root:K00th%40n%40llur@localhost:3306/StockAnalysis'
if menu == "Data Cleaning":
    st.header("Data Cleaning")
    yaml_folder_path = st.text_input("YAML Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\data')
    output_folder_path = st.text_input("Output Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output')
    if st.button("Generate CSV Files"):
        extract_and_transform_data(yaml_folder_path, output_folder_path)
        st.success("CSV files generated successfully!")

elif menu == "Volatility Analysis":
    st.header("Volatility Analysis")
    csv_folder_path = st.text_input("CSV Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output')
    volatility_output_folder_path = st.text_input("Volatility Output Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\VolatilityAnalysis')
    if st.button("Analyze Volatility"):
        csv_file_path, top_10_volatile_stocks = calculate_volatility(csv_folder_path, volatility_output_folder_path)
        insert_volatility_data_to_mysql(csv_file_path, connection_string)
    if st.button("Show Volatility Chart from Database"):
        plot_volatility_bar_chart_from_db(connection_string)

elif menu == "Cumulative Return":
    st.header("Cumulative Return")
    csv_folder_path = st.text_input("CSV Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output')
    cumulative_return_output_folder_path = st.text_input("Cumulative Return Output Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\CumulativeReturns')
    if st.button("Cumulative Return Over Time"):
        csv_file_path, top_5_performing_stocks = calculate_and_save_cumulative_return(csv_folder_path,cumulative_return_output_folder_path)
        insert_cumulative_return_data_to_mysql(csv_file_path, connection_string)
    if st.button("Show Cumulative Return from Database"):
        plot_cumulative_return_bar_chart_from_db(connection_string)
        
elif menu == "Sector-wise Performance":
    st.header("Sector-wise Performance")
    # Load the sector data
    sector_data = pd.read_csv(r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\Sectordata\\Sector_data - Sheet1.csv')
    # Initialize a dictionary to store cumulative returns for each sector
    sector_returns = {}
    # Folder containing the 50 CSV files
    csv_folder_path = r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output'
    # Extract the ticker symbol from the Symbol column after the colon
    sector_data['Ticker'] = sector_data['Symbol'].apply(lambda x: x.split(': ')[-1])
    # Iterate over each CSV file in the folder
    for file in os.listdir(csv_folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file)
            ticker = file.split('.')[0]
            # Load the stock data
            df = pd.read_csv(file_path)
            # Calculate the cumulative return for the stock
            df['daily_return'] = df['close'].pct_change()
            df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1
            cumulative_return = df['cumulative_return'].iloc[-1]
            # Check if the ticker exists in the sector data
            if ticker in sector_data['Ticker'].values:
                # Get the sector for the stock
                sector = sector_data[sector_data['Ticker'] == ticker]['sector'].values[0]
                # Add the cumulative return to the sector's list of returns
                if sector not in sector_returns:
                    sector_returns[sector] = []
                sector_returns[sector].append(cumulative_return)
            else:
                print(f"Ticker {ticker} not found in sector data.")
    # Calculate the average yearly return for each sector
    average_sector_returns = {sector: sum(returns) / len(returns) for sector, returns in sector_returns.items()}
    
    # Load the sector data
    sector_data = pd.read_csv(r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\Sectordata\\Sector_data - Sheet1.csv')
    # Initialize a dictionary to store cumulative returns for each sector
    sector_returns = {}
    # Folder containing the 50 CSV files
    csv_folder_path = r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output'
    # Extract the ticker symbol from the Symbol column after the colon
    sector_data['Ticker'] = sector_data['Symbol'].apply(lambda x: x.split(': ')[-1])
    # Iterate over each CSV file in the folder
    for file in os.listdir(csv_folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file)
            ticker = file.split('.')[0]
            # Load the stock data
            df = pd.read_csv(file_path)
            # Calculate the cumulative return for the stock
            df['daily_return'] = df['close'].pct_change()
            df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1
            cumulative_return = df['cumulative_return'].iloc[-1]
            # Check if the ticker exists in the sector data
            if ticker in sector_data['Ticker'].values:
                # Get the sector for the stock
                sector = sector_data[sector_data['Ticker'] == ticker]['sector'].values[0]
                # Add the cumulative return to the sector's list of returns
                if sector not in sector_returns:
                    sector_returns[sector] = []
                sector_returns[sector].append(cumulative_return)
            else:
                print(f"Ticker {ticker} not found in sector data.")
    # Calculate the average yearly return for each sector
    average_sector_returns = {sector: sum(returns) / len(returns) for sector, returns in sector_returns.items()}
    # Convert the average sector returns to a DataFrame for plotting and saving to CSV
    average_sector_returns_df = pd.DataFrame(list(average_sector_returns.items()), columns=['Sector', 'Average Yearly Return'])
    # Display the DataFrame in Streamlit
    st.write("Average Yearly Return by Sector:")
    st.dataframe(average_sector_returns_df)
    # Save the DataFrame to CSV
    output_csv_path = r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\SectorwisePerformance\\average_sector_returns.csv'
    average_sector_returns_df.to_csv(output_csv_path, index=False)
    st.success(f"CSV file saved successfully at {output_csv_path}")
    # Insert the average sector returns data into MySQL
    insert_average_sector_returns_to_mysql(output_csv_path, connection_string)
    # Plot the bar chart from the database
    #connection_string = 'root:K00th%40n%40llur@localhost:3306/StockAnalysis'
    plot_average_sector_returns_bar_chart_from_db(connection_string)
    # Function to insert average sector returns data into MySQL using SQLAlchemy with pymysql

elif menu == "Stock Price Correlation":
    st.header("Stock Price Correlation")

    # Folder containing the CSV files
    csv_folder_path = r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output'

    # Initialize a dictionary to store closing prices for each stock
    closing_prices = {}

    # Iterate over each CSV file in the folder
    for file in os.listdir(csv_folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file)
            ticker = file.split('.')[0]
            
            # Load the stock data
            df = pd.read_csv(file_path)
            
            # Store the closing prices for the stock
            if 'close' in df.columns:
                closing_prices[ticker] = df['close']
            else:
                st.warning(f"Column 'close' not found in {file}")

    # Convert the closing prices dictionary to a DataFrame
    closing_prices_df = pd.DataFrame(closing_prices)

    # Calculate the correlation matrix
    correlation_matrix = closing_prices_df.corr()

    # Display the correlation matrix in a DataFrame
    st.dataframe(correlation_matrix)

    # Save the correlation matrix to CSV
    output_csv_path = r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\StockPriceCorrelation\\correlation_matrix.csv'
    correlation_matrix.to_csv(output_csv_path)

    # Insert the correlation matrix data into MySQL
    insert_correlation_matrix_to_mysql(output_csv_path, connection_string)

    # Show success message
    st.success("Correlation matrix data inserted into MySQL successfully!")

    # Button to show the price correlation matrix in a heatmap
    if st.button("Show Price Correlation Matrix in Heatmap"):
        plot_correlation_heatmap_from_db(connection_string)

elif menu == "Top 5 Gainers and Losers":
    st.header("Top 5 Gainers and Losers (Month-wise)")
    data_folder_path = st.text_input("Data Folder Path", r'C:\\Users\\niyas.abdul\\Documents\\StockAnalysis\\output')
    if st.button("Analyze"):
        all_files = [f for f in os.listdir(data_folder_path) if f.endswith('.csv')]
        
        monthly_gainers_losers = {}
        
        for file in all_files:
            file_path = os.path.join(data_folder_path, file)
            df = pd.read_csv(file_path)
            
            # Ensure the 'close' column exists
            if 'close' not in df.columns:
                st.error(f"'close' column not found in {file}")
                continue
            
            monthly_returns = calculate_monthly_returns(df)
            
            for month in monthly_returns.index.strftime('%Y-%m').unique():
                if month not in monthly_gainers_losers:
                    monthly_gainers_losers[month] = {'gainers': pd.Series(dtype=float), 'losers': pd.Series(dtype=float)}
                
                month_data = monthly_returns[monthly_returns.index.strftime('%Y-%m') == month]
                top_gainers, top_losers = get_top_gainers_losers(month_data)
                
                if not top_gainers.empty:
                    monthly_gainers_losers[month]['gainers'] = pd.concat([monthly_gainers_losers[month]['gainers'], pd.Series(top_gainers.values, index=[file.replace('.csv', '')]*len(top_gainers))])
                if not top_losers.empty:
                    monthly_gainers_losers[month]['losers'] = pd.concat([monthly_gainers_losers[month]['losers'], pd.Series(top_losers.values, index=[file.replace('.csv', '')]*len(top_losers))])
        
        for month, data in monthly_gainers_losers.items():
            if data['gainers'].notna().any() and data['losers'].notna().any():
                st.header(f"Top 5 Gainers and Losers in {month}")
                
                gainers_df = data['gainers'].nlargest(5).reset_index()
                losers_df = data['losers'].nsmallest(5).reset_index()
                
                gainers_tickers = gainers_df['index'].tolist()
                losers_tickers = losers_df['index'].tolist()
                
                fig = plot_top_gainers_losers(gainers_df.set_index('index')[0], losers_df.set_index('index')[0], month, gainers_tickers, losers_tickers)
                st.pyplot(fig)
                
                # Insert data into MySQL
                insert_into_mysql(engine, month, gainers_df, losers_df)