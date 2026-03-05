# Bigdata.com Tools for Snowflake Cortex Agents

This Native App exposes Bigdata.com API and MCP tools as Snowflake stored procedures, enabling seamless integration with Snowflake Cortex Agents.

## Tools Available

> :warning: **While API was a first attempt to validate the pattern, MCP is far better and must be the defacto choice.**

### MCP Tools (Model Context Protocol) :star: Recommended

- `mcp_search` - Search for financial insights using MCP protocol
- `mcp_find_companies` - Identify companies by name, ticker, ISIN, SEDOL, CUSIP, or URL
- `mcp_company_tearsheet` - Get comprehensive financial data for public/private companies

### API Tools :warning: Legacy

- `bigdata_search` - Search documents across news, filings, transcripts, and research 
- `bigdata_research_agent` - AI research agent for comprehensive analysis and insights

## Prerequisites

1. A Bigdata.com API key from [Developer Platform](https://platform.bigdata.com/api-keys)

## Usage
 
### API Tools - Direct Calls

```sql
-- Search for financial news (smart mode auto-interprets query)
CALL bigdata_app.tools.bigdata_search('NVIDIA earnings Q4 2025', 'smart', 10);

-- Search with fast mode (direct query, no interpretation)
CALL bigdata_app.tools.bigdata_search('Microsoft Azure revenue growth', 'fast', 20);

-- Research agent for comprehensive analysis (standard effort)
CALL bigdata_app.tools.bigdata_research_agent(
    'What are the key takeaways from Apple latest earnings call?',
    'standard'
);

-- Quick research with lite effort (default)
CALL bigdata_app.tools.bigdata_research_agent(
    'Summarize Tesla stock performance this week',
    'lite'
);
```

### MCP Tools - Direct Calls

```sql
-- Search using MCP protocol
CALL bigdata_app.tools.mcp_search('Apple earnings Q4 2024', 10);

-- Find a company by name, ticker, or identifier
CALL bigdata_app.tools.mcp_find_companies('Apple');
CALL bigdata_app.tools.mcp_find_companies('AAPL');
CALL bigdata_app.tools.mcp_find_companies('US0378331005'); -- ISIN

-- Get company tearsheet (use entity ID from find_companies)
CALL bigdata_app.tools.mcp_company_tearsheet('4A6F00', 'Public', 'quarter');
CALL bigdata_app.tools.mcp_company_tearsheet('4A6F00', 'Public', 'annual');
```

### Integration with Cortex Agent

Use the **External Agent Setup** tabs in the Streamlit app to generate complete agent creation scripts:
- **External Agent Setup** - Cortex Agent with API tools (bigdata_search, bigdata_research_agent)
- **External Agent Setup MCP** - Cortex Agent with MCP tools (mcp_search, mcp_find_companies, mcp_company_tearsheet)

### Streamlit App

The app includes a built-in Streamlit UI with four tabs:

1. **API Tools** - Test Document Search and Research Agent
2. **MCP Tools** - Test Find Companies, Company Tearsheet, and Search
3. **External Agent Setup** - Generate SQL scripts for Cortex Agent with API tools
4. **External Agent Setup MCP** - Generate SQL scripts for Cortex Agent with MCP tools

## Support

- Bigdata.com API Documentation: https://docs.bigdata.com/
- Search API: https://docs.bigdata.com/api-reference/search/search-documents
- Research Agent: https://docs.bigdata.com/api-reference/research-agent/research-agent
- MCP Reference: https://docs.bigdata.com/mcp-reference/introduction
- MCP find_companies: https://docs.bigdata.com/mcp-reference/tools/find-companies
- MCP bigdata_search: https://docs.bigdata.com/mcp-reference/tools/bigdata-search
- MCP bigdata_company_tearsheet: https://docs.bigdata.com/mcp-reference/tools/bigdata-company-tearsheet
