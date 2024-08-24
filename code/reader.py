import os
import re
import tenacity
import markdown
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts import PromptTemplate
import cfg
import json
import tiktoken

from config import Config
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# main class for reading the pdf and communicate with openai

TOP_K = 20


import os
import csv



def remove_brackets(string):
    return re.sub(r'\([^)]*\)', '', string).strip()

def _docs_to_string(docs, num_docs=TOP_K, with_source=True):
    output = ""
    docs = docs[:num_docs]
    for doc in docs:
        output += "Content: {}\n".format(doc.page_content)
        if with_source:
            output += "Source: {}\n".format(doc.metadata['source'])
        output += "\n---\n"
    return output

def _find_answer(string, name="ANSWER"):
    for l in string.split('\n'):
        if name in l:
            start = l.find(":") + 3
            end = len(l) - 1
            return l[start:end]
    return string

def _find_sources(string):
    pattern = r'\d+'
    numbers = [int(n) for n in re.findall(pattern, string)]
    return numbers

def _find_float_numbers(string):
    pattern = r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
    float_numbers = [float(n) for n in re.findall(pattern, string)]
    return float_numbers

def _find_score(string):
    for l in string.split('\n'):
        if "SCORE" in l:
            d = re.search(r'[-+]?\d*\.?\d+', l)
            break
    return d[0]

