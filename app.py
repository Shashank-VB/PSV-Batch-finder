import pandas as pd
import math
import streamlit as st

# Title of the app
st.title("Polished Stone Value (PSV) Calculator Results")

# Sidebar for user inputs
st.sidebar.title("Polished Stone Value (PSV) Calculator")
st.sidebar.header("Enter values:")

# Input fields
Site_Number = st.sidebar.text_input("Enter Site Number:")
link_section = st.sidebar.text_input("Enter Link Section:")
aadt_value = st.sidebar.number_input("Enter AADT value:", min_value=0)
per_hgvs = st.sidebar.number_input("Enter % of HGVs:")
year = st.sidebar.number_input("Enter Year", min_value=0)
lanes = st.sidebar.number_input("Enter number of lanes", min_value=1)

# Initialize session state to store results list
if "results_list" not in st.session_state:
    st.session_state.results_list = []

# Helper function to round up values
def roundup(value):
    return math.ceil(value)

# Design period calculation
if year == 0:
    design_period = 0
else:
    design_period = (20 + 2025) - year

# Calculation for AADT_HGVS
if per_hgvs >= 11:
    result1 = per_hgvs
    AADT_HGVS = (result1 * (aadt_value / 100))
else:
    result2 = 11
    AADT_HGVS = ((result2 * aadt_value) / 100)

# Total projected AADT_HGVs
total_projected_aadt_hgvs = AADT_HGVS * ((1 + 1.54 / 100) ** design_period)
AADT_HGVS = round(AADT_HGVS)
total_projected_aadt_hgvs = round(total_projected_aadt_hgvs)

# Lane details
lane1 = 0
lane2 = 0
lane3 = 0
lane4 = 0
lane_details_lane1 = 0
lane_details_lane2 = 0
lane_details_lane3 = 0
lane_details_lane4 = 0

if lanes == 1:
    lane1 = 100
    lane_details_lane1 = total_projected_aadt_hgvs
elif lanes > 1 and lanes <= 3:
    if total_projected_aadt_hgvs < 5000:
        lane1 = round(100 - (0.0036 * total_projected_aadt_hgvs))
        lane2 = round(100 - (100 - (0.0036 * total_projected_aadt_hgvs)))
    elif total_projected_aadt_hgvs >= 5000 and total_projected_aadt_hgvs < 25000:
        lane1 = round(89 - (0.0014 * total_projected_aadt_hgvs))
        lane2 = round(100 - lane1)
    elif total_projected_aadt_hgvs >= 25000:
        lane1 = 54
        lane2 = 100 - 54
        lane3 = 0
    lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1 / 100))
    lane_details_lane2 = round(total_projected_aadt_hgvs * (lane2 / 100))

