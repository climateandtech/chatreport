# key: topic, value: list of search key
# temperature for generation
temperature = 0.

# size of retrieving chunks (number of characters)
chunk_size = 500
# overlap length between chunks
chunk_overlap = 20
# whether to use document compression
compression = False
# similarity threshold to remove the less-related chunks (from the retrieved top-k)
similarity_threshold = 0.76
# how many related chunks to be retrieved?
retriever_top_k = 20

retrieval_queries = {
    'general': ["What is the company of the report?", "What sector does the company belong to?", "Where is the company located?",
                #"What carbon emissions-related issues are discussed in this report?"
          ],
    'tcfd_1': "How does the company’s board oversee carbon emissions-related risks and opportunities in its sustainability strategy?",
    'tcfd_2': "How detailed and complete are the metrics disclosed in the environment section concerning carbon emissions?",
    'tcfd_3': "What are the most relevant carbon emissions-related risks and opportunities that the organization has identified over the short, medium, and long term? Are risks clearly associated with a specific timeframe?",
    'tcfd_4': "Does the organization disclose its Scope 1, Scope 2, and, if appropriate, Scope 3 greenhouse gas (GHG) emissions? What are the related risks, and do they differ depending on the scope?",
    'tcfd_5': "How are the processes for identifying, assessing, and managing carbon emissions-related risks integrated into the organization’s overall risk management?",
    'tcfd_6': "How well is the carbon emissions data presented? Does it include visual aids such as infographics, and are key points clearly highlighted?",
    'tcfd_7': "How clearly does the report define the perimeter of activities and locations covered by the carbon emissions data?",
    'tcfd_8': "To what extent does the carbon emissions reporting include all of the company’s operations, including international activities?",
    'tcfd_9': "How thoroughly has the information in the report related to carbon emissions been audited by an external party?",
}


tcfds = {
    'tcfd_1': "The board's oversight of carbon emissions-related risks and opportunities",
    'tcfd_2': "The completeness and detail of metrics disclosed within the environment section concerning carbon emissions",
    'tcfd_3': "The carbon emissions-related risks and opportunities the organization has identified over the short, medium, and long term",
    'tcfd_4': "Scope 1, Scope 2, and, if appropriate, Scope 3 greenhouse gas (GHG) emissions, and the associated risks",
    'tcfd_5': "How processes for identifying, assessing, and managing carbon emissions-related risks are integrated into the organization's overall risk management",
    'tcfd_6': "The clarity and effectiveness of the presentation of carbon emissions data, including the use of visual aids such as infographics and the highlighting of key points",
    'tcfd_7': "The clarity in defining the perimeter of activities and locations covered by the carbon emissions data",
    'tcfd_8': "The comprehensiveness of the carbon emissions reporting in covering all of the company’s operations, including international activities",
    'tcfd_9': "The extent to which the carbon emissions data in the report has been audited by an external party",
}