class Reader:
    def __init__(self, llm_name='gpt-3.5-turbo', answer_key_name='ANSWER', max_token=512, q_name='Q', a_name='A',
                 answer_length='60', root_path='./', gitee_key='', user_name='default', language='en', question_set=None):
        self.user_name = user_name  # user name
        self.language = language
        self.root_path = root_path
        self.max_token = max_token
        self.llm_name = llm_name
        self.tiktoken_encoder = tiktoken.encoding_for_model(self.llm_name)
        self.cur_api = 0
        self.file_format = 'md'  # or 'txt'
        self.answer_key_name = answer_key_name
        self.q_name = q_name
        self.a_name = a_name
        self.answer_length = answer_length
        self.basic_info_answers = []
        self.answers = []
        self.assessment_results = []
        self.user_questions = []
        self.user_answers = []
        self.question_set = question_set
        self.qa_prompt = 'tcfd_qa_source'
        self.prompts = cfg.prompts
        self.system_prompt = cfg.system_prompt
        self.assessments = question_set['assessments']
        self.queries = question_set['questions']
        self.guidelines = question_set['guidelines']

    async def qa_with_chat(self, report_list):
        htmls = []
        for report_index, report in enumerate(report_list):
            basic_info_prompt = PromptTemplate(template=self.prompts['general'], input_variables=["context"])
            if "turbo" in self.llm_name:
                message = [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=basic_info_prompt.format(
                        context=_docs_to_string(report.section_text_dict['general'], with_source=False)))
                ]
                llm = ChatOpenAI(temperature=0, max_tokens=256)
                output_text = llm(message).content
            else:
                message = basic_info_prompt.format(
                    context=_docs_to_string(report.section_text_dict['general'], with_source=False))
                llm = OpenAI(temperature=0, max_tokens=256)
                output_text = llm(message)
            print(output_text)
            try:
                basic_info_dict = json.loads(output_text)
            except ValueError as e:
                basic_info_dict = {'COMPANY_NAME': _find_answer(output_text, name='COMPANY_NAME'),
                                   'COMPANY_SECTOR': _find_answer(output_text, name='COMPANY_SECTOR'),
                                   'COMPANY_LOCATION': _find_answer(output_text, name='COMPANY_LOCATION')}
            basic_info_string = """Company name: {name}\nCompany sector: {sector}\nCompany Location: {location}""" \
                .format(name=basic_info_dict['COMPANY_NAME'], sector=basic_info_dict['COMPANY_SECTOR'],
                        location=basic_info_dict['COMPANY_LOCATION'])
            self.basic_info_answers.append(basic_info_dict)

            tcfd_questions = {k: v for k, v in self.queries.items() if 'tcfd' in k}
            tcfd_prompt = PromptTemplate(template=self.prompts[self.qa_prompt],
                                         input_variables=["basic_info", "summaries", "question", "guidelines",
                                                          "answer_length"])
            answers = {}
            messages = []
            keys = []
            for k, q in tcfd_questions.items():
                num_docs = 20
                current_prompt = tcfd_prompt.format(basic_info=basic_info_string,
                                                    summaries=_docs_to_string(report.section_text_dict[k]),
                                                    question=q, guidelines=self.guidelines[k],
                                                    answer_length=self.answer_length)
                if '16k' not in self.llm_name:
                    while len(self.tiktoken_encoder.encode(current_prompt)) > 3500 and num_docs > 10:
                        num_docs -= 1
                        current_prompt = tcfd_prompt.format(basic_info=basic_info_string, summaries=_docs_to_string(report.section_text_dict[k], num_docs=num_docs), question=q, guidelines=self.guidelines[k], answer_length=self.answer_length)
                if "turbo" in self.llm_name:
                    message = [
                        SystemMessage(content=self.system_prompt),
                        HumanMessage(content=current_prompt)
                    ]
                else:
                    message = current_prompt
                keys.append(k)
                messages.append(message)
            if "turbo" in self.llm_name:
                llm = ChatOpenAI(temperature=0, max_tokens=512)
            else:
                llm = OpenAI(temperature=0, max_tokens=512)
            outputs = await llm.agenerate(messages)
            output_texts = {k: g[0].text for k, g in zip(keys, outputs.generations)}

            for k, text in output_texts.items():
                try:
                    answers[k] = json.loads(text)
                    if 'SOURCES' not in answers[k].keys() or self.answer_key_name not in answers[k].keys():
                        raise ValueError("Key name(s) not defined!")
                except ValueError as e:
                    answers[k] = {self.answer_key_name: _find_answer(text, name=self.answer_key_name),
                                  'SOURCES': _find_sources(text)}
                page_source = []
                for s in answers[k]['SOURCES']:
                    try:
                        page_source.append(report.page_idx[s])
                    except Exception as e:
                        pass
                answers[k]['PAGE'] = list(set(page_source))
                answers[k][self.answer_key_name] = remove_brackets(answers[k][self.answer_key_name])
                print(answers[k])
            self.answers.append(answers)

            questionnaire_governance = ""
            questionnaire_strategy = ""
            questionnaire_risk = ""
            questionnaire_metrics = ""
            for idx, (k, q) in enumerate(tcfd_questions.items()):
                if 2 > idx >= 0:
                    if idx == 0:
                        questionnaire_governance += "In governance:\n\n"
                    questionnaire_governance += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_governance += self.a_name + "{}: {}\n\n".format(int(idx + 1),
                                                                                  answers[k][self.answer_key_name])
                    questionnaire_governance += "\n"
                elif 5 > idx >= 2:
                    if idx == 2:
                        questionnaire_strategy += "In strategy:\n\n"
                    questionnaire_strategy += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_strategy += self.a_name + "{}: {}\n\n".format(int(idx + 1),
                                                                                answers[k][self.answer_key_name])
                    questionnaire_strategy += "\n"
                elif 8 > idx >= 5:
                    if idx == 5:
                        questionnaire_risk += "In risk management:\n\n"
                    questionnaire_risk += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_risk += self.a_name + "{}: {}\n\n".format(int(idx + 1),
                                                                            answers[k][self.answer_key_name])
                    questionnaire_risk += "\n"
                elif idx >= 8:
                    if idx == 8:
                        questionnaire_metrics += "In metrics and targets:\n\n"
                    questionnaire_metrics += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_metrics += self.a_name + "{}: {}\n\n".format(int(idx + 1),
                                                                               answers[k][self.answer_key_name])
                    questionnaire_metrics += "\n"
            questionnaire = questionnaire_governance + questionnaire_strategy + questionnaire_risk + questionnaire_metrics

            htmls.append(markdown.markdown(questionnaire))
        return htmls

    async def analyze_with_chat(self, report_list):
        htmls = []
        for report_index, report in enumerate(report_list):
            tcfd_assessment_prompt = PromptTemplate(template=self.prompts['tcfd_assessment'],
                                                    input_variables=["question", "requirements", "disclosure"])
            tcfd_questions = {k: v for k, v in self.queries.items() if 'tcfd' in k}
            assessments = {}
            messages = []
            keys = []
            for idx, k in enumerate(self.assessments.keys()):
                num_docs = 20
                current_prompt = tcfd_assessment_prompt.format(question=self.queries[k],
                                                               requirements=self.assessments[k],
                                                               disclosure=_docs_to_string(
                                                                   report.section_text_dict[k], with_source=False))
                if '16k' not in self.llm_name:
                    while len(self.tiktoken_encoder.encode(current_prompt)) > 3200 and num_docs > 10:
                        num_docs -= 1
                        current_prompt = tcfd_assessment_prompt.format(question=self.queries[k],
                                                                       requirements=self.assessments[k],
                                                                       disclosure=_docs_to_string(
                                                                           report.section_text_dict[k],
                                                                           num_docs=num_docs,
                                                                           with_source=False))
                if "turbo" in self.llm_name:
                    message = [
                        SystemMessage(content=self.system_prompt),
                        HumanMessage(content=current_prompt)
                    ]
                else:
                    message = current_prompt
                keys.append(k)
                messages.append(message)
            if "turbo" in self.llm_name:
                llm = ChatOpenAI(temperature=0, max_tokens=512)
            else:
                llm = OpenAI(temperature=0, max_tokens=512)
            outputs = await llm.agenerate(messages)
            output_texts = {k: g[0].text for k, g in zip(keys, outputs.generations)}

            for k, text in output_texts.items():
                try:
                    assessments[k] = json.loads(text)
                    if 'SCORE' not in assessments[k].keys() or 'ANALYSIS' not in assessments[k].keys():
                        raise ValueError("Key name(s) not defined!")
                except ValueError as e:
                    assessments[k] = {'ANALYSIS': _find_answer(text, name='ANALYSIS'),
                                      'SCORE': _find_score(text)}
                analysis_text = remove_brackets(assessments[k]['ANALYSIS'])
                if "<CRITICAL_ELEMENT>" in analysis_text:
                    analysis_text = analysis_text.replace("<CRITICAL_ELEMENT>", "TCFD recommendation point")
                if "<DISCLOSURE>" in analysis_text:
                    analysis_text = analysis_text.replace("<DISCLOSURE>", "report's disclosure")
                if "<REQUIREMENTS>" in analysis_text:
                    analysis_text = analysis_text.replace("<REQUIREMENTS>", "TCFD guidelines")
                assessments[k]['ANALYSIS'] = analysis_text
                print(assessments[k])
            self.assessment_results.append(assessments)

            questionnaire_governance = ""
            questionnaire_strategy = ""
            questionnaire_risk = ""
            questionnaire_metrics = ""
            for idx, (k, q) in enumerate(tcfd_questions.items()):
                if 2 > idx >= 0:
                    if idx == 0:
                        questionnaire_governance += "In governance:\n\n"
                    questionnaire_governance += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_governance += "Analysis{}: {}\n\n".format(int(idx + 1), assessments[k]['ANALYSIS'])
                    questionnaire_governance += "Score{}: {}\n\n".format(int(idx + 1), assessments[k]['SCORE'])
                    questionnaire_governance += "\n"
                elif 5 > idx >= 2:
                    if idx == 2:
                        questionnaire_strategy += "In strategy:\n\n"
                    questionnaire_strategy += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_strategy += "Analysis{}: {}\n\n".format(int(idx + 1), assessments[k]['ANALYSIS'])
                    questionnaire_strategy += "Score{}: {}\n\n".format(int(idx + 1), assessments[k]['SCORE'])
                    questionnaire_strategy += "\n"
                elif 8 > idx >= 5:
                    if idx == 5:
                        questionnaire_risk += "In risk management:\n\n"
                    questionnaire_risk += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_risk += "Analysis{}: {}\n\n".format(int(idx + 1), assessments[k]['ANALYSIS'])
                    questionnaire_risk += "Score{}: {}\n\n".format(int(idx + 1), assessments[k]['SCORE'])
                    questionnaire_risk += "\n"
                elif idx >= 8:
                    if idx == 8:
                        questionnaire_metrics += "In metrics and targets:\n\n"
                    questionnaire_metrics += self.q_name + "{}: {}\n\n".format(int(idx + 1), q)
                    questionnaire_metrics += "Analysis{}: {}\n\n".format(int(idx + 1), assessments[k]['ANALYSIS'])
                    questionnaire_metrics += "Score{}: {}\n\n".format(int(idx + 1), assessments[k]['SCORE'])
                    questionnaire_metrics += "\n"
            questionnaire = questionnaire_governance + questionnaire_strategy + questionnaire_risk + questionnaire_metrics
            all_scores = [float(s['SCORE']) for s in assessments.values()]

            htmls.append(markdown.markdown(questionnaire + '\n\n' + "Average score: {}".format(sum(all_scores) / 11)))
        return htmls