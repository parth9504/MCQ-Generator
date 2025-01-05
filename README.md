**Learn Mate: Companion for Learning**
This project aims to provide an AI driven based platform to learners, to evaluate their learning by **summarizing text**, generating **objective** and **subjective questions**.

The proposed project leverages cutting-edge natural language processing (NLP) techniques to  create an AI-driven platform for summarizing and evaluating textual data. The platform is designed to process uploaded documents, including .docx and .pdf files, using Python libraries like python-docx and PyPDF2. This functionality ensures broad compatibility with various document formats, making it accessible to diverse user needs. Once the document is uploaded, the first step involves generating an abstractive summary of the content using the Pegasus model, a state-of-the-art transformer designed specifically for text summarization. The model condenses the text into a coherent and contextually accurate summary, enabling users to grasp the essence of lengthy materials effortlessly.

Attached below is the workflow of this project.
![Input Files (Formats like  pdf, docx)](https://github.com/user-attachments/assets/9146b67a-cc9f-40c4-b827-94cd566e13a9)

**Project Overview**
This project encompasses the following features:

**1. Document Uploading**
The platform supports .docx and .pdf file formats, utilizing Python libraries such as python-docx and PyPDF2 for file parsing and text extraction. This ensures compatibility with widely used document formats, allowing users to effortlessly upload their study materials.

**2. Text Summarization**
The text summarization process is powered by the Pegasus model, a state-of-the-art transformer architecture for abstractive summarization. This model condenses lengthy text into concise, contextually relevant summaries, enabling users to focus on the most important information without reading the entire document. Summarization serves as the foundation for subsequent question generation.

**3. Multiple-Choice Question Generation**
The MCQ generation process involves the following steps:

- **Relevant Sentence Selection**: Summarized content is analyzed to identify sentences with significant information.
- **Keyword Identification**: Important keywords, including nouns, pronouns, adjectives, dates, numbers, and values, are extracted and ranked based on their contextual importance.
- **Blank Creation**: Critical keywords are replaced with blanks to form fill-in-the-blank-style questions.
- **Distractor Generation**: Using the Sense2Vec library, contextually similar but incorrect options (distractors) are generated. These distractors enhance the quality of MCQs by making them more challenging and thought-provoking.
4. Subjective Question Generation
For subjective questions, the platform uses a transformer model (T5) trained on the SQuAD dataset which is available on Hugging Face Transformers too. The process includes:

- **Sentence Selection**: Specific sentences from the summarized content are chosen.
- **Keyword Identification**: Key elements within the sentences are extracted and treated as potential answers.
- **Question Formation**: The context and extracted keywords are passed to the T5 model, which generates relevant and well-aligned questions based on the provided content.




