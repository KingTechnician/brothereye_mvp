import streamlit as st
import markdown
import os
import io
import requests
import time
import pandas as pd
import base64
import pdfkit
from markdown_pdf import MarkdownPdf,Section
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

base_css="""
body {
  font-family: 'Orbitron', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  text-align: center;
  text-shadow: 0 0 5px rgba(0, 198, 255, 0.5);
}

p {
  margin: 10px 0;
}

.highlight {
  background-color: #24243e;
  padding: 10px;
  border-radius: 5px;
}



"""

api_link = "https://brothereye-cloud.onrender.com"

api_key = os.getenv("BROTHEREYE_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_current_job(job_id,job_type):
    base_url = f"{api_link}/api_job_status"

    data = {
        "job_id": job_id,
        "job_type": job_type
    }

    print(data)

    response = requests.get(base_url, headers=headers, json=data)

    if response.status_code == 200:
        print("approved")
    else:
        st.error("Job Not Found")

    return response.json()

def wait_for_geo_search_phase_to_finish(job_id,job_type,progress_bar):
    current_job = get_current_job(job_id,job_type)
    time.sleep(1)
    if(current_job["search_phase"]==0):
        progress_bar.progress(0)
        geo_search(job_id)
    elif current_job["search_phase"] == 100:
        progress_bar.progress(100)
        return

    while current_job["search_phase"] != 100:
        time.sleep(2)
        current_job = get_current_job(job_id,job_type)
        progress_bar.progress(current_job["search_phase"])


    return current_job

def wait_for_geo_marker_phase_to_finish(job_id,job_type,progress_bar):
    current_job = get_current_job(job_id,job_type)
    time.sleep(1)
    if(current_job["marker_phase"]==0):
        progress_bar.progress(0)
    elif current_job["marker_phase"] == 100:
        progress_bar.progress(100)
        return

    while current_job["marker_phase"] != 100:
        time.sleep(2)
        current_job = get_current_job(job_id,job_type)
        progress_bar.progress(current_job["marker_phase"])


    return current_job

def wait_for_geo_synopsis_phase_to_finish(job_id,job_type,progress_bar):
    current_job = get_current_job(job_id,job_type)
    time.sleep(1)
    if(current_job["synopsis_phase"]==0):
        progress_bar.progress(0)
    elif current_job["synopsis_phase"] == 100:
        progress_bar.progress(100)
        return

    while current_job["synopsis_phase"] != 100:
        time.sleep(2)
        current_job = get_current_job(job_id,job_type)
        progress_bar.progress(current_job["synopsis_phase"])

    return current_job

def wait_for_search_phase_to_finish(job_id,job_type,progress_bar):
    current_job = get_current_job(job_id,job_type)
    time.sleep(1)
    if(current_job["search_phase"]==0):
        progress_bar.progress(0)
        people_search(job_id)
    elif current_job["search_phase"] == 100:
        progress_bar.progress(100)
        return

    while current_job["search_phase"] != 100:
        time.sleep(2)
        current_job = get_current_job(job_id,job_type)
        progress_bar.progress(current_job["search_phase"])
    

    return current_job
def wait_for_additional_info_phase_to_finish(job_id,job_type,progress_bar):
    current_job = get_current_job(job_id,job_type)
    time.sleep(1)
    if(current_job["additional_info_phase"]==0):
        progress_bar.progress(0)
    elif current_job["additional_info_phase"] == 100:
        progress_bar.progress(100)
        return

    while current_job["additional_info_phase"] != 100:
        time.sleep(2)
        current_job = get_current_job(job_id,job_type)
        progress_bar.progress(current_job["additional_info_phase"])
    

    return current_job


def start_job(job_type,message):
    base_url = f"{api_link}/api_job"



    data = {
        "message": message,
        "job_type": job_type
    }

    response = requests.post(base_url, headers=headers, json=data)

    return response.json()

def geo_search(job_id):
    base_url = f"{api_link}/api_geo_search"

    headers = {
        "Authorization":f"Bearer {api_key}",
        "Content-Type":"application/json"
    }

    data = {
        "job_id":job_id
    }

    response = requests.post(base_url,headers=headers,json=data)

    if response.status_code == 200:
        print("Search Phase Started")
    else:
        raise Exception("Search Phase Failed to Start")

def people_search(job_id):
    base_url = f"{api_link}/api_people_search"

    headers = {
        "Authorization":f"Bearer {api_key}",
        "Content-Type":"application/json"
    }

    data = {
        "job_id":job_id
    }

    response = requests.post(base_url,headers=headers,json=data)

    if response.status_code == 200:
        print("Search Phase Started")
    else:
        raise Exception("Search Phase Failed to Start")
    
def create_pdf_from_html(html_content, filename):
    # Convert HTML content to PDF
    pdfkit.from_string(html_content, filename)

def create_download_link(pdf,filename):
    b64 = base64.b64encode(pdf)
    return f"<a href='data:application/octet-stream;base64,{b64.decode()}' download='{filename}.pdf'>Click here to download the PDF</a>"
 
st.set_page_config(page_title="BrotherEye MVP", page_icon="👁️")




def geo():
    job_type = "geo"
    st.write("Searches By Location")
    query_params = st.query_params

    try:
        if "geo_job_id" in query_params:
            st.session_state["geo_job_id"] = query_params["geo_job_id"]
            st.session_state["current_job"] = get_current_job(query_params["geo_job_id"],"geo")
        else:
            st.session_state["geo_job_id"] = None
            st.session_state["current_job"] = None
    except:
        pass
    
    if st.session_state.get("geo_job_id") is None:
        prompt = st.text_input("Describe the location you are looking for. What do you want us to find out about it?")

        if st.button("Submit",disabled=st.session_state.get("geo_job_id") is not None):
            response = start_job("geo",prompt)
            time.sleep(2)
            st.json(response)
            st.session_state["geo_job_id"] = response["job_id"]
            st.query_params.geo_job_id = response["job_id"]

            current_job = get_current_job(response["job_id"],job_type)

            st.session_state["current_job"] = current_job
            # send the request to the API
            # get the response
            # display the response

    

    geo_job = st.session_state.get("current_job")

    if geo_job is not None:
        with st.status("Handling your request. Check updates here..."):
            search_phase = st.progress(geo_job["search_phase"],"Searching for information about your location...")
            print(query_params)
            wait_for_geo_search_phase_to_finish(geo_job["id"],job_type,search_phase)
            marker_phase = st.progress(geo_job["marker_phase"],"Marking the location on the map...")
            wait_for_geo_marker_phase_to_finish(geo_job["id"],job_type,marker_phase)
            synopsis_phase = st.progress(geo_job["synopsis_phase"],"Creating a synopsis of the location...")
            wait_for_geo_synopsis_phase_to_finish(geo_job["id"],job_type,synopsis_phase)
            

        parsed_synopsis = ""
        if geo_job["synopsis"] is not None and 'title' in geo_job["synopsis"] and 'summary' in geo_job["synopsis"]:
            parsed_synopsis = f"# {geo_job['synopsis']['title']}\n\n{geo_job['synopsis']['summary']}\n\n"

        #geo_job['markers'], for each marker, have a string name, string reason, double lat, double long, string source, string map_link
        st.title("All Markers Found in this Investigation (May Need to Reload Page)")
        for marker in geo_job["markers"]:
            with st.expander(f"{marker['name']} - {marker['reason']}"):
                st.write(f"**Coordinates**: {marker['latitude']}, {marker['longitude']}")
                st.write(f"**Source**: {marker['source']}")
                st.write(f"**Map Link**: {marker['map_link'] if 'map_link' in marker else 'Not Available'}")
        # Create a dataframe with longitude column and latitude column for map

        # Display the map

        marker_frame = pd.DataFrame(geo_job["markers"])


        world_map = st.map(marker_frame,zoom=2)


        export_as_pdf = st.button("Export as PDF")

        

        if export_as_pdf:
            pdf = MarkdownPdf()
            final_report = f"\n\n{parsed_synopsis}\n\n# BrotherEye Location Report {geo_job['id']}\n\n{geo_job['search']}"
            pdf.add_section(Section(final_report,toc=False),user_css=base_css)
            
            buffer = io.BytesIO()
            pdf.save(buffer)


            st.markdown(create_download_link(buffer.getvalue(),f"Brothereye Location Report {geo_job['id']}"),unsafe_allow_html=True)


def people():
    job_type = "people"
    st.write('Searches By People')

    query_params = st.query_params

    try:

        if "people_job_id" in query_params:
            st.session_state["people_job_id"] = query_params["people_job_id"]
            print(query_params["people_job_id"])
            st.session_state["current_job"] = get_current_job(query_params["people_job_id"],"people")
        else:
            st.session_state["people_job_id"] = None
            st.session_state["current_job"] = None
    except:
        pass


    if st.session_state.get("people_job_id") is None:
        prompt = st.text_input("Describe the person(s) you are looking for. What do you want us to find out about them?")


        
        if st.button("Submit",disabled=st.session_state.get("people_job_id") is not None):
            
            response = start_job("people",prompt)
            time.sleep(2)
            st.json(response)
            st.session_state["people_job_id"] = response["job_id"]
            st.query_params.people_job_id = response["job_id"]

            current_job = get_current_job(response["job_id"],job_type)

            st.session_state["current_job"] = current_job
            # send the request to the API
            # get the response
            # display the response
    
    people_job = st.session_state.get("current_job")

    print(people_job)

    if people_job is not None:
        with st.status("Handling your request. Check updates here..."):
            search_phase = st.progress(people_job["search_phase"],"Searching for information about your person of interest...")
            print(query_params)
            wait_for_search_phase_to_finish(people_job["id"],job_type,search_phase)
            additional_info_phase = st.progress(people_job["additional_info_phase"],"Gathering additional information...")
            wait_for_additional_info_phase_to_finish(people_job["id"],job_type,additional_info_phase)

        

        st.markdown(people_job["search"])

        st.title("All People Involved in this Investigation")
        for person in people_job["additional_info"]:
            #Display name as title, list of descriptions as comma-separated subtitle, and misc as Streamlit chips
            with st.expander(str(person["name"])):
                st.subheader("Description")
                st.write(", ".join(person["description"]))
                st.subheader("Miscellaneous Information")
                st.write(f"**{(','.join(person['misc']))}**")


        export_as_pdf = st.button("Export as PDF")

        if export_as_pdf:
            pdf = MarkdownPdf()
            final_report = f"# BrotherEye People Report {people_job['id']}\n\n{people_job['search']}\n\n"
            pdf.add_section(Section(final_report,toc=False),user_css=base_css)
            
            buffer = io.BytesIO()
            pdf.save(buffer)


            st.markdown(create_download_link(buffer.getvalue(),f"Brothereye People Report {people_job['id']}"),unsafe_allow_html=True)

def home():
    st.title('BrotherEye MVP')
    st.write('Welcome to BrotherEye MVP! This is a minimal viable product for BrotherEye, a tool that implements information search and retrieval.')
    st.write("The magic is going to be at Search by Location and at Search by People. Click on the icons to navigate to the respective pages.")
    st.markdown("**Note: Please keep in mind that this only gathers from public information. We, in fact, do not have access to private information.**")
    st.markdown("**Another Note: This is going to be discrete and encrypted soon. But until then, I can read your stuff. So...just keep that in mind.**")

pg = st.navigation([
    st.Page(home, title="Information", icon="🏠"),
    st.Page(geo, title="Search By Location", icon="🗺️"),
    st.Page(people, title="Search By People", icon="🧘‍♀️")
])

pg.run()