# Add this at the top of your main.py file
import sys
import os

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import time
import pandas as pd
import streamlit as st
from tools.enhanced_duckduckgo_search import   enhanced_duckduckgo_search
from tools.enhanced_scrape_website import  scrape_website
#from tools.enhanced_openai_search import   enhanced_openai_search
from tools.ceo_name import   search_for_hospital_ceo
from tools.insurance import   search_for_insurance
from tools.adress import search_for_address
from tools.url import search_for_website
from  tools.phone_number import contact_number
from tools.revenue import search_for_revenue
from tools.specialitie import search_for_specialities
from tools.doctors import search_for_doctors
from prompts import adress_prompt , CONTACTPERSON_prompt , CONTACTNUMBER_prompt , analyze_extraction_results,URLWEBSITE_prompt , NETREVENUE_prompt , NOOFSPECIALTIES_prompt , NOOFDOCTORS_prompt , INSURANCESACCEPTED_prompt
from helper import airtable_add , extract_validation_result , validate_hospital , create_category_queries , extract_urls_from_json , analyse_raw
from dotenv import load_dotenv
from Crewai_agent import run_agent
from tools.deep_search import process_healthcare_provider 
load_dotenv()



# Set your API keys (in a real app, you would use st.secrets)
API_KEY_AIRTABLE = os.environ["API_KEY_AIRTABLE"]
# Create a temporary directory for results
def main():
    st.set_page_config(page_title="Research Assistant with CrewAI", layout="wide")
    
    # Initialize session state for API keys
    if 'openai_api_key' not in st.session_state:
        st.session_state['openai_api_key'] = OPENAI_API_KEY
    
    st.title("Klaim Project")
    
    # Sidebar for API keys
    with st.sidebar:
        st.header("Configuration")
        
        # We're using a form to better control when the API keys are updated
        with st.form("api_keys_form"):
            openai_key = st.text_input("OpenAI API Key", value=st.session_state['openai_api_key'], 
                                      type="password", key="openai_key_input")
            submit_keys = st.form_submit_button("Save API Keys")

            
            
            if submit_keys:
                st.session_state['openai_api_key'] = openai_key
                OPENAI_API_KEY= st.session_state['openai_api_key']
                st.success("API keys saved!")
        
        st.markdown("---")

    
    # Main area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        
        
        # Using a form to control when the research is triggered
        with st.form("research_form"):
            user_input = st.text_area("Enter the hospital name you would like to research.", 
                                     height=150,
                                     placeholder="Example: AMANA VILLAGE HEALTHCARE L.L.C")
            
            submitted = st.form_submit_button("Research This Topic")
            
            if submitted and (not user_input or len(user_input.strip()) < 10):
                st.error("Please enter a more detailed research topic or question.")
    
    # Only run the research if the form was submitted with valid input
    if 'submitted' in locals() and submitted and user_input and len(user_input.strip()) >= 10:
        with col2:
            st.header("Research Results")
            
            with st.spinner("The AI agents are researching your topic. This may take several minutes..."):
                # st.markdown(enhanced_duckduckgo_search(user_input))
                #result= extract_validation_result(validate_hospital(OPENAI_API_KEY, user_input))
                hospital_name = user_input
                ADDRESS_search_result= search_for_address(hospital_name  , OPENAI_API_KEY)
                #Using openai web search 
                CONTACT_PERSON_result=search_for_hospital_ceo(hospital_name , OPENAI_API_KEY)

                #CONTACT_NUMBER =contact_number(hospital_name , CONTACT_PERSON_result['ceo_name'])
                URL_WEBSITE = search_for_website(hospital_name  , OPENAI_API_KEY)


                #Using openai web search 
                NETREVENUEYEARLY = search_for_revenue(hospital_name  , OPENAI_API_KEY)
                NO_OF_SPECIALTIES = search_for_specialities(hospital_name, OPENAI_API_KEY)
                NOOFDOCTORS = search_for_doctors(hospital_name , OPENAI_API_KEY)
                INSURANCES_ACCEPTED = search_for_insurance(hospital_name , OPENAI_API_KEY)

                #Using duckduckgo web search 
                #NETREVENUEYEARLY = enhanced_duckduckgo_search(hospital_name ,create_category_queries(hospital_name ,'NET REVENUE/YEARLY'))
                #NO_OF_SPECIALTIES = enhanced_duckduckgo_search(hospital_name ,create_category_queries(hospital_name ,'NO. OF SPECIALTIES'))
                #NOOFDOCTORS = enhanced_duckduckgo_search(hospital_name ,create_category_queries(hospital_name ,'NO. OF DOCTORS'))


                # st.markdown("----------------------------RAW input--------------------------------")
                # urls_ADDRESS_search_result= extract_urls_from_json(ADDRESS_search_result)
                # urls_URL_WEBSITE= extract_urls_from_json(URL_WEBSITE)
                # urls_NETREVENUEYEARLY= extract_urls_from_json(NETREVENUEYEARLY)
                # urls_NO_OF_SPECIALTIES= extract_urls_from_json(NO_OF_SPECIALTIES)
                # urls_NOOFDOCTORS= extract_urls_from_json(NOOFDOCTORS)
                # ADDRESS_optimize_search = []
                # optimize_URL_WEBSITE = []
                # optimize_NETREVENUEYEARLY = []
                # NO_OF_SPECIALTIES_optimize = []
                # NOOFDOCTORS_optimize = []
                # st.write(urls_ADDRESS_search_result)
                # st.write("€€€€€€€€")
                # st.write(urls_URL_WEBSITE)
                # st.write("€€€€€€€€")
                # st.write(urls_NETREVENUEYEARLY)  
                # st.write("€€€€€€€€")                       
                # st.write(urls_NO_OF_SPECIALTIES)  
                # st.write("€€€€€€€€")                
                # st.write(urls_NOOFDOCTORS)
                # st.write('RAW DATA Scrapped')                           
                # for item in urls_ADDRESS_search_result:
                #     try:
                #         result = analyse_raw(GEMINI_API_KEY, adress_prompt(scrape_website(item)), 'ADDRESS')
                #         st.markdown(result)

                #         ADDRESS_optimize_search.append(result)
                #     except Exception as e:
                #         print(f"Address error: {e}")

                # for item in urls_URL_WEBSITE:
                #     try:
                #         result = analyse_raw(GEMINI_API_KEY, URLWEBSITE_prompt(scrape_website(item)), 'URL WEBSITE')
                #         st.markdown(result)

                #         optimize_URL_WEBSITE.append(result)
                #     except Exception as e:
                #         print(f"Website error: {e}")

                # for item in urls_NETREVENUEYEARLY:
                #     try:
                #         result = analyse_raw(GEMINI_API_KEY, NETREVENUE_prompt(scrape_website(item)), 'NET REVENUE/YEARLY')
                #         st.markdown(result)

                #         optimize_NETREVENUEYEARLY.append(result)
                #     except Exception as e:
                #         print(f"Website error: {e}")

                # for item in urls_NOOFDOCTORS:
                #     try:
                #         result = analyse_raw(GEMINI_API_KEY, NOOFDOCTORS_prompt(scrape_website(item)), 'NO. OF DOCTORS')
                #         st.markdown(result)

                #         NOOFDOCTORS_optimize.append(result)
                #     except Exception as e:
                #         print(f"Website error: {e}")
                
                    
                # for item in urls_NO_OF_SPECIALTIES:
                #     try:
                #         result = analyse_raw(GEMINI_API_KEY, NOOFSPECIALTIES_prompt(scrape_website(item)), 'NO. OF SPECIALTIES')
                #         st.markdown(result)

                #         NO_OF_SPECIALTIES_optimize.append(result)
                #     except Exception as e:
                #         print(f"Website error: {e}")

                # st.markdown("##################### Optimize")
                # st.markdown(NO_OF_SPECIALTIES_optimize)
                # st.markdown(NOOFDOCTORS_optimize)
                # st.markdown(optimize_NETREVENUEYEARLY)
                # st.markdown(ADDRESS_optimize_search)
                # st.markdown(optimize_URL_WEBSITE)
                # st.markdown("#####################")
                # Final_ADDRESS_optimize_search=analyse_raw(GEMINI_API_KEY , analyze_extraction_results(ADDRESS_optimize_search ,"ADDRESS") ,"ADDRESS")
                # Final_optimize_URL_WEBSITE=analyse_raw(GEMINI_API_KEY , analyze_extraction_results(optimize_URL_WEBSITE  ,'URL WEBSITE') ,  'URL WEBSITE')
                # Final_optimize_NETREVENUEYEARLY=analyse_raw(GEMINI_API_KEY , analyze_extraction_results(optimize_NETREVENUEYEARLY , 'NET REVENUE/YEARLY') , 'NET REVENUE/YEARLY')
                # Final_NO_OF_SPECIALTIES_optimize=analyse_raw(GEMINI_API_KEY , analyze_extraction_results(NO_OF_SPECIALTIES_optimize , 'NO. OF SPECIALTIES') , 'NO. OF SPECIALTIES')
                # Final_NOOFDOCTORS_optimize=analyse_raw(GEMINI_API_KEY , analyze_extraction_results(NOOFDOCTORS_optimize , 'NO. OF DOCTORS') , 'NO. OF DOCTORS')
                # #airtable_add(research_output["result"] , API_KEY_AIRTABLE)
                # st.markdown("##################### Final")
                # st.markdown(Final_ADDRESS_optimize_search)
                # st.markdown(Final_optimize_URL_WEBSITE)
                # st.markdown(Final_optimize_NETREVENUEYEARLY)
                # st.markdown(Final_NO_OF_SPECIALTIES_optimize)
                # st.markdown(Final_NOOFDOCTORS_optimize)
                # st.markdown("#####################")
                Final_data={
                    'HCP NAME' : hospital_name ,
                    'STATUS' :  'Hospital',
                    'ADDRESS' : ADDRESS_search_result,
                    'CONTACT PERSON (CEO/MD/CFO/COO)' : CONTACT_PERSON_result,
                    # 'CONTACT NUMBER_Hospital' : CONTACT_NUMBER,
                    # 'CONTACT NUMBER_PERSON' : CONTACT_NUMBER,
                    # 'E-mail PERSON' : CONTACT_NUMBER,
                    # 'E-mail Hospital' : CONTACT_NUMBER,
                    'URL WEBSITE' : URL_WEBSITE,
                    'NET REVENUE/YEARLY' : NETREVENUEYEARLY,
                    'NO. OF SPECIALTIES' : NO_OF_SPECIALTIES ,
                    'NO. OF DOCTORS' :NOOFDOCTORS ,
                    'INSURANCES ACCEPTED' : INSURANCES_ACCEPTED
               }                
                st.subheader("Research Report")
                st.markdown('################')
                st.markdown(run_agent(Final_data))


    elif 'submitted' not in locals() or not submitted:
        with col2:
            st.header("Research Results")
            st.info("Enter a research topic and click 'Research This Topic' to begin.")

if __name__ == "__main__":
    main()

