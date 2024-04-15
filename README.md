# Text2ESQuery

Text2ESQuery enhances the querying process of Elasticsearch (ES) by converting natural language queries into ES query language. This system aims to improve user experience and query accuracy by integrating Prompt Engineering techniques. It accepts natural language queries as input and translates them into precise ES queries using sophisticated Prompt Engineering, ensuring accurate and relevant search results.

![Text2ESQuery](Text2ESQuery-video.gif)

## Features

- Accepts natural language queries and converts them into Elasticsearch query language.
- Improves user experience and query accuracy through Prompt Engineering techniques.
- Executes generated ES queries against the Elasticsearch database.
- Retrieves relevant sample records and presents them in a clear and organized manner.
- Provides visualizations to aid users in understanding the retrieved data.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/Text2ESQuery.git
   ```

2. Install the required dependencies:
   
   ```sh
   pip install -r requirements.txt
   ```
   
3. Run the Streamlit web app:
   
   ```sh
   streamlit run app.py
   ```

## Usage

1. **OpenAI API Key**: Users must first enter their OpenAI API key to authenticate requests.

2. **Table Selection**: Users select the table name from a dropdown menu, populated with available table names from the Elasticsearch database.

3. **Natural Language Query**: Users enter their natural language query into a text input field.

4. **Query Processing**: The OpenAI API processes the natural language query to generate an Elasticsearch query.

5. **Query Execution**: The generated Elasticsearch query is executed against the Elasticsearch database.

6. **Results Display**: Relevant sample records are displayed to the user in a table format.

7. **Data Visualization**: Optional data visualization options, such as charts or graphs, help users understand the data.

8. **Result Summary**: A summary of the query results is provided, highlighting key insights or patterns in the data.

## Future Enhancements

- Extending to Other NoSQL Databases
- Making Interactive Visualization
- Tackling Output Tokens

## Conclusion

In conclusion, Text2ESQuery simplifies Elasticsearch querying by converting natural language queries into Elasticsearch query language. It enhances user experience and accuracy through Prompt Engineering. Text2ESQuery makes Elasticsearch accessible by eliminating the need for users to know the query language. It retrieves and presents relevant data with visualizations, improving usability. It has potential for other NoSQL databases, offering a valuable tool for effective data interaction.
