# SQL-Genie

SQL-Genie is a powerful and intuitive web application that allows users to convert natural language queries into SQL queries, visualize the results in various chart formats, and explore table schemas effortlessly. Built with **Streamlit**, this tool is perfect for data analysts, engineers, or anyone who needs to quickly generate SQL queries and gain insights from their databases.

---

## Features

- **Natural Language to SQL**: Simply type your question in plain English, and SQL-Genie will generate the corresponding SQL query for a PostgreSQL database.
- **Customizable Visualizations**: Choose between various chart types such as **Bar**, **Line**, **Area**, and **Donut** to visualize your query results instantly.
- **Schema Explorer**: Select tables and explore their schemas to understand the structure of your data.
- **User-Friendly Interface**: Built with **Streamlit**, the app offers a clean and interactive UI, designed for quick data exploration.

---

## Technologies Used

- **Python**: The core programming language used.
- **Streamlit**: Framework for building the web app.
- **PostgreSQL**: Database used for querying.
- **Altair**: For creating visualizations like bar, line, area, and donut charts.
- **Requests**: To communicate with the backend API for generating SQL queries.

---

## Getting Started

### Prerequisites

To run this project locally, you need to have the following installed:

- **Python 3.7+**
- **PostgreSQL** (make sure your database is set up and accessible)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mayurtableau/SQL-Genie.git
    cd SQL-Genie
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # OR
    source venv/bin/activate  # On Linux/Mac
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database connection and update any required credentials in `db_config.py`.

5. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

6. Open your browser and navigate to `http://localhost:8501` to interact with the app.

---

## Usage

- **Step 1**: Select the tables you want to use for generating SQL queries.
- **Step 2**: Ask your question in plain English (e.g., "Show the total sales by month").
- **Step 3**: The app will generate the SQL query for you and display it.
- **Step 4**: You can visualize the result of the query by choosing a chart type such as Bar, Line, Area, or Donut.
- **Step 5**: View the result in a table format and gain insights from the query.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

1. Fork this repository.
2. Create your feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

---

## Contact

If you have any questions, feel free to contact me at:

- **Email**: Mayurrr2019@outlook.com
- **GitHub**: [@Mayurtableau](https://github.com/Mayurtableau)
