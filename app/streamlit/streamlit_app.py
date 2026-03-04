import streamlit as st
import json
from snowflake.snowpark.context import get_active_session
from image_loader import render_image, get_image_base64

st.set_page_config(
    page_title="Bigdata.com",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .card {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 0.5rem;
    }
    .card-meta {
        font-size: 0.85rem;
        color: #6c757d;
    }
    .card-text {
        font-size: 0.95rem;
        color: #495057;
        line-height: 1.6;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 500;
        border-radius: 4px;
        margin-right: 0.5rem;
    }
    .badge-primary {
        background: #e7f1ff;
        color: #0d6efd;
    }
    .badge-success {
        background: #d1e7dd;
        color: #198754;
    }
    .result-count {
        font-size: 0.9rem;
        color: #198754;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .answer-box {
        background: #f8f9fa;
        border-left: 4px solid #0d6efd;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .trace-item {
        padding: 0.75rem;
        border-bottom: 1px solid #e9ecef;
        font-size: 0.9rem;
    }
    .stButton > button {
        background: #0d6efd;
        color: white !important;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background: #0b5ed7;
        color: white !important;
    }
    .stButton > button:focus,
    .stButton > button:active,
    .stButton > button:focus:not(:active) {
        background: #0b5ed7;
        color: white !important;
        box-shadow: none;
    }
    div[data-testid="stTabs"] button {
        font-weight: 500;
    }
    .mcp-section {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    .mcp-section h1, .mcp-section h2, .mcp-section h3, .mcp-section h4, .mcp-section h5 {
        color: #212529;
        margin-top: 0.5rem;
    }
    .mcp-content {
        max-height: 600px;
        overflow-y: auto;
    }
    .mcp-content table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        background: white;
        border-radius: 6px;
        overflow: hidden;
    }
    .mcp-content th {
        background: #0d6efd;
        color: white;
        padding: 0.75rem;
        text-align: left;
        font-weight: 600;
    }
    .mcp-content td {
        padding: 0.75rem;
        border-bottom: 1px solid #dee2e6;
    }
    .mcp-content tr:hover {
        background: #f1f3f4;
    }
    .mcp-content p {
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .mcp-content strong {
        color: #212529;
    }
    .mcp-content code {
        background: #e9ecef;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

def render_mcp_content(text_content):
    """Render MCP markdown content with nice formatting for tearsheet"""
    import re
    sections = re.split(r'\n(?=#{1,3}\s)', text_content)
    
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split('\n')
        header = lines[0] if lines else ""
        content = '\n'.join(lines[1:]) if len(lines) > 1 else ""
        
        if header.startswith('# '):
            st.markdown(f"### {header[2:]}")
        elif header.startswith('## '):
            with st.expander(header[3:], expanded=True):
                st.markdown(content, unsafe_allow_html=True)
        elif header.startswith('### '):
            with st.expander(header[4:], expanded=True):
                st.markdown(content, unsafe_allow_html=True)
        else:
            st.markdown(section, unsafe_allow_html=True)

def render_companies(data):
    """Render Find Companies results"""
    if isinstance(data, list):
        companies = data
    else:
        companies = data if isinstance(data, list) else []
    
    st.markdown(f'<div class="result-count">{len(companies)} companies found</div>', unsafe_allow_html=True)
    
    for company in companies:
        company_type = company.get('type', 'Unknown')
        badge_class = 'badge-success' if company_type == 'Public' else 'badge-primary'
        listings = company.get('listing_values') or []
        listings_str = ', '.join(listings[:3]) if listings else 'N/A'
        
        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div>
                    <div class="card-title">{company.get('name', 'Unknown')}</div>
                    <div class="card-meta">
                        <span class="badge {badge_class}">{company_type}</span>
                        <span class="badge badge-primary">{company.get('sector', 'N/A')}</span>
                        <span>{company.get('country', '')}</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <code style="background:#e7f1ff;padding:0.3rem 0.6rem;border-radius:4px;font-weight:600;color:#0d6efd;">{company.get('id', '')}</code>
                </div>
            </div>
            <div class="card-text" style="margin-top:0.75rem;">{company.get('description', 'No description available') or 'No description available'}</div>
            <div class="card-meta" style="margin-top:0.5rem;">
                <strong>Listings:</strong> {listings_str}
                {f' | <a href="{company.get("webpage")}" target="_blank">{company.get("webpage")}</a>' if company.get('webpage') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_search_results(data):
    """Render MCP Search results"""
    results = data.get('results', []) if isinstance(data, dict) else []
    
    st.markdown(f'<div class="result-count">{len(results)} results found</div>', unsafe_allow_html=True)
    
    for result in results:
        source_name = result.get('source', {}).get('name', 'Unknown')
        timestamp = result.get('timestamp', '')[:10] if result.get('timestamp') else ''
        headline = result.get('headline', 'No headline')
        url = result.get('url', '')
        chunks = result.get('chunks', [])
        
        st.markdown(f"""
        <div class="card">
            <div class="card-title">
                {'<a href="' + url + '" target="_blank" style="color:#212529;text-decoration:none;">' + headline + '</a>' if url else headline}
            </div>
            <div class="card-meta">
                <span class="badge badge-primary">{source_name}</span>
                <span>{timestamp}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for chunk in chunks[:2]:
            relevance = chunk.get('relevance', 0)
            text = chunk.get('text', '')
            col_rel, col_text = st.columns([1, 9])
            with col_rel:
                st.markdown(f'<span class="badge badge-success">{relevance:.0%}</span>', unsafe_allow_html=True)
            with col_text:
                st.markdown(f'<div class="card-text">{text[:500]}{"..." if len(text) > 500 else ""}</div>', unsafe_allow_html=True)
        
        st.markdown("---")

logo_b64 = get_image_base64("logo.png")
st.markdown(f'''<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
<img src="{logo_b64}" height="50">
</div>''', unsafe_allow_html=True)

session = get_active_session()

tab1, tab2, tab3, tab4 = st.tabs(["API Tools", "MCP Tools", "External Agent Setup API", "External Agent Setup MCP"])

with tab1:
    st.markdown("#### API Tools")
    st.markdown("Search documents and get AI-powered analysis from financial data.", unsafe_allow_html=True)
    
    api_tool = st.selectbox("Select Tool", ["Document Search", "Research Agent"], key="api_tool")
    
    if api_tool == "Document Search":
        search_query = st.text_input("Query", value="Apple earnings Q4 2024", label_visibility="collapsed", placeholder="Enter your search query...", key="search_query")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            search_mode = st.selectbox("Mode", ["smart", "fast"], label_visibility="collapsed")
        with col2:
            max_chunks = st.select_slider("Results", options=[5, 10, 20, 30, 50], value=10, label_visibility="collapsed")
        with col3:
            search_clicked = st.button("Search", key="search", use_container_width=True)
        
        if search_clicked:
            with st.spinner("Searching..."):
                try:
                    result = session.call("tools.bigdata_search", search_query, search_mode, max_chunks)
                    data = json.loads(result)
                    
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        results = data.get("results", [])
                        st.markdown(f'<div class="result-count">{len(results)} documents found</div>', unsafe_allow_html=True)
                        
                        for doc in results[:10]:
                            source_name = doc.get('source', {}).get('name', 'Unknown')
                            timestamp = doc.get('timestamp', '')[:10] if doc.get('timestamp') else ''
                            headline = doc.get('headline', 'No headline')
                            
                            with st.container():
                                st.markdown(f"""
                                <div class="card">
                                    <div class="card-title">{headline}</div>
                                    <div class="card-meta">
                                        <span class="badge badge-primary">{source_name}</span>
                                        <span>{timestamp}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                for chunk in doc.get("chunks", [])[:2]:
                                    relevance = chunk.get('relevance', 0)
                                    text = chunk.get("text", "")
                                    col_rel, col_text = st.columns([1, 9])
                                    with col_rel:
                                        st.markdown(f'<span class="badge badge-success">{relevance:.0%}</span>', unsafe_allow_html=True)
                                    with col_text:
                                        st.markdown(f'<div class="card-text">{text[:500]}{"..." if len(text) > 500 else ""}</div>', unsafe_allow_html=True)
                                
                                st.markdown("---")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif api_tool == "Research Agent":
        message = st.text_area(
            "Question",
            value="What are the latest earnings results for Microsoft?",
            height=100,
            label_visibility="collapsed",
            placeholder="Enter your research question..."
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            research_effort = st.radio("Depth", ["lite", "standard"], horizontal=True, label_visibility="collapsed")
        with col2:
            research_clicked = st.button("Analyze", key="research", use_container_width=True)
        
        if research_clicked:
            with st.spinner("Analyzing... this may take a moment"):
                try:
                    result = session.call("tools.bigdata_research_agent", message, research_effort)
                    data = json.loads(result)
                    
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        if data.get("answer"):
                            st.markdown("#### Analysis")
                            st.markdown(data["answer"])
                        
                        if data.get("trace"):
                            with st.expander("View research trace"):
                                for step in data["trace"]:
                                    if step["type"] == "thinking":
                                        st.info(f"**Thinking:** {step['content']}")
                                    elif step["type"] == "action":
                                        st.success(f"**Action:** {step['tool']}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("#### MCP Tools")
    st.markdown("Access Bigdata.com tools via Model Context Protocol.", unsafe_allow_html=True)
    
    mcp_tool = st.selectbox("Select Tool", [
        "Find Companies",
        "Company Tearsheet",
        "Search"
    ])
    
    if mcp_tool == "Find Companies":
        query = st.text_input("Search Query", value="Apple", placeholder="Company name, ticker, ISIN, SEDOL, CUSIP, or URL", key="mcp_query")
        if st.button("Find", key="mcp_find"):
            with st.spinner("Searching..."):
                try:
                    result = session.call("tools.mcp_find_companies", query)
                    data = json.loads(result)
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        content = data.get("content", [])
                        if content and len(content) > 0:
                            text_content = content[0].get("text", "")
                            try:
                                companies_data = json.loads(text_content)
                                render_companies(companies_data)
                            except:
                                st.markdown(text_content)
                        else:
                            st.json(data)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif mcp_tool == "Company Tearsheet":
        col1, col2 = st.columns(2)
        with col1:
            rp_entity_id = st.text_input("Entity ID", value="4A6F00", placeholder="6-char RavenPack ID (e.g., 4A6F00)", key="mcp_entity_id")
        with col2:
            company_type = st.selectbox("Company Type", ["Public", "Private"], key="mcp_company_type")
        interval = st.selectbox("Interval", ["quarter", "annual"], key="mcp_interval") if company_type == "Public" else "quarter"
        if st.button("Get Tearsheet", key="mcp_tearsheet"):
            with st.spinner("Fetching tearsheet..."):
                try:
                    result = session.call("tools.mcp_company_tearsheet", rp_entity_id, company_type, interval)
                    data = json.loads(result)
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        content = data.get("content", [])
                        if content and len(content) > 0:
                            text_content = content[0].get("text", "")
                            render_mcp_content(text_content)
                        else:
                            st.json(data)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif mcp_tool == "Search":
        mcp_search_text = st.text_input("Search Text", value="Apple earnings", key="mcp_search_text")
        mcp_max_chunks = st.select_slider("Max Results", options=[5, 10, 20, 30], value=10, key="mcp_chunks")
        if st.button("Search", key="mcp_search_btn"):
            with st.spinner("Searching..."):
                try:
                    result = session.call("tools.mcp_search", mcp_search_text, mcp_max_chunks)
                    data = json.loads(result)
                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        content = data.get("content", [])
                        if content and len(content) > 0:
                            text_content = content[0].get("text", "")
                            try:
                                search_data = json.loads(text_content)
                                render_search_results(search_data)
                            except:
                                st.markdown(text_content)
                        else:
                            st.json(data)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab3:
    st.markdown("#### Cortex Agent Setup")
    st.markdown("Generate a SQL script to create a Cortex Agent with Bigdata.com tools.", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        agent_db = st.text_input("Database", value="MY_DB")
    with col2:
        agent_schema = st.text_input("Schema", value="MY_SCHEMA")
    with col3:
        warehouse = st.text_input("Warehouse", value="DEMO_WH")
    
    agent_name = st.text_input("Agent name", value="FINANCIAL_ANALYST")
    
    app_name = session.sql("SELECT CURRENT_DATABASE()").collect()[0][0]
    
    script = f'''-- Cortex Agent with Bigdata.com Tools
-- Generated by {app_name}

CREATE OR REPLACE AGENT {agent_db}.{agent_schema}.{agent_name}
    FROM SPECIFICATION $$
{{
    "models": {{
        "orchestration": "auto"
    }},
    "orchestration": {{}},
    "tools": [
        {{
            "tool_spec": {{
                "type": "generic",
                "name": "BIGDATA_SEARCH",
                "description": "Search for financial insights across news, SEC filings, earnings transcripts, and research documents. Executes parameterized queries with configurable search modes and result chunking. Use for finding specific information, news events, or document discovery.",
                "input_schema": {{
                    "type": "object",
                    "properties": {{
                        "query": {{
                            "type": "string",
                            "description": "The financial info you are searching, and the period if relevant"
                        }},
                        "search_mode": {{
                            "type": "string",
                            "description": "fast (default): Single query with specified filters. smart: Analyzes query text to auto-define filters and runs multiple sub-queries for better coverage. Use smart for user questions without pre-processing."
                        }},
                        "max_chunks": {{
                            "type": "number",
                            "description": "The number of chunks to return, if unsure use 10"
                        }}
                    }},
                    "required": ["query", "search_mode", "max_chunks"]
                }}
            }}
        }},
        {{
            "tool_spec": {{
                "type": "generic",
                "name": "BIGDATA_RESEARCH",
                "description": "AI research agent for comprehensive financial analysis. Performs deep research on company financials, market trends, and investment insights. Returns detailed analysis with citations.",
                "input_schema": {{
                    "type": "object",
                    "properties": {{
                        "message": {{
                            "type": "string",
                            "description": "The user's message/question to send to the agent, everything related to company financials"
                        }},
                        "research_effort": {{
                            "type": "string",
                            "description": "Research effort level: 'lite' (default) for quick analysis, 'standard' for comprehensive research"
                        }}
                    }},
                    "required": ["message", "research_effort"]
                }}
            }}
        }}
    ],
    "tool_resources": {{
        "BIGDATA_SEARCH": {{
            "type": "procedure",
            "identifier": "{app_name}.TOOLS.BIGDATA_SEARCH",
            "name": "BIGDATA_SEARCH(VARCHAR, DEFAULT VARCHAR, DEFAULT NUMBER)",
            "execution_environment": {{
                "type": "warehouse",
                "warehouse": "{warehouse}",
                "query_timeout": 90
            }}
        }},
        "BIGDATA_RESEARCH": {{
            "type": "procedure",
            "identifier": "{app_name}.TOOLS.BIGDATA_RESEARCH_AGENT",
            "name": "BIGDATA_RESEARCH_AGENT(VARCHAR, DEFAULT VARCHAR)",
            "execution_environment": {{
                "type": "warehouse",
                "warehouse": "{warehouse}",
                "query_timeout": 180
            }}
        }}
    }}
}}
$$;
'''
    
    st.code(script, language="sql")

with tab4:
    st.markdown("#### Cortex Agent Setup (MCP)")
    st.markdown("Generate a SQL script to create a Cortex Agent with MCP tools.", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mcp_agent_db = st.text_input("Database", value="MY_DB", key="mcp_agent_db")
    with col2:
        mcp_agent_schema = st.text_input("Schema", value="MY_SCHEMA", key="mcp_agent_schema")
    with col3:
        mcp_warehouse = st.text_input("Warehouse", value="DEMO_WH", key="mcp_warehouse")
    
    mcp_agent_name = st.text_input("Agent name", value="FINANCIAL_ANALYST_MCP", key="mcp_agent_name")
    
    mcp_app_name = session.sql("SELECT CURRENT_DATABASE()").collect()[0][0]
    
    mcp_script = f'''-- Cortex Agent with Bigdata.com MCP Tools
-- Generated by {mcp_app_name}

CREATE OR REPLACE AGENT {mcp_agent_db}.{mcp_agent_schema}.{mcp_agent_name}
    FROM SPECIFICATION $$
{{
    "models": {{
        "orchestration": "auto"
    }},
    "orchestration": {{}},
    "tools": [
        {{
            "tool_spec": {{
                "type": "generic",
                "name": "MCP_SEARCH",
                "description": "Search for financial insights across news, SEC filings, earnings transcripts, and research documents using MCP protocol.",
                "input_schema": {{
                    "type": "object",
                    "properties": {{
                        "search_text": {{
                            "type": "string",
                            "description": "Natural-language search query for financial and business content"
                        }},
                        "max_chunks": {{
                            "type": "number",
                            "description": "Maximum number of chunks to retrieve. Default is 10."
                        }}
                    }},
                    "required": ["search_text"]
                }}
            }}
        }},
        {{
            "tool_spec": {{
                "type": "generic",
                "name": "MCP_FIND_COMPANIES",
                "description": "Identify a private or public company by name, ticker, ISIN, SEDOL, CUSIP, or webpage URL and retrieve its Knowledge Graph ID.",
                "input_schema": {{
                    "type": "object",
                    "properties": {{
                        "query": {{
                            "type": "string",
                            "description": "Partial or complete company name, webpage, ticker, ISIN, SEDOL, or CUSIP"
                        }}
                    }},
                    "required": ["query"]
                }}
            }}
        }},
        {{
            "tool_spec": {{
                "type": "generic",
                "name": "MCP_COMPANY_TEARSHEET",
                "description": "Get comprehensive financial data, market intelligence, and analyst coverage for both public and private companies.",
                "input_schema": {{
                    "type": "object",
                    "properties": {{
                        "rp_entity_id": {{
                            "type": "string",
                            "description": "6-character RavenPack entity ID from find_companies (e.g., 4A6F00 for Alphabet)"
                        }},
                        "company_type": {{
                            "type": "string",
                            "description": "Must be 'Public' or 'Private' - use the exact type field from find_companies response"
                        }},
                        "interval": {{
                            "type": "string",
                            "description": "For public companies only: 'quarter' (default) or 'annual' for financial statement periods"
                        }}
                    }},
                    "required": ["rp_entity_id", "company_type"]
                }}
            }}
        }}
    ],
    "tool_resources": {{
        "MCP_SEARCH": {{
            "type": "procedure",
            "identifier": "{mcp_app_name}.TOOLS.MCP_SEARCH",
            "name": "MCP_SEARCH(VARCHAR, DEFAULT NUMBER)",
            "execution_environment": {{
                "type": "warehouse",
                "warehouse": "{mcp_warehouse}",
                "query_timeout": 180
            }}
        }},
        "MCP_FIND_COMPANIES": {{
            "type": "procedure",
            "identifier": "{mcp_app_name}.TOOLS.MCP_FIND_COMPANIES",
            "name": "MCP_FIND_COMPANIES(VARCHAR)",
            "execution_environment": {{
                "type": "warehouse",
                "warehouse": "{mcp_warehouse}",
                "query_timeout": 180
            }}
        }},
        "MCP_COMPANY_TEARSHEET": {{
            "type": "procedure",
            "identifier": "{mcp_app_name}.TOOLS.MCP_COMPANY_TEARSHEET",
            "name": "MCP_COMPANY_TEARSHEET(VARCHAR, VARCHAR, DEFAULT VARCHAR)",
            "execution_environment": {{
                "type": "warehouse",
                "warehouse": "{mcp_warehouse}",
                "query_timeout": 180
            }}
        }}
    }}
}}
$$;
'''
    
    st.code(mcp_script, language="sql")
