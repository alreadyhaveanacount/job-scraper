import streamlit as st
import pandas as pd
from job_scraper import load_page

st.title("Job Scrapper")

query = st.text_input("Job function?")
page_range = st.slider("Starting - Ending Page", 1, 50, (1, 10), 1)
employment_types = st.multiselect("Wanted employment types", ["full_time", "part_time", "contract"])
workplace_location = st.multiselect("Workplace location", ["remote", "hybrid", "on_site"])
seniority = st.multiselect("Minimal seniority level", ["entry_level", "mid_level", "senior", "manager", "director", "executive"])
travel_frequency = st.selectbox("Travel frequency", ("Not relevant", "never", "sometimes", "often"))
compensation_currency = st.selectbox("Compensation currency", ("USD", "CAD", "EUR", "GBP", "AUD"))
compensation = st.number_input("Minimal salary", step=0.01, min_value=0.0, format="%.2f")
footer = st.container()

def scrape_for_jobs():
    buffer = []

    arguments = {
        "compensationCurrency": compensation_currency
    }

    if query != "": arguments["query"] = query
    if len(employment_types) > 0: arguments["employmentType"] = employment_types
    if len(workplace_location) > 0: arguments["workplaceLocation"] = workplace_location
    if len(seniority) > 0: arguments["seniority"] = seniority
    if travel_frequency != "Not relevant": arguments["travelFrequency"] = travel_frequency
    if compensation > 0: arguments["compensation"] = compensation * 100

    with footer:
        progress = st.progress(0)

    for current_page in range(page_range[0], page_range[1]+1):
        if current_page > 1:
            arguments["page"] = current_page
        
        load_page(buffer, arguments)

        progress.progress(current_page/page_range[1])

    data = pd.DataFrame(buffer)

    with footer:
        st.write("Result:")
        st.write(data)
        st.download_button("Download data CSV", data.to_csv().encode("utf-8"), "job_scraped.csv")

with footer:
    st.button("Scrape!", on_click=scrape_for_jobs, type="primary")