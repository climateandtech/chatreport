import os
import json
import csv
import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def structure_data(report_name, answers, assessments, retrieved_chunks):
    data = []
    for question_id, answer in answers.items():
        assessment = assessments.get(question_id, {})
        relevant_chunks = retrieved_chunks.get(question_id, {}).values()
        
        data.append({
            "Report Name": report_name,
            "Question ID": question_id,
            "Question": answer.get("question", ""),
            "Answer": answer.get("answer", ""),
            "Sources": ", ".join(map(str, answer.get("sources", []))),
            "Pages": answer.get("pages", ""),  # Ensure this key exists in your JSON
            "Assessment": assessment.get("analysis", ""),
            "Score": assessment.get("score", ""),
            "Retrieved Chunks": " | ".join(relevant_chunks)
        })
    return data

def load_json_data(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                data[filename] = json.load(file)
    return data

def load_all_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                data.append(json.load(f))
    return data

def load_retrieved_chunks(directory):
    retrieved_chunks = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                retrieved_chunks.update(json.load(f))
    return retrieved_chunks

def load_all_data(answers_dir, assessment_dir, retrieved_chunks_dir):
    all_answers = load_all_json_files(answers_dir)
    all_assessments = load_all_json_files(assessment_dir)
    retrieved_chunks = load_retrieved_chunks(retrieved_chunks_dir)
    return all_answers, all_assessments, retrieved_chunks

def combine_data(all_answers, all_assessments):
    combined_answers = {k: v for d in all_answers for k, v in d.items()}
    combined_assessments = {k: v for d in all_assessments for k, v in d.items()}
    return combined_answers, combined_assessments

def generate_csv(data, output_path):
    keys = data[0].keys() if data else []
    with open(output_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def process_and_generate_csv(report_name, combined_answers, combined_assessments, retrieved_chunks, base_dir):
    structured_data = structure_data(report_name, combined_answers, combined_assessments, retrieved_chunks)
    question_set = os.path.basename(base_dir)
    csv_output_path = os.path.join(base_dir, f"{question_set}_answers_assessments.csv")
    generate_csv(structured_data, csv_output_path)

def create_csv_from_json(data_dir, question_set, output_dir):
    assessments_dir = os.path.join(data_dir, question_set, "assessment")
    
    # Load assessment data
    assessments = load_json_data(assessments_dir)

    all_data = [["Report Name", "TCFD Key", "Question", "Analysis", "Score"]]  # Initialize with header
    for report_filename, assessment_data in assessments.items():
        report_name = os.path.splitext(report_filename)[0]  # Extract report name without extension
        for tcfd_key, tcfd_data in assessment_data.items():
            row = [
                report_name,
                tcfd_key,
                tcfd_key,  # Assuming the TCFD key is the question
                tcfd_data.get("ANALYSIS", ""),
                tcfd_data.get("SCORE", "")
            ]
            all_data.append(row)

    # Write to CSV
    output_csv_path = os.path.join(data_dir, question_set, output_dir, f"{question_set}_answers_assessments.csv")
    with open(output_csv_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(all_data)