tcfd_assessment = {
    'tcfd_1': """In describing the board's oversight of carbon emissions-related risks and opportunities, organizations should consider including a discussion of the following:
1. processes and frequency by which the board and/or board committees (e.g., audit, risk, or other committees) are informed about carbon emissions-related issues;
2. whether the board and/or board committees consider carbon emissions-related issues when reviewing and guiding strategy, major plans of action, risk management policies, annual budgets, and business plans as well as setting the organization’s performance objectives, monitoring implementation and performance, and overseeing major capital expenditures, acquisitions, and divestitures; and 
3. how the board monitors and oversees progress against goals and targets for addressing carbon emissions-related issues.
""",
    'tcfd_2': """In describing the metrics disclosed in the environment section concerning carbon emissions, organizations should consider providing the following information:
1. a comprehensive list of the specific metrics used to measure and report carbon emissions, covering all scopes (Scope 1, Scope 2, and, if appropriate, Scope 3);
2. the degree of detail and granularity in these metrics, including any benchmarks or targets set by the organization; and
3. how these metrics align with industry standards or regulations, and how they contribute to the organization’s overall carbon management strategy.
""",
    'tcfd_3': """In describing the carbon emissions-related risks and opportunities the organization has identified over the short, medium, and long term, organizations should consider providing the following information:
1. a clear description of what the organization considers to be the relevant short-, medium-, and long-term time horizons, taking into consideration the useful life of the organization's assets or infrastructure;
2. a detailed description of the specific carbon emissions-related issues potentially arising in each time horizon (short, medium, and long term) that could have a material financial impact on the organization; and
3. an explanation of the process(es) used to determine which risks and opportunities could have a material financial impact on the organization. Organizations should consider providing a description of their risks and opportunities by sector and/or geography, as appropriate.
""",
    'tcfd_4': """In describing impact of climate-related risks and opportunities on the organization's businesses, strategy, and financial planning, organizations should discuss how identified climate-related issues have affected their businesses, strategy, and financial planning:
1. a comprehensive disclosure of Scope 1, Scope 2, and, where relevant, Scope 3 GHG emissions, in line with recognized methodologies such as the GHG Protocol;
2. an assessment of the risks associated with each scope, and how these risks differ across scopes; and
3. A description of the methodologies used to calculate or estimate these emissions, ensuring transparency and comparability.
""",
    'tcfd_5': """In describing the integration of processes for identifying, assessing, and managing carbon emissions-related risks into the organization’s overall risk management, organizations should consider including the following:
1. a description of how carbon emissions-related risks are incorporated into the broader enterprise risk management framework; 
2. an explanation of how these risks are prioritized relative to other risks, including the criteria used for determining their significance; and
3. the specific processes used for monitoring and mitigating these risks over time, including any feedback mechanisms or continuous improvement processes.
""",
    'tcfd_6': """In describing the clarity and effectiveness of the presentation of carbon emissions data, organizations should consider discussing:
1. the use of visual aids such as infographics, charts, and tables to enhance the clarity of carbon emissions data;
2. the highlighting of key points and metrics to ensure they are easily identifiable and understandable; and 
3. the overall structure and readability of the report, including the avoidance of dense text blocks that could hinder comprehension.
""",
    'tcfd_7': """In describing the perimeter of activities and locations covered by the carbon emissions data, organizations should consider including:
1. a clear definition of the geographic and operational boundaries covered by the carbon emissions data;
2. an explanation of any exclusions or limitations in the data coverage, including the rationale for these exclusions; and
3. a description of how the defined perimeter aligns with the organization’s overall business operations and carbon management strategy. 
""",
    'tcfd_8': """In describing the comprehensiveness of the carbon emissions reporting in covering all of the company’s operations, including international activities, organizations should consider providing:
1. a detailed account of how the carbon emissions reporting covers all relevant business units, subsidiaries, and international operations;
2. an assessment of any areas where data might be incomplete or less accurate, along with steps taken to address these gaps; and
3. a discussion on how the organization ensures that the reporting is consistent across all operations, including those in different jurisdictions or regulatory environments.
""",
    'tcfd_9': """In describing the extent to which the carbon emissions data in the report has been audited by an external party, organizations should consider including:
1. a clear statement on which sections of the carbon emissions data have been independently audited, and by whom;
2. an explanation of the auditing process, including the standards or guidelines followed; and
3. a discussion of any areas where data was not audited, including the reasons for this and the potential impact on the overall accuracy and reliability of the report.
""",
}

# Make QA more critical
tcfd_guidelines = {
    'tcfd_1': """8. Please focus specifically on the board's direct oversight of carbon emissions-related risks and opportunities within the sustainability strategy. Avoid discussing broader corporate risk management systems or unrelated topics.
""",
    'tcfd_2': """8. Please focus on the detail and completeness of the metrics disclosed in the environment section concerning carbon emissions. Do not include broader environmental metrics that do not directly pertain to carbon emissions.
""",
    'tcfd_3': """8. Please focus solely on the identification of carbon emissions-related risks and opportunities over the specified timeframes (short, medium, and long term). Avoid discussing the company-wide risk management system or unrelated risks.
""",
    'tcfd_4': """8. Confirm the disclosure of Scope 1, Scope 2, and, if appropriate, Scope 3 greenhouse gas (GHG) emissions. Provide any available data or specific figures on these emissions. Focus on the risks directly related to these emissions rather than general climate-related risks.
""",
    'tcfd_5': """8. Please focus on how the processes for identifying, assessing, and managing carbon emissions-related risks are integrated into the organization’s overall risk management. Exclude discussions on broader risk identification or unrelated management strategies.
""",
    'tcfd_6': """8. Please focus on the clarity and effectiveness of the presentation of carbon emissions data, particularly the use of visual aids such as infographics and the clear highlighting of key points. Avoid discussing the content of the data itself.
""",
    'tcfd_7': """8. Please provide a clear analysis of how well the report defines the perimeter of activities and locations covered by the carbon emissions data. Avoid discussing any aspects outside the defined perimeter.
""",
    'tcfd_8': """8. Please focus on the comprehensiveness of the carbon emissions reporting in covering all of the company’s operations, including international activities. Avoid discussing operations outside the scope of the carbon emissions reporting.
""",
    'tcfd_9': """8. Please focus on the extent to which the carbon emissions data in the report has been audited by an external party. Provide details on which sections have been audited and by whom. Avoid discussing non-carbon-related data or general audit practices.
""",
}
system_prompt = "You are an AI assistant in the role of a Senior Equity Analyst with expertise in climate science that analyzes companys' sustainability reports."

