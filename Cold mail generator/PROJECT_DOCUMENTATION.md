# Campus Invitation Mail Generator - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Components Deep Dive](#components-deep-dive)
6. [Complete Data Flow](#complete-data-flow)
7. [Step-by-Step Working](#step-by-step-working)
8. [Setup and Installation](#setup-and-installation)
9. [Configuration](#configuration)
10. [Error Handling](#error-handling)

---

## 🎯 Project Overview

### Purpose
The **Campus Invitation Mail Generator** is an AI-powered application designed to automate the process of sending personalized campus recruitment invitation emails to companies. It analyzes job postings from company career pages and generates customized invitation letters highlighting relevant student capabilities and portfolio projects.

### Use Case
**Scenario**: HBTU Kanpur's Placement Coordinator (Abhijeet Kushwaha) needs to invite companies for on-campus recruitment drives. Instead of manually analyzing job requirements and crafting emails, the system:
- Extracts job details from company career pages
- Matches job requirements with student portfolios
- Generates professional, personalized invitation emails
- Includes relevant portfolio links to showcase student capabilities

### Key Benefits
- ✅ **Time Efficiency**: Automates email generation process
- ✅ **Personalization**: Each email is tailored to specific job requirements
- ✅ **Smart Matching**: AI-powered semantic search matches skills with portfolios
- ✅ **Professional Output**: Consistent, well-formatted invitation letters
- ✅ **Scalability**: Handle multiple job postings simultaneously

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Streamlit Web App)                          │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ URL Input
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WEB SCRAPING LAYER                          │
│                 (LangChain WebBaseLoader)                       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ Raw HTML Content
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TEXT PROCESSING LAYER                         │
│               (Utils - Text Cleaning)                           │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ Cleaned Text
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI EXTRACTION LAYER                        │
│            (Groq LLM - Job Information Extraction)              │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ Structured Job Data (JSON)
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SEMANTIC SEARCH LAYER                         │
│              (ChromaDB - Vector Database)                       │
│           Portfolio Skills ← → Job Skills Matching              │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ Relevant Portfolio Links
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EMAIL GENERATION LAYER                        │
│          (Groq LLM - Personalized Email Writing)                │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ Generated Email
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT DISPLAY                             │
│              (Streamlit UI - Markdown Format)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | Streamlit | 1.35.0+ | User interface and application framework |
| **LLM Provider** | Groq API | - | Fast LLM inference (Llama 3.3 70B) |
| **LLM Framework** | LangChain | 0.2.14 | LLM orchestration and prompt management |
| **Vector Database** | ChromaDB | 0.5.0+ | Semantic search and embeddings storage |
| **Web Scraping** | LangChain Community | 0.2.12 | Web content extraction |
| **Data Processing** | Pandas | 2.0.2+ | Portfolio data management |
| **Text Cleaning** | Regex (re) | Built-in | HTML and text preprocessing |
| **Environment** | Python-dotenv | 1.0.0 | Secure API key management |

### Additional Dependencies
- **Selenium**: Browser automation (if dynamic content loading needed)
- **Unstructured**: Document parsing
- **BeautifulSoup4**: HTML parsing (via dependencies)

---

## 📁 Project Structure

```
project-genai-cold-email-generator-main/
│
├── app/                                    # Main application directory
│   ├── main.py                            # Streamlit app entry point
│   ├── chains.py                          # LLM chain logic (extraction & email)
│   ├── portfolio.py                       # Portfolio management & vector search
│   ├── utils.py                           # Utility functions (text cleaning)
│   ├── .env                               # Environment variables (API keys)
│   └── resource/
│       └── my_portfolio.csv               # Portfolio database (skills & links)
│
├── vectorstore/                           # ChromaDB persistent storage
│   ├── chroma.sqlite3                     # SQLite database for metadata
│   └── [collection_id]/                   # Vector embeddings storage
│       ├── data_level0.bin
│       ├── header.bin
│       ├── length.bin
│       └── link_lists.bin
│
├── imgs/                                  # Documentation images
│   └── architecture.png
│
├── email_generator.ipynb                  # Jupyter notebook for testing
├── tutorial_groq.ipynb                    # Groq API tutorial
├── tutorial_chromadb.ipynb                # ChromaDB tutorial
├── my_portfolio.csv                       # Portfolio data (root copy)
├── requirements.txt                       # Python dependencies
├── README.md                              # Project README
├── .gitignore                             # Git ignore rules
└── PROJECT_DOCUMENTATION.md               # This file
```

---

## 🔍 Components Deep Dive

### 1. **main.py** - Application Entry Point

**Purpose**: Orchestrates the entire application flow and provides the user interface.

**Key Functions**:

```python
def create_streamlit_app(llm, portfolio, clean_text):
    """
    Main application function that:
    1. Creates Streamlit UI
    2. Accepts URL input from user
    3. Coordinates all components
    4. Displays generated emails
    """
```

**Responsibilities**:
- 🎨 Render Streamlit UI (title, input field, button)
- 🔗 Accept career page URL from user
- 📥 Load web content using WebBaseLoader
- 🧹 Clean extracted text
- 📊 Initialize portfolio vector database
- 🤖 Extract job information via LLM
- 🔍 Query portfolio for matching skills
- ✉️ Generate personalized emails
- 📤 Display output in markdown format
- ⚠️ Handle errors gracefully

**Workflow Logic**:
```
User Input (URL) 
    ↓
Load Web Content 
    ↓
Clean Text 
    ↓
Load Portfolio to VectorDB 
    ↓
Extract Jobs (LLM) 
    ↓
For Each Job:
    ├→ Get Skills
    ├→ Validate Skills Format
    ├→ Query Matching Portfolio Links
    ├→ Generate Email (LLM)
    └→ Display Email
```

---

### 2. **chains.py** - LLM Chain Management

**Purpose**: Manages all LLM interactions using LangChain framework.

#### Class: `Chain`

**Initialization**:
```python
def __init__(self):
    self.llm = ChatGroq(
        temperature=0,              # Deterministic output
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )
```

**Method 1: `extract_jobs(cleaned_text)`**

**Purpose**: Extract structured job information from career page text.

**Input**: 
- `cleaned_text` (string): Preprocessed text from career page

**Process**:
1. Creates a prompt template with instructions
2. Sends cleaned text to LLM
3. Requests JSON output with specific keys
4. Parses LLM response into Python dict/list
5. Validates and returns job data

**Output Format**:
```json
[
    {
        "role": "Software Engineer",
        "experience": "2-4 years",
        "skills": ["Python", "Django", "MySQL", "REST API"],
        "description": "We are seeking a talented software engineer..."
    }
]
```

**Error Handling**:
- Catches `OutputParserException` if context is too large
- Ensures return value is always a list (even for single job)

**Method 2: `write_mail(job, links)`**

**Purpose**: Generate personalized invitation email based on job requirements.

**Input**:
- `job` (dict): Job information extracted earlier
- `links` (list): Relevant portfolio links from semantic search

**Prompt Engineering**:
- Role: Abhijeet Kushwaha, Placement Coordinator at HBTU Kanpur
- Context: Inviting company for on-campus MCA recruitment
- Requirements:
  - Highlight HBTU MCA student capabilities
  - Match job requirements with student skills
  - Include relevant portfolio links
  - Professional tone with emojis
  - Proper line breaks for readability
  - Include contact information

**Output**: 
- Raw email content (markdown formatted string)

---

### 3. **portfolio.py** - Portfolio Management & Semantic Search

**Purpose**: Manages student portfolio data and provides semantic search capabilities.

#### Class: `Portfolio`

**Initialization**:
```python
def __init__(self, file_path="app/resource/my_portfolio.csv"):
    # Load portfolio CSV
    self.data = pd.read_csv(file_path, encoding="latin1")
    
    # Initialize ChromaDB client (persistent storage)
    self.chroma_client = chromadb.PersistentClient('vectorstore')
    
    # Get or create collection
    self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
```

**Method 1: `load_portfolio()`**

**Purpose**: Load portfolio data into vector database (if not already loaded).

**Process**:
1. Check if collection is empty
2. If empty, iterate through CSV rows
3. For each row:
   - Extract techstack (e.g., "Python, Django, MySQL")
   - Create embedding automatically (ChromaDB handles this)
   - Store with metadata (portfolio link)
   - Assign unique UUID

**Vector Database Structure**:
```
Document: "Python, Django, MySQL"
Metadata: {"links": "https://example.com/python-portfolio"}
ID: "uuid-generated-string"
Embedding: [0.234, -0.123, 0.456, ...] (automatically generated)
```

**Method 2: `query_links(skills)`**

**Purpose**: Find relevant portfolio links based on job skills using semantic search.

**Input**: 
- `skills` (list): Job skills extracted by LLM (e.g., ["Python", "Django"])

**Process**:
1. **Validation**: Check if skills list is non-empty
2. **Semantic Search**: 
   - Convert skills to embeddings
   - Find similar documents in vector database
   - Use cosine similarity for matching
   - Return top 2 most relevant results
3. **Extract Metadata**: Get portfolio links from matched documents

**Example**:
```python
# Input
skills = ["Python", "Django", "REST API"]

# ChromaDB finds similar embeddings
# Matches: "Python, Django, MySQL" (high similarity)
#          "Python, Flask, PostgreSQL" (medium similarity)

# Output
[
    {"links": "https://example.com/python-portfolio"},
    {"links": "https://example.com/flask-portfolio"}
]
```

**Why Semantic Search?**
- Understands context (Django ≈ Flask ≈ Web Framework)
- Handles synonyms (JavaScript ≈ JS, Machine Learning ≈ ML)
- More flexible than exact keyword matching

---

### 4. **utils.py** - Text Processing Utilities

**Purpose**: Clean and preprocess raw HTML/text content.

**Function: `clean_text(text)`**

**Purpose**: Remove noise from scraped web content.

**Cleaning Steps**:

1. **Remove HTML Tags**:
   ```python
   text = re.sub(r'<[^>]*?>', '', text)
   # <div>Hello</div> → Hello
   ```

2. **Remove URLs**:
   ```python
   text = re.sub(r'http[s]?://(?:...)+', '', text)
   # Visit https://example.com → Visit 
   ```

3. **Remove Special Characters**:
   ```python
   text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
   # Hello@World! → Hello World
   ```

4. **Normalize Whitespace**:
   ```python
   text = re.sub(r'\s{2,}', ' ', text)
   # Hello    World → Hello World
   ```

5. **Trim and Clean**:
   ```python
   text = text.strip()
   text = ' '.join(text.split())
   ```

**Why Clean Text?**
- LLMs perform better with clean input
- Reduces token count (cost optimization)
- Removes navigation, footer, and irrelevant content
- Focuses on actual job description content

---

### 5. **my_portfolio.csv** - Portfolio Database

**Structure**:
```csv
Techstack,Links
"React, Node.js, MongoDB",https://example.com/react-portfolio
"Python, Django, MySQL",https://example.com/python-portfolio
"Java, Spring Boot, Oracle",https://example.com/java-portfolio
```

**Fields**:
- **Techstack**: Comma-separated skills/technologies
- **Links**: Portfolio/project URLs showcasing those skills

**Usage**:
- Loaded into ChromaDB as vector embeddings
- Used for semantic matching with job requirements
- Can be easily updated with new projects

---

## 🔄 Complete Data Flow

### Detailed End-to-End Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: USER INPUT                                              │
│ User enters career page URL in Streamlit interface              │
│ Example: https://careers.netapp.com/job/...                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: WEB SCRAPING                                            │
│ WebBaseLoader fetches HTML content from URL                     │
│ Output: Raw HTML with all page elements                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: TEXT CLEANING                                           │
│ utils.clean_text() processes raw content:                       │
│   • Removes HTML tags                                           │
│   • Strips URLs                                                 │
│   • Removes special characters                                  │
│   • Normalizes whitespace                                       │
│ Output: Clean, readable text                                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: PORTFOLIO LOADING                                       │
│ portfolio.load_portfolio() checks ChromaDB:                     │
│   • If empty: Load CSV → Create embeddings → Store              │
│   • If exists: Skip (use cached data)                           │
│ Result: Vector database ready for search                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: JOB EXTRACTION (LLM Call #1)                           │
│ Chain.extract_jobs(cleaned_text):                              │
│   1. Create prompt with cleaned text                            │
│   2. Send to Groq LLM (Llama 3.3 70B)                          │
│   3. LLM analyzes and extracts job info                         │
│   4. Parse JSON response                                        │
│ Output: Structured job data (role, skills, experience, desc)    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: ITERATE JOBS                                            │
│ For each extracted job posting:                                 │
│   ┌───────────────────────────────────────┐                    │
│   │ STEP 6a: Extract Skills               │                    │
│   │ Get skills from job.get('skills', []) │                    │
│   │ Validate: ensure it's a list          │                    │
│   └──────────────┬────────────────────────┘                    │
│                  ▼                                              │
│   ┌───────────────────────────────────────┐                    │
│   │ STEP 6b: Semantic Search              │                    │
│   │ Portfolio.query_links(skills):        │                    │
│   │   • Convert skills to embeddings      │                    │
│   │   • Search ChromaDB for similar docs  │                    │
│   │   • Return top 2 matching portfolios  │                    │
│   └──────────────┬────────────────────────┘                    │
│                  ▼                                              │
│   ┌───────────────────────────────────────┐                    │
│   │ STEP 6c: Email Generation (LLM #2)   │                    │
│   │ Chain.write_mail(job, links):        │                    │
│   │   • Create personalized prompt        │                    │
│   │   • Include job details + portfolio   │                    │
│   │   • Send to Groq LLM                 │                    │
│   │   • Generate invitation email         │                    │
│   └──────────────┬────────────────────────┘                    │
│                  ▼                                              │
│   ┌───────────────────────────────────────┐                    │
│   │ STEP 6d: Display Email               │                    │
│   │ st.code(email, language='markdown')  │                    │
│   │ Show formatted email in UI            │                    │
│   └───────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: USER REVIEWS OUTPUT                                    │
│ User sees all generated emails in Streamlit interface           │
│ Can copy and send to respective companies                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Working

### Phase 1: Application Initialization

**1. Import Dependencies**
```python
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
```

**2. Initialize Components**
```python
chain = Chain()          # Initialize LLM with Groq API
portfolio = Portfolio()  # Initialize portfolio manager
st.set_page_config(...)  # Configure Streamlit page
```

**3. Launch Streamlit App**
```bash
streamlit run app/main.py
```

---

### Phase 2: User Interaction

**4. Display UI**
- Title: "📧 Campus Invitation Mail Generator"
- Input field: URL text box (pre-filled with example)
- Submit button: Triggers processing

**5. User Input**
- User pastes company career page URL
- Example: `https://careers.netapp.com/job/bengaluru/software-engineering-manager/27600/90339827328`
- Clicks "Submit" button

---

### Phase 3: Data Extraction

**6. Web Scraping**
```python
loader = WebBaseLoader([url_input])
raw_data = loader.load().pop().page_content
```
- WebBaseLoader sends HTTP request to URL
- Receives HTML response
- Extracts page content including text, tags, scripts, etc.

**7. Text Cleaning**
```python
cleaned_data = clean_text(raw_data)
```
- Removes all HTML tags: `<div>`, `<span>`, etc.
- Strips navigation menus, footers, sidebars
- Removes URLs and special characters
- Result: Clean, plain text of job description

---

### Phase 4: Portfolio Preparation

**8. Load Portfolio**
```python
portfolio.load_portfolio()
```

**First-time execution**:
- Read `my_portfolio.csv` with Pandas
- For each row:
  - Document: "Python, Django, MySQL"
  - Metadata: {"links": "https://..."}
  - ChromaDB automatically creates embeddings
  - Stores in `vectorstore/` directory

**Subsequent executions**:
- Check if ChromaDB collection has data
- If yes, skip loading (use existing vectors)
- This saves time and API calls

---

### Phase 5: Job Information Extraction

**9. LLM Extraction Call**
```python
jobs = llm.extract_jobs(cleaned_data)
```

**What happens internally**:

**Prompt sent to LLM**:
```
### SCRAPED TEXT FROM WEBSITE:
[cleaned career page text]

### INSTRUCTION:
Extract job postings in JSON format with keys:
role, experience, skills, description

### VALID JSON (NO PREAMBLE):
```

**LLM Response**:
```json
{
    "role": "Software Engineering Manager",
    "experience": "8+ years",
    "skills": ["Team Leadership", "Java", "Microservices", "Cloud"],
    "description": "Lead a team of engineers..."
}
```

**Processing**:
- LangChain's `JsonOutputParser` parses the response
- Validates JSON structure
- Converts to Python dictionary
- Wraps in list if single job: `[job_dict]`

---

### Phase 6: Semantic Matching

**10. Skills Extraction**
```python
for job in jobs:
    skills = job.get('skills', [])
```
- Extract skills from each job
- Example: `["Java", "Microservices", "Cloud"]`

**11. Skills Validation**
```python
if isinstance(skills, str):
    skills = [skills]  # Convert string to list
elif not isinstance(skills, list):
    skills = []  # Handle invalid format
```
- Ensures skills is always a list
- Prevents ChromaDB query errors

**12. Semantic Search**
```python
links = portfolio.query_links(skills)
```

**ChromaDB Process**:
1. **Embedding Generation**:
   - Skills: `["Java", "Microservices", "Cloud"]`
   - ChromaDB creates embedding vector: `[0.234, -0.123, ...]`

2. **Similarity Search**:
   - Compares with all portfolio embeddings
   - Calculates cosine similarity scores
   - Example matches:
     - "Java, Spring Boot, Oracle" → 0.89 similarity
     - "Kotlin, Android, Firebase" → 0.45 similarity

3. **Return Top Matches**:
   - Get top 2 results (`n_results=2`)
   - Extract metadata (links)

**Result**:
```python
[
    {"links": "https://example.com/java-portfolio"},
    {"links": "https://example.com/kotlin-backend-portfolio"}
]
```

---

### Phase 7: Email Generation

**13. Email Writing Call**
```python
email = llm.write_mail(job, links)
```

**Prompt Template**:
```
### JOB DESCRIPTION:
{
    "role": "Software Engineering Manager",
    "experience": "8+ years",
    "skills": ["Team Leadership", "Java", "Microservices", "Cloud"],
    "description": "Lead a team of engineers..."
}

### INSTRUCTION:
You are Abhijeet Kushwaha, TPR at HBTU Kanpur.
Write an invitation email for on-campus MCA recruitment.
Highlight HBTU MCA student capabilities.
Include these portfolio links: [...]
Format properly.

Contact: 240231001@hbtu.ac.in, +91-7408909350
```

**LLM Output** (example):
```
Subject: Invitation for On-Campus Recruitment Drive - HBTU Kanpur MCA

Dear Hiring Manager,

I hope this email finds you well! 🌟

I am Abhijeet Kushwaha, Training & Placement Representative at HBTU Kanpur.
I'm reaching out to invite your esteemed organization for an on-campus 
recruitment drive for our MCA students.

We noticed your requirement for a Software Engineering Manager with 
expertise in Java, Microservices, and Cloud technologies. Our MCA 
students have strong capabilities in these areas...

Portfolio References:
🔗 https://example.com/java-portfolio
🔗 https://example.com/kotlin-backend-portfolio

Looking forward to your positive response! 😊

Best regards,
Abhijeet Kushwaha
Placement Coordinator, HBTU Kanpur
📧 240231001@hbtu.ac.in
📱 +91-7408909350
```

---

### Phase 8: Output Display

**14. Display in Streamlit**
```python
st.code(email, language='markdown')
```
- Renders email in code block
- Markdown formatting preserved
- User can copy entire email
- Multiple emails displayed if multiple jobs found

**15. Error Handling**
```python
except Exception as e:
    st.error(f"An Error Occurred: {e}")
```
- Catches any runtime errors
- Displays user-friendly error message
- Continues execution for other jobs

---

## ⚙️ Setup and Installation

### Prerequisites
- Python 3.9 - 3.12 (Python 3.13+ not fully supported by all dependencies)
- Git
- Groq API Key

### Installation Steps

**1. Clone Repository**
```bash
git clone https://github.com/cw-HX/Campus-Invitation-Mail-Generator.git
cd Campus-Invitation-Mail-Generator
```

**2. Create Virtual Environment**
```bash
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure API Key**
Create `app/.env` file:
```env
GROQ_API_KEY='your-api-key-here'
```

Get your API key from: https://console.groq.com/keys

**5. Run Application**
```bash
streamlit run app/main.py
```

**6. Access Application**
Open browser: `http://localhost:8501`

---

## 🔧 Configuration

### Environment Variables

**File**: `app/.env`

```env
GROQ_API_KEY='your-groq-api-key'
```

### Portfolio Configuration

**File**: `app/resource/my_portfolio.csv`

**Format**:
```csv
Techstack,Links
"Python, Django, REST API",https://github.com/student1/django-project
"React, Node.js, MongoDB",https://github.com/student2/mern-stack
```

**Customization**:
- Add more portfolio entries
- Update links to actual student projects
- Include relevant tech stacks for your institution

### LLM Configuration

**File**: `app/chains.py`

```python
self.llm = ChatGroq(
    temperature=0,      # 0 = deterministic, 1 = creative
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"  # Can change model
)
```

**Available Models**:
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

---

## ⚠️ Error Handling

### Common Errors and Solutions

**1. "Non-empty lists are required for ['documents']"**

**Cause**: Empty skills list passed to ChromaDB

**Solution**: Already fixed in code
```python
def query_links(self, skills):
    if not skills or len(skills) == 0:
        return []  # Return empty list instead of querying
    return self.collection.query(...)
```

**2. "Context too big. Unable to parse jobs."**

**Cause**: Career page content exceeds LLM context window

**Solution**: 
- Improve text cleaning
- Use larger context model
- Split content into chunks

**3. "Failed to load web content"**

**Cause**: Invalid URL or website blocking scraping

**Solution**:
- Verify URL is correct
- Check website robots.txt
- Consider using Selenium for dynamic pages

**4. "API Key not found"**

**Cause**: Missing or incorrect `.env` file

**Solution**:
- Ensure `app/.env` exists
- Verify `GROQ_API_KEY` is set correctly
- Check for typos in variable name

---

## 🎓 Key Concepts Explained

### 1. **Vector Embeddings**
- Convert text to numerical vectors
- Similar meanings = similar vectors
- Enable semantic search (not just keyword matching)

### 2. **Semantic Search**
- Understands context and meaning
- "Python developer" matches "Django expert"
- Better than exact string matching

### 3. **LLM Prompting**
- Clear instructions = better results
- Structured output (JSON) = easier parsing
- Few-shot examples improve accuracy

### 4. **Persistent Vector Store**
- ChromaDB saves embeddings to disk
- No need to recreate on each run
- Faster subsequent queries

### 5. **LangChain Chains**
- Pipe (`|`) operator chains components
- `Prompt | LLM | Parser`
- Modular and reusable

---

## 🚀 Future Enhancements

### Potential Improvements

1. **Email Customization**
   - Allow custom templates
   - Different formats for different companies

2. **Batch Processing**
   - Process multiple URLs at once
   - Generate comparison reports

3. **Analytics Dashboard**
   - Track email success rates
   - Company response analytics

4. **Multi-language Support**
   - Generate emails in multiple languages
   - Regional customization

5. **Integration**
   - Direct email sending (SMTP)
   - CRM integration
   - Calendar scheduling

6. **Enhanced Portfolio**
   - Student skill ratings
   - Project descriptions
   - GitHub integration

---

## 📞 Support and Contact

**Placement Coordinator**: Abhijeet Kushwaha  
**Email**: 240231001@hbtu.ac.in  
**Phone**: +91-7004489697  
**Institution**: HBTU Kanpur

---

## 📄 License

This project is created for educational and placement purposes at HBTU Kanpur.

---

**Last Updated**: January 8, 2026  
**Version**: 1.0.0  
**Author**: Campus Placement Team, HBTU Kanpur