elif lanes >= 4:
    if total_projected_aadt_hgvs <= 10500:
        lane1 = round(100 - (0.0036 * total_projected_aadt_hgvs))
        lane_2_3 = (total_projected_aadt_hgvs - ((total_projected_aadt_hgvs * lane1) / 100))
        lane2 = round(89 - (0.0014 * lane_2_3))
        lane3 = 100 - lane2
        lane4 = 0
    elif total_projected_aadt_hgvs > 10500 and total_projected_aadt_hgvs < 25000:
        lane1 = round(75 - (0.0012 * total_projected_aadt_hgvs))
        lane_2_3 = (total_projected_aadt_hgvs - ((total_projected_aadt_hgvs * lane1) / 100))
        lane2 = round(89 - (0.0014 * lane_2_3))
        lane3 = 100 - lane2
        lane4 = 0
    elif total_projected_aadt_hgvs >= 25000:
        lane1 = 45
        lane_2_3 = (total_projected_aadt_hgvs - ((total_projected_aadt_hgvs * lane1) / 100))
        lane2 = round(75 - (0.0012 * lane_2_3))
        lane3 = 100 - lane2
        lane4 = 0
    lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1 / 100))
    lane_details_lane2 = round((total_projected_aadt_hgvs * (lane2 / 100))
    lane_details_lane3 = round(total_projected_aadt_hgvs - (lane3 / 100))

# PSV Calculation - Placeholder logic (based on the upload of the PSV lookup table)
value1 = st.sidebar.text_input("Enter Site Category:")
value2 = st.sidebar.number_input("Enter IL value:")
result1 = 'NA'
result2 = 'NA'
result3 = 'NA'

# Upload PSV lookup table (Excel file)
st.sidebar.header("Upload DMRB CD 236 table 3.3b")
uploaded_file = st.sidebar.file_uploader("Upload Excel file with PSV Lookup Table", type=["xlsx"])

if uploaded_file is not None:
    # Read the uploaded Excel file into a DataFrame
    df_psv_lookup = pd.read_excel(uploaded_file)

    # Perform PSV Lookup based on inputs
    if value1 and value2:
        # Assuming the uploaded table has columns: 'SiteCategory', 'IL', and the range columns like '0-10', '10-20', etc.
        range_column = None
        for col in df_psv_lookup.columns:
            if '-' in col:
                col_range = list(map(int, col.split('-')))
                if col_range[0] <= lane_details_lane1 <= col_range[1]:
                    range_column = col
                    break
        
        if range_column:
            filtered_df = df_psv_lookup[(df_psv_lookup['SiteCategory'] == value1) & (df_psv_lookup['IL'] == value2)]
            if not filtered_df.empty:
                result1 = filtered_df.iloc[0][range_column]
            else:
                result1 = "No matching result found."
        else:
            result1 = "No matching range found for lane 1."

        # For Lane 2
        if lane_details_lane2 > 0:
            range_column = None
            for col in df_psv_lookup.columns:
                if '-' in col:
                    col_range = list(map(int, col.split('-')))
                    if col_range[0] <= lane_details_lane2 <= col_range[1]:
                        range_column = col
                        break
            
            if range_column:
                filtered_df = df_psv_lookup[(df_psv_lookup['SiteCategory'] == value1) & (df_psv_lookup['IL'] == value2)]
                if not filtered_df.empty:
                    result2 = filtered_df.iloc[0][range_column]
                else:
                    result2 = "No matching result found."
            else:
                result2 = "No matching range found for lane 2."

        # For Lane 3
        if lane_details_lane3 > 0:
            range_column = None
            for col in df_psv_lookup.columns:
                if '-' in col:
                    col_range = list(map(int, col.split('-')))
                    if col_range[0] <= lane_details_lane3 <= col_range[1]:
                        range_column = col
                        break
            
            if range_column:
                filtered_df = df_psv_lookup[(df_psv_lookup['SiteCategory'] == value1) & (df_psv_lookup['IL'] == value2)]
                if not filtered_df.empty:
                    result3 = filtered_df.iloc[0][range_column]
                else:
                    result3 = "No matching result found."
            else:
                result3 = "No matching range found for lane 3."

# Add result to session state when user clicks "Next Link Section"
if st.sidebar.button("Next Link Section"):
    entry = {
        "Site Number": Site_Number,
        "Link Section": link_section,
        "AADT Value": aadt_value,
        "percent hgv"     :per_hgvs,
        "Year of Data": year,
        "Lanes": lanes,
        "AADT of HGVs": AADT_HGVS,
        "Design Period": design_period,
        "Total Projected AADT of HGVs": total_projected_aadt_hgvs,
        "% HGV in Lane 1": lane1,
        "% HGV in Lane 2": lane2 if lanes > 1 else 'NA',
        "% HGV in Lane 3": lane3 if lanes > 2 else 'NA',
        "% HGV in Lane 4": lane4 if lanes > 3 else 'NA',
        "Design traffic Lane 1": lane_details_lane1,
        "Design traffic Lane 2": lane_details_lane2,
        "Design traffic Lane 3": lane_details_lane3,
        "Design traffic Lane 4": lane_details_lane4,
        "Min.PSV Lane 1": result1,
        "Min.PSV Lane 2": result2,
        "Min.PSV Lane 3": result3
    }
    st.session_state.results_list.append(entry)

# Display stored results with a collapsible section
st.subheader("PSV Calculation Results:")
with st.expander("View PSV Calculation Results", expanded=True):
    if st.session_state.results_list:
        df_results = pd.DataFrame(st.session_state.results_list)
        st.write(df_results)

        # Create a download button for CSV
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="Download All Results as CSV",
            data=csv,
            file_name="psv_results.csv",
            mime="text/csv"
        )
    else:
        st.write("No results added yet.")

# Collapsible section for editing results
with st.expander("Edit Results"):
    if st.session_state.results_list:
        df_results = pd.DataFrame(st.session_state.results_list)
        selected_index = st.selectbox("Select row to edit", options=range(len(df_results)), format_func=lambda x: f"Row {x+1}")
        
        if selected_index is not None:
            selected_row = df_results.iloc[selected_index]
            
            # Editable fields
            edited_site_number = st.text_input("Edit Site Number", value=selected_row["Site Number"])
            edited_link_section = st.text_input("Edit Link Section", value=selected_row["Link Section"])  
            edited_AADT_Value = st.text_input("Edit AADT Value", value=selected_row["AADT Value"])
            edited_percent_hgv = st.number_input("percent hgv", value=selected_row["percent hgv"])
            edited_year_of_Data = st.number_input("Year of Data", value=selected_row["Year of Data"])
            edited_Lanes = st.number_input("Lanes", value=selected_row["Lanes"])
                     
            # Update Button
            if st.button("Update Entry"):
                st.session_state.results_list[selected_index] = {
                    "Site Number": edited_site_number,
                    "Link Section": edited_link_section,
                    "AADT Value": edited_AADT_Value,
                    "percent hgv": edited_percent_hgv,
                    "Year of Data": edited_year_of_Data,
                    "Lanes": edited_Lanes
                }
                st.success("Entry updated successfully!")
                st.rerun()
    else:
        st.write("No results to edit.")
