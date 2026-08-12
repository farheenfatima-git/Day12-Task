#### **Multilingual Financial Query Engine — Architecture**



##### System Flow



User

↓

Website / Web Application / Mobile Application

↓

FastAPI Backend

↓

Input Validation

↓

AI Service

↓

Gemini API

↓

Structured Query

↓

Financial Data

↓

Python/Pandas Processing

↓

Validated Response

↓

Application



##### Components



**1. Application**

The user submits a financial question through the website, web application, or mobile application.



**2. FastAPI Backend**

Receives the request, validates the input, and communicates with the AI service.



**3. AI Service**

The `ai\_service.py` module sends the user's question to Gemini and converts it into a structured financial query.



**4. Gemini API**

Gemini understands natural-language questions in English, Urdu, Roman Urdu, and mixed-language queries.



**5. Financial Data**

The POC uses CSV files as sample financial data.



**6. Python/Pandas**

Processes the structured query against the financial data and generates the result.



**Error Handling**



The system handles:



\- Missing or invalid user ID

\- Empty or very short questions

\- Questions exceeding the allowed length

\- Invalid AI responses

\- Invalid JSON from the AI

\- Unsupported financial intents

\- Unknown customers

\- AI/API processing failures



**AI Service Requirements**



| Requirement | Implementation |

|---|---|

| External AI API | Gemini API |

| ML/AI Model | Gemini |

| Database | CSV files in POC |

| Prompt Engineering | Yes |

| Python Service | FastAPI |

| Background Processing | Not required for current POC |



**Data Privacy**



\- API keys are stored in `.env`.

\- `.env` is excluded from GitHub.

\- Only necessary financial information should be sent to the AI service.

\- A production system should avoid sending sensitive personal or financial information unnecessarily.

\- Production deployment should use authentication and encrypted communication.



**API Cost**



The feature depends on an external Gemini API.



Costs depend on:

\- Number of API requests

\- Input token usage

\- Output token usage

\- Selected Gemini model



For the POC, usage is limited to testing.



**Response Latency**



The response requires an external AI API call, so latency depends on:



\- Internet connection

\- Gemini API response time

\- Prompt size

\- Amount of financial data processed



For a production system, caching and optimized prompts could reduce unnecessary requests.



**Rate Limits**



The Gemini API may enforce request and usage limits.



A production implementation should include:



\- Request throttling

\- Retry handling

\- Usage monitoring

\- Appropriate API quotas



**Security**



Production deployment should include:



\- API authentication

\- HTTPS

\- Secure API key storage

\- Input validation

\- Rate limiting

\- Access control

\- Protection of financial data



**Hallucination / AI Error Handling**



Gemini is used only to interpret the user's question.



The AI does not directly generate the financial amount.



Instead:



User Question

↓

Gemini identifies intent and parameters

↓

Python retrieves actual financial data

↓

Python calculates the result

↓

API returns the result



This reduces the risk of the AI inventing financial figures.



**Future Integration**



The FastAPI endpoint can later be connected to:



*Web* *Application*

An AI query feature inside the financial dashboard.



*Mobile Application*

A multilingual financial assistant interface.



The mobile/web client would send:



```json

{

&#x20; "user\_id": 101,

&#x20; "question": "Ali par kitne paise baqi hain?"

}