prompts = {
    'general':
        """You are tasked with the role of a climate scientist, assigned to analyze a company's sustainability report. Based on the following extracted parts from the sustainability report, answer the given QUESTIONS. 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Format your answers in JSON format with the following keys: COMPANY_NAME, COMPANY_SECTOR, and COMPANY_LOCATION.

QUESTIONS: 
1. What is the company of the report?
2. What sector does the company belong to? 
3. Where is the company located?

=========
{context}
=========
Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
    'tcfd_qa_source': """As a senior equity analyst with expertise in climate science evaluating a company's sustainability report, you are presented with the following background information:

{basic_info}

With the above information and the following extracted components of the sustainability report at hand, please respond to the posed question, ensuring to reference the relevant parts ("SOURCES").
Format your answer in JSON format with the two keys: ANSWER (this should contain your answer string without sources), and SOURCES (this should be a list of the source numbers that were referenced in your answer).

QUESTION: {question}
=========
{summaries}
=========

Please adhere to the following guidelines in your answer:
1. Your response must be precise, thorough, and grounded on specific extracts from the report to verify its authenticity.
2. If you are unsure, simply acknowledge the lack of knowledge, rather than fabricating an answer.
3. Keep your ANSWER within {answer_length} words.
4. Be skeptical to the information disclosed in the report as there might be greenwashing (exaggerating the firm's environmental responsibility). Always answer in a critical tone.
5. cheap talks are statements that are costless to make and may not necessarily reflect the true intentions or future actions of the company. Be critical for all cheap talks you discovered in the report.
6. Always acknowledge that the information provided is representing the company's view based on its report.
7. Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements, and communicate your findings.
{guidelines}

Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
    'user_qa_source': """As a senior equity analyst with expertise in climate science evaluating a company's sustainability report, you are presented with the following background information:

{basic_info}

With the above information and the following extracted components of the sustainability report at hand, please respond to the posed question, ensuring to reference the relevant parts ("SOURCES").
Format your answer in JSON format with the two keys: ANSWER (this should contain your answer string without sources), and SOURCES (this should be a list of the source numbers that were referenced in your answer).

QUESTION: {question}
=========
{summaries}
=========

Please adhere to the following guidelines in your answer:
1. Your response must be precise, thorough, and grounded on specific extracts from the report to verify its authenticity.
2. If certain information is unclear or unavailable, admit the lack of knowledge rather than devising an answer.
3. Answer the question strictly based on the provided extracts. If the information available is insufficient, clearly state that the question cannot be answered based on the given report.
4. Keep your ANSWER within {answer_length} words.
5. Be skeptical to the information disclosed in the report as there might be greenwashing (exaggerating the firm's environmental responsibility). Always answer in a critical tone.
6. cheap talks are statements that are costless to make and may not necessarily reflect the true intentions or future actions of the company. Be critical for all cheap talks you discovered in the report.
7. Always acknowledge that the information provided is representing the company's view based on its report.
8. Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements, and communicate your findings.

Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
    'tcfd_summary_source': """Your task is to analyze and summarize any disclosures related to the following <CRITICAL_ELEMENT> in a company's sustainability report:

<CRITICAL_ELEMENT>: {question}

Provided below is some basic information about the company under evaluation:

{basic_info}

In addition to the above, the following extracted sections of the sustainability report have been made available to you for review:

{summaries}

Your task is to summarize the company's disclosure of the aforementioned <CRITICAL_ELEMENT>, based on the information presented in these extracts. Please adhere to the following guidelines in your summary:
1. If the <CRITICAL_ELEMENT> is disclosed in the report, try to summarize by direct extractions from the report. Reference the source of this information from the provided extracts to confirm its credibility.
2. If the <CRITICAL_ELEMENT> is not addressed in the report, state this clearly without attempting to extrapolate or manufacture information.
3. Keep your SUMMARY within {answer_length} words.
4. Be skeptical to the information disclosed in the report as there might be greenwashing (exaggerating the firm's environmental responsibility). Always answer in a critical tone.
5. cheap talks are statements that are costless to make and may not necessarily reflect the true intentions or future actions of the company. Be critical for all cheap talks you discovered in the report.
6. Always acknowledge that the information provided is representing the company's view based on its report.
7. Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements, and communicate your findings.
{guidelines}

Your summarization should be formatted in JSON with two keys:
1. SUMMARY: This should contain your summary without source references.
2. SOURCES: This should be a list of the source numbers that were referenced in your summary.

Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
    'tcfd_qa': """As a senior equity analyst with expertise in climate science evaluating a company's sustainability report, you are presented with the following essential information about the report:

{basic_info}

With the above information and the following extracted components of the sustainability report at hand, please respond to the posed question. 
Your answer should be precise, comprehensive, and substantiated by direct extractions from the report to establish its credibility.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

QUESTION: {question}
=========
{summaries}
=========
""",
    'tcfd_assessment': """Your task is to rate a sustainability report's disclosure quality on the following <CRITICAL_ELEMENT>:

<CRITICAL_ELEMENT>: {question}

These are the <REQUIREMENTS> that outline the necessary components for high-quality disclosure pertaining to the <CRITICAL_ELEMENT>:

<REQUIREMENTS>:
---
{requirements}
---

Presented below are select excerpts from the sustainability report, which pertain to the <CRITICAL_ELEMENT>:

<DISCLOSURE>:
---
{disclosure}
---

Please analyze the extent to which the given <DISCLOSURE> satisfies the aforementioned <REQUIREMENTS>. Your ANALYSIS should specify which <REQUIREMENTS> have been met and which ones have not been satisfied.
Your response should be formatted in JSON with two keys:
1. ANALYSIS: A paragraph of analysis (be in a string format). No longer than 150 words.
2. SCORE: An integer score from 0 to 100. A score of 0 indicates that most of the <REQUIREMENTS> have not been met or are insufficiently detailed. In contrast, a score of 100 suggests that the majority of the <REQUIREMENTS> have been met and are accompanied by specific details.

Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
    'scoring': """Your task is to rate the disclosure quality of a sustainability report. You'll be provided with a <REPORT SUMMARY> that contains {question_number} (DISCLOSURE_REQUIREMENT, DISCLOSURE_CONTENT) pairs. DICLOSURE_REQUIREMENT corresponds to a key piece of information that the report should disclose. DISCLOSURE_CONTENT summarizes the report's disclosed information on that topic. 
For each pair, you should assign a score reflecting the depth and comprehensiveness of the disclosed information. A score of 1 denotes a detailed and comprehensive disclosure. A score of 0.5 suggests that the disclosed information is lacking in detail. A score of 0 indicates that the requested information is either not disclosed or is disclosed without any detail.
Please format your response in a JSON structure, with the keys 'COMMENT' (providing your overall assessment of the report's quality) and 'SCORES' (a list containing the {question_number} scores corresponding to each question-and-answer pair).

<REPORT SUMMARY>:
---
{summaries}
---
Your FINAL_ANSWER in JSON (ensure there's no format error):
""",
  'to_question': """Examine the following statement and transform it into a question, suitable for a ChatGPT prompt, if it is not already phrased as one. If the statement is already a question, return it as it is.
Statement: {statement}"""
#     'scoring': """Your role is that of a climate scientist rating the disclosure quality of a sustainability report. You'll be provided with a <REPORT SUMMARY> that contains {question_number} question-and-answer pairs. Each pair corresponds to a key piece of information that the report should disclose, with the answer summarizing the report's disclosed information on that topic. Your responsibility is to assess the quality of these disclosures.
# For each question-and-answer pair, assign a score based on the question-anwering quality and the disclosure detailedness and comprehensiveness. If the question is thoroughly answered and the disclosed information is thoroughly detailed, assign a score of 1. If the question is only partially answered or the dsclosed information lacks substantial detail, assign a score of 0.5. If the information asked by the question is either not disclosed or disclosed without any detail, assign a score of 0.
# Please format your response in a JSON structure, with the keys 'COMMENT' (providing your overall assessment of the report's quality) and 'SCORES' (a list containing the {question_number} scores corresponding to each question-and-answer pair).

# <REPORT SUMMARY>:
# ---
# {summaries}
# ---
# FINAL_ANSWER in JSON (ensure there's no format error):
# """,
}