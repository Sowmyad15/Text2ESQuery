# app.py
import streamlit as st
import link_es as es
import config as c
import pandas as pd


st.set_page_config(
    page_title="Text2ESQuery",
    page_icon="🧊",
    layout="wide")

st.title("Text2ESQuery")

# Function to initialize session state
def init_session_state():
    if 'dataset' not in st.session_state:
        st.session_state.dataset = None
        st.session_state.col_names = None
        st.session_state.mapping = None

init_session_state()

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    index_names = es.connect_es(c.ES_ID, c.ES_PASS)[1]

    dataset = st.selectbox("Choose Index/Table", [index for index in index_names if not index.startswith('.') and index != 'metrics-endpoint.metadata_current_default'],
                           key="index_selector",
                           placeholder="Select Index/Table Name",
                           index=[index for index in index_names if not index.startswith('.') and index != 'metrics-endpoint.metadata_current_default'].index(st.session_state.dataset) if st.session_state.dataset else None,
                           format_func=lambda x: x)  # Make it as a side scrollable menu
    # Update session state if dataset changes
    if dataset != st.session_state.dataset:
        st.session_state.dataset = dataset
        st.session_state.col_names, st.session_state.mapping = es.get_columns(dataset)



with st.expander(f"Columns in {st.session_state.dataset}"):
    if dataset is not None:
        st.info(f"{dataset} index contains the following list of columns: {st.session_state.col_names}", icon="ℹ️")

with st.form('my_form'):   
    prompt1 = f"""Use the Elasticsearch index '{dataset}', your task is to generate an Elasticsearch query as per the column names {st.session_state.col_names}, {st.session_state.mapping}.
Do not add '.keyword' in the ElasticSearch Query under both 'aggregation' and '_source' fields of the query. Try to provide aggregation field in the result and return all data records under '_source'."""

    user1 = st.text_area('Enter text:')
    
    st.form_submit_button('Submit')
    
    if openai_api_key.startswith('sk-') and st.session_state.dataset is not None and user1 !="":
        query = es.get_completion(openai_api_key, prompt1, user1)
    
        
        tab1,tab2,tab3,tab4=st.tabs(['ES Query',"ES Output","Aggregation","Visualisation"])
        with tab1:
            
            with st.container(border=True):
                st.header("ES Query")
                st.code(query)
                    
        with tab2:
            with st.container(border=True):
                st.header("Data Fetched") 
                res=es.convert_json(query, st.session_state.dataset)
                st.write(res)
                    
        with tab3:
            with st.container(border=True):
                
                if res.get("hits", {}).get("hits", []):
                    st.header("Sample Data:")
                    hits = res.get("hits", {}).get("hits", [])

                    # Extract _source field from each hit
                    sources = [hit.get("_source", {}) for hit in hits]

                    df = pd.DataFrame(sources)
                          
                    st.dataframe(df)
                            
                st.header("Aggregation")
                to_df=f"""Extract the details under 'aggregations' field,  in {res} and display it in sentence with bullet points. If 'aggregations' field is empty, then inform the user by stating the reason for empty aggregation field, do not include Document Count here."""
                final_df = es.get_completion(openai_api_key,to_df,res)
                st.write(final_df)
                                

        with tab4:
            with st.container(border=True):      
                
                vis=f"""Use data, {res} or {final_df} and Create a Streamlit dashboard using plotly express library, use colorful and creative charts, KPI, text cards, maps (if possible)etc., based on the available data. The script should only include code, no comments, and it should be built only using Streamlit. Do not include document count in the visualization. 
                If no data is found, return a text stating that you couldn't find any suitable visualization for the data. Always Generate visualisation supported by streamlit and modify or skip data as needed."""
                
                vis_f=es.get_completion(openai_api_key,vis,final_df)
                        
                if vis_f.startswith("```"):
                    code=es.extract_code(vis_f)
                else:
                    code=vis_f
            
            
                try:    
                    exec(code)
                        
                            
                except Exception as e:
                    st.error(f"Error executing the script: {e}")
                        
                        
                inf=f"Use the data from {final_df} and {res}, generate business intelligence insights based on the data. Provide a well-formatted text. Return only the insights."
                inf_f=es.get_completion(openai_api_key,inf,res)
                st.info(inf_f)
                
    elif not openai_api_key.startswith('sk-'):
        st.warning('Please enter a valid OpenAI API key!', icon='⚠')
                                
                    
                
        



            
