import os, json
import argparse
from document import Report
from reader import Reader
from user_qa import UserQA
import webbrowser
import asyncio
from langchain.callbacks import get_openai_callback
from utils import load_config  # Import the utility function
from config import Config

# Function to load the configuration based on the question set
def load_question_set(question_set):
    file_path = f'question_sets/{question_set}.yaml'
    return config.load_config(file_path)

TOP_K = 20

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", type=str, default=None)
    parser.add_argument("--pdf_url", type=str, default=None)
    parser.add_argument("--basic_info_dir", type=str, default='data/basic_info')
    parser.add_argument("--llm_name", type=str, default='gpt-3.5-turbo')
    parser.add_argument("--answers_dir", type=str, default='data/answers')
    parser.add_argument("--assessment_dir", type=str, default='data/assessment')
    parser.add_argument("--vector_db_dir", type=str, default='data/vector_db')
    parser.add_argument("--retrieved_chunks_dir", type=str, default='data/retrieved_chunks')
    parser.add_argument("--user_qa_dir", type=str, default='data/user_qa')
    parser.add_argument("--user_question", type=str, default='')
    parser.add_argument("--answer_length", type=int, default=50)
    parser.add_argument("--detail", action='store_true', default=False)
    parser.add_argument("--top_k", type=int, default=20)
    parser.add_argument("--question_set", type=str, default='default', help="Specify the question set to use")
    args = parser.parse_args()

    config = Config(f'question_sets/{args.question_set}.yaml')


    if args.pdf_path:
        report_name = os.path.basename(args.pdf_path)
    else:
        assert (args.pdf_url is not None)
        report_name = args.pdf_url.split('/')[-1]
    assert report_name.endswith('.pdf')
    report_name = report_name.replace('.pdf', '')

    if not os.path.exists(args.basic_info_dir):
        os.makedirs(args.basic_info_dir)
    if not os.path.exists(args.answers_dir):
        os.makedirs(args.answers_dir)
    if not os.path.exists(args.assessment_dir):
        os.makedirs(args.assessment_dir)
    if not os.path.exists(args.vector_db_dir):
        os.makedirs(args.vector_db_dir)
    if not os.path.exists(args.retrieved_chunks_dir):
        os.makedirs(args.retrieved_chunks_dir)
    if not os.path.exists(args.user_qa_dir):
        os.makedirs(args.user_qa_dir)
    destination_folder = "data/pdf/"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    report = Report(
        path=args.pdf_path,
        url=args.pdf_url,
        store_path=os.path.join(destination_folder, report_name + '.pdf'),
        db_path=os.path.join(args.vector_db_dir, report_name),
        retrieved_chunks_path=os.path.join(args.retrieved_chunks_dir, report_name)
    )

    import pdb; pdb.set_trace()
    if args.user_question == None:
        try:
            reader = Reader(llm_name=args.llm_name, answer_length=str(args.answer_length))
            result_qa = asyncio.run(reader.qa_with_chat(report_list=[report]))
            result_analysis = asyncio.run(reader.analyze_with_chat(report_list=[report]))
        except Exception as e:
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = str(e)
            if "This model's maximum context length is" in msg:
                report = Report(
                    path=os.path.join(destination_folder, args.pdf_path.split('/')[-1]),
                    store_path=None,
                    top_k=TOP_K - 5,
                    db_path=os.path.join(args.vector_db_dir, report_name),
                    retrieved_chunks_path=os.path.join(args.retrieved_chunks_dir, report_name)
                )
                reader = Reader(llm_name=args.llm_name, answer_length=str(args.answer_length))
                result_qa = asyncio.run(reader.qa_with_chat(report_list=[report]))
                result_analysis = asyncio.run(reader.analyze_with_chat(report_list=[report]))

        html_path_qa = report_name + '_' + args.llm_name + '_qa.html'
        html_path_analysis = report_name + '_' + args.llm_name + '_analysis.html'
        with open(html_path_qa, 'w') as f:
            f.write(result_qa[0])
        with open(html_path_analysis, 'w') as f:
            f.write(result_analysis[0])
        with open(os.path.join(args.basic_info_dir, report_name + '_' + args.llm_name + '.json'), 'w') as f:
            json.dump(reader.basic_info_answers[0], f)
        with open(os.path.join(args.answers_dir, report_name + '_' + args.llm_name + '.json'), 'w') as f:
            json.dump(reader.answers[0], f)
        with open(os.path.join(args.assessment_dir, report_name + '_' + args.llm_name + '.json'), 'w') as f:
            json.dump(reader.assessment_results[0], f)
    else:
        qa = UserQA(llm_name=args.llm_name)
        answer, _ = qa.user_qa(
            args.user_question,
            report,
            basic_info_path=os.path.join(args.basic_info_dir, report_name + '_' + args.llm_name + '.json'),
            answer_length=args.answer_length,
        )
        print(answer)
        with open(os.path.join(args.user_qa_dir, report_name + '_' + args.llm_name + '.jsonl'), 'a') as f:
            qa_json = json.dumps(answer)
            f.write(qa_json + '\n')


if __name__ == '__main__':
    with get_openai_callback() as cb:
        main()
        print(cb)