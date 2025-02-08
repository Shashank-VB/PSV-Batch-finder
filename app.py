import pandas as pd
import math
import streamlit as st

# Title of the app
st.title("Polished Stone Value (PSV) Calculator Results")

# Sidebar for user inputs
st.sidebar.title("Polished Stone Value (PSV) Calculator")
st.sidebar.header("Enter values:")

# Input fields
aadt_value = st.sidebar.number_input("Enter AADT value:", min_value=0)
per_hgvs = st.sidebar.number_input("Enter % of HGVs:")
year = st.sidebar.number_input("Enter Year", min_value=0)
lanes = st.sidebar.number_input("Enter number of lanes", min_value=1)
link_section = st.sidebar.text_input("Enter Link Section:")

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
    AADT_HGVS = (per_hgvs * (aadt_value / 100))
else:
    AADT_HGVS = ((11 * aadt_value) / 100)

# Total projected AADT_HGVs
total_projected_aadt_hgvs = AADT_HGVS * ((1 + 1.54 / 100) ** design_period)
AADT_HGVS = round(AADT_HGVS)
total_projected_aadt_hgvs = round(total_projected_aadt_hgvs)

# Lane details
if lanes == 1:
    lane1 = 100
elif lanes == 2:
    lane1 = 50
    lane2 = 50
elif lanes == 3:
    lane1 = 33
    lane2 = 33
    lane3 = 34
else:
    lane1 = 25
    lane2 = 25
    lane3 = 25
    lane4 = 25

# Store lane values for display
lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1 / 100))
lane_details_lane2 = round(total_projected_aadt_hgvs * (lane2 / 100)) if lanes > 1 else 0
lane_details_lane3 = round(total_projected_aadt_hgvs * (lane3 / 100)) if lanes > 2 else 0
lane_details_lane4 = round(total_projected_aadt_hgvs * (lane4 / 100)) if lanes > 3 else 0

# PSV Calculation - Placeholder logic
value1 = st.sidebar.text_input("Enter Site Category:")
value2 = st.sidebar.number_input("Enter IL value:")
result1 = 'NA'
result2 = 'NA'
result3 = 'NA'

# Upload PSV lookup table (Excel file)
st.sidebar.header("Upload PSV Lookup Table")
uploaded_file = st.sidebar.file_uploader("Upload Excel file with PSV Lookup Table", type=["xlsx"])

if uploaded_file is not None:
    # Read the uploaded Excel file into a DataFrame
    df_psv_lookup = pd.read_excel(uploaded_file)

    # Display the first few rows of the uploaded PSV lookup table
    st.write("PSV Lookup Table (First 5 rows):")
    st.write(df_psv_lookup.head())

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

# Add result to session state when user clicks "Add Result"
if st.sidebar.button("Add Result"):
    entry = {
        "Link Section": link_section,
        "AADT_HGVS": AADT_HGVS,
        "Design Period": design_period,
        "Total Projected AADT HGVs": total_projected_aadt_hgvs,
        "Lane 1": lane1,
        "Lane 2": lane2 if lanes > 1 else 'NA',
        "Lane 3": lane3 if lanes > 2 else 'NA',
        "Lane 4": lane4 if lanes > 3 else 'NA',
        "Lane 1 Details": lane_details_lane1,
        "Lane 2 Details": lane_details_lane2,
        "Lane 3 Details": lane_details_lane3,
        "Lane 4 Details": lane_details_lane4,
        "PSV Lane 1": result1,
        "PSV Lane 2": result2,
        "PSV Lane 3": result3
    }
    st.session_state.results_list.append(entry)

# Display stored results
st.subheader("All Results:")
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
