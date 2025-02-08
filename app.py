import pandas as pd
import math
import streamlit as st
import io

# Title
st.title("Polished Stone Value (PSV) Calculator Results")

# Input parameters
st.sidebar.title ("Polished Stone Value (PSV) Calculator")
st.sidebar.header ("Enter values:")

# Create a form to enter multiple link sections
link_sections = st.sidebar.text_area("Enter Link Sections (separate with commas)", "")

# Convert the link sections to a list
link_section_list = [link.strip() for link in link_sections.split(',') if link.strip()]

# Other input fields (they remain the same)
aadt_value = st.sidebar.number_input("Enter AADT value:", min_value=0)
per_hgvs = st.sidebar.number_input("Enter % of HGVs:")
year = st.sidebar.number_input("Enter Year", min_value=0)
lanes = st.sidebar.number_input("Enter number of Lanes", min_value=1)

# Initialize result lists for each section
results = []

def roundup(value):
    return math.ceil(value)

if year == 0:
    design_period = 0
elif year != 0:
    design_period = ((20 + 2025) - year)

# Process each link section
for link_section in link_section_list:
    # Calculation
    if per_hgvs >= 11:
        result1 = per_hgvs
        AADT_HGVS = (result1 * (aadt_value / 100))
    else:
        result2 = 11
        AADT_HGVS = ((result2 * aadt_value) / 100)

    total_projected_aadt_hgvs = (AADT_HGVS * (1 + 1.54 / 100) ** design_period)
    AADT_HGVS = round(AADT_HGVS)
    total_projected_aadt_hgvs = round(total_projected_aadt_hgvs)

    # Calculate lane percentages
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
            lane2 = 54
            lane3 = 100 - 54
        lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1 / 100))
        lane_details_lane2 = round((total_projected_aadt_hgvs - lane_details_lane1) * (lane2 / 100))
        lane_details_lane3 = round(total_projected_aadt_hgvs - (lane_details_lane1 + lane_details_lane2))

    # PSV Calculation
    value1 = st.sidebar.text_input("Enter Site Category:")
    value2 = st.sidebar.number_input("Enter IL value:")
    value3 = lane_details_lane1
    value4 = lane_details_lane2
    value5 = lane_details_lane3

    # Assuming the uploaded Excel data and matching the results
    # For simplicity, using placeholders for PSV results
    result = 'NA'
    result2 = 'NA'
    result3 = 'NA'

    # Append each section's result to the list
    results.append({
        'Link Section': link_section,
        'AADT_HGVS': AADT_HGVS,
        'Design Period': design_period,
        'Total Projected AADT HGVs': total_projected_aadt_hgvs,
        'Lane 1': lane1,
        'Lane 2': lane2,
        'Lane 3': lane3,
        'Lane 4': lane4,
        'Lane 1 Details': lane_details_lane1,
        'Lane 2 Details': lane_details_lane2,
        'Lane 3 Details': lane_details_lane3,
        'Lane 4 Details': lane_details_lane4,
        'PSV Lane 1': result,
        'PSV Lane 2': result2,
        'PSV Lane 3': result3,
    })

# Convert to DataFrame for output
df_results = pd.DataFrame(results)

# Display the DataFrame on the Streamlit page
st.write("PSV Results Output", df_results)

# Convert the DataFrame to CSV
csv_data = df_results.to_csv(index=False)

# Create a download button for the CSV file
st.download_button(
    label="Download Results as CSV",
    data=csv_data,
    file_name='psv_results.csv',
    mime='text/csv'
)
