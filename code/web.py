import streamlit as st
import os
import subprocess
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# This code was authored by Christian Woerle from Climate+Tech.
# For more information, visit our website at https://www.climateandtech.com.
# You can also check out Christian's GitHub at https://github.com/suung.





# Password protection
def check_password():
    def password_entered():
        if st.session_state["password"] == os.getenv("PASSWORD"):  # Get password from environment variable
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        st.stop()
    else:
        return True

if check_password():
    # Define directories
    input_dir = "input"
    output_dir = "output"
    data_dir = "data"
    question_sets_dir = "question_sets"

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load question sets
    question_sets = [f.replace('.yaml', '') for f in os.listdir(question_sets_dir) if f.endswith('.yaml')]
    # Streamlit app
    st.title("Climate+Tech Sustainability Report Analytics App")
    st.markdown("For more information, visit [Climate+Tech](https://www.climateandtech.com). For custom tool development, get in touch.")
    st.markdown("""
    This tool is based on the scientific research by Jingwei Ni, Julia Bingler, Chiara Colesanti-Senni, and others. For more details, refer to their paper [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4476733).
    """)

    # Dropdown for selecting question set
    question_set = st.selectbox("Select a Question Set", question_sets)


    # Download button for the selected question set
    if question_set:
        question_set_path = os.path.join(question_sets_dir, f"{question_set}.yaml")
        with open(question_set_path, "r") as file:
            question_set_content = file.read()
        st.download_button(
            label="Download Question Set",
            data=question_set_content,
            file_name=f"{question_set}.yaml",
            mime="text/yaml"
        )
    with st.expander("Customize questionset"):
        # File uploader for uploading a new question set
        uploaded_question_set = st.file_uploader("Upload a Question Set", type=["yaml"])
        if uploaded_question_set is not None:
            uploaded_question_set_path = os.path.join(question_sets_dir, uploaded_question_set.name)
            with open(uploaded_question_set_path, "wb") as file:
                file.write(uploaded_question_set.getbuffer())
            st.success(f"Uploaded {uploaded_question_set.name}")
            st.experimental_rerun()

    # File uploader for report
    uploaded_file = st.file_uploader("Upload a Report", type=["pdf"])

    if uploaded_file is not None:
        # Sanitize file name
        sanitized_filename = os.path.basename(uploaded_file.name)
        report_path = os.path.join(input_dir, sanitized_filename)
        
        # Save uploaded file to input directory
        with open(report_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {sanitized_filename}")

    # Run the app script with the selected input and question set
    if st.button("Run Analysis"):
        with st.spinner("Running analysis..."):
            # Define the command to run the app script
            command = [
                "python", "code/app.py",  # Adjusted to include the relative path to app.py
                "--pdf_path", report_path,
                "--question_set", question_set
            ]
            # Run the command and capture output
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Analysis completed successfully!")
                st.text(result.stdout)  # Display standard output
                # Copy the generated CSV to the output directory
                csv_filename = f"{question_set}_answers_assessments.csv"
                csv_path = os.path.join(data_dir, question_set, csv_filename)
                if os.path.exists(csv_path):
                    shutil.copy(csv_path, os.path.join(output_dir, csv_filename))
                    st.success(f"CSV file generated: {csv_filename}")
                    # Offer the user to download the CSV
                    with open(os.path.join(output_dir, csv_filename), "rb") as f:
                        st.download_button(
                            label="Download CSV",
                            data=f,
                            file_name=csv_filename,
                            mime="text/csv"
                        )
                else:
                    st.error("CSV file not found.")
            else:
                st.error("Error running analysis.")
                st.text(result.stderr)

    selected_reports = []
    # List report names in the data directory
    if question_set:
        question_set_dir = os.path.join(data_dir, question_set)
        if os.path.exists(question_set_dir):
            report_names = set()
            for file in os.listdir(question_set_dir):
                if file.endswith(f"{question_set}_answers_assessments.csv"):
                    csv_path = os.path.join(question_set_dir, file)
                    df = pd.read_csv(csv_path)
                    report_names.update(df['Report Name'].unique())
            report_names = list(report_names)
            selected_reports = st.multiselect("Select Reports to Compare", report_names, default=report_names)
    else:
        st.warning("Please select a question set.")

    if selected_reports:
        data_frames = []
        for report in selected_reports:
            for file in os.listdir(question_set_dir):
                if file.endswith(f"{question_set}_answers_assessments.csv"):
                    csv_path = os.path.join(question_set_dir, file)
                    df = pd.read_csv(csv_path)
                    if report in df['Report Name'].unique():
                        df = df[df['Report Name'] == report]
                        df['Report'] = report
                        data_frames.append(df)

        if data_frames:
            combined_df = pd.concat(data_frames)
            st.dataframe(combined_df)

            # Plot the scores per TCFD and report using a radar chart
            if "Score" in combined_df.columns:
                st.subheader("Scores per TCFD and Report")
                radar_data = combined_df.pivot(index='Question ID', columns='Report', values='Score').fillna(0)
                st.write(radar_data)  # Debugging line to check the data

                # Create radar chart using Matplotlib
                labels = radar_data.index
                num_vars = len(labels)

                # Compute angle for each axis
                angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                angles += angles[:1]

                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                
                # Define different line styles and colors
                line_styles = ['-', '--', '-.', ':']
                colors = plt.cm.viridis(np.linspace(0, 1, len(radar_data.columns)))
                
                for i, report in enumerate(radar_data.columns):
                    values = radar_data[report].tolist()
                    values += values[:1]
                    
                    # Add a small offset to each report's data
                    offset = np.random.normal(0, 0.01, len(values))
                    values = [v + o for v, o in zip(values, offset)]
                    
                    ax.plot(angles, values, label=report, linestyle=line_styles[i % len(line_styles)], color=colors[i])
                
                ax.set_yticklabels([])
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

                st.pyplot(fig)
    else:
        st.warning("No reports selected for comparison.")

    # Always display the download button if the CSV file exists
    csv_filename = f"{question_set}_answers_assessments.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            st.download_button(
                label="Download CSV",
                key="download_csv",
                data=f,
                file_name=csv_filename,
                mime="text/csv"
            )

# Create a Streamlit footer
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
.footer img {
    height: 30px;
    vertical-align: middle;
    margin-right: 10px;
}
</style>
<div class="footer">
    <img src="https://www.climateandtech.com/climateandtech.png" alt="Climate+Tech Logo">
    <p>Climate+Tech Sustainability Report Analysis Tool</p>
    <p>Based on <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4476733" target="_blank">this paper</a> by Jingwei Ni, Julia Bingler, Chiara Colesanti Senni, Mathias Kraus, Glen Gostlow, Tobias Schimanski, Dominik Stammbach, Saeid Vaghefi, Qian Wang, Nicolas Webersinke, Tobias Wekhof, Tingyu Yu, and Markus Leippold</p>
    <p>For custom tool development contact us at <a href="https://www.climateandtech.com" target="_blank">www.climateandtech.com</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

