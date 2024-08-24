import yaml
import os
import csv
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def structure_data(report_name, answers, assessments, retrieved_chunks):
    data = []
    for question_id, answer in answers.items():
        assessment = assessments.get(question_id, {})
        data.append({
            "Report Name": report_name,
            "Question ID": question_id,
            "Question": answer.get("QUESTION", ""),
            "Answer": answer.get("ANSWER", ""),
            "Sources": ", ".join(map(str, answer.get("SOURCES", []))),
            "Pages": ", ".join(map(str, answer.get("PAGE", []))),
            "Assessment": assessment.get("ANALYSIS", ""),
            "Score": assessment.get("SCORE", ""),
            "Retrieved Chunks": " | ".join(retrieved_chunks.get(question_id, []))
        })
    return data

def read_existing_csv(csv_path):
    if not os.path.exists(csv_path):
        return []
    
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
    
def generate_csv(data, output_path):
    existing_data = read_existing_csv(output_path)
    combined_data = existing_data + data
    
    keys = combined_data[0].keys() if combined_data else data[0].keys()
    with open(output_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(combined_data)

    
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

def process_and_generate_csv(report_name, combined_answers, combined_assessments, retrieved_chunks, base_dir):
    structured_data = structure_data(report_name, combined_answers, combined_assessments, retrieved_chunks)
    question_set = os.path.basename(base_dir)
    csv_output_path = os.path.join(base_dir, f"{question_set}_answers_assessments.csv")
    generate_csv(structured_data, csv_output_path)

