# Bigdata.com Native App for Snowflake

A Snowflake Native App that exposes Bigdata.com API and MCP tools for integration with Snowflake Cortex Agents.

## Overview

This app provides two sets of tools:

> :warning: **While API was a first attempt to validate the pattern, MCP is far better and must be the defacto choice.**

### MCP Tools (Model Context Protocol) :star: Recommended

- **mcp_search** - Search for financial insights using MCP protocol
- **mcp_find_companies** - Identify companies by name, ticker, ISIN, SEDOL, CUSIP, or URL
- **mcp_company_tearsheet** - Get comprehensive financial data and analyst coverage for public/private companies

### API Tools :warning: Legacy

- **bigdata_search** - Search across news, SEC filings, earnings transcripts, and research documents
- **bigdata_research_agent** - AI-powered research agent for comprehensive financial analysis

## Project Structure

```
├── app/
│   ├── manifest.yml          # Native App manifest
│   ├── README.md             # In-app documentation
│   ├── sql/
│   │   ├── init.sql          # Main setup script
│   │   ├── callbacks.sql     # Reference callbacks
│   │   ├── apis.sql          # Internal API procedures
│   │   ├── mcp.sql           # Internal MCP procedures
│   │   └── proxies.sql       # Public proxy procedures
│   └── streamlit/
│       └── streamlit_app.py  # UI application
├── snowflake.yml             # Snow CLI configuration
├── Makefile                  # Build commands
└── README.md                 # This file
```

## Streamlit UI

The app includes a Streamlit interface with four tabs:

1. **API Tools** - Test Document Search and Research Agent
2. **MCP Tools** - Test Find Companies, Company Tearsheet, and Search
3. **External Agent Setup** - Generate SQL script for Cortex Agent with API tools
4. **External Agent Setup MCP** - Generate SQL script for Cortex Agent with MCP tools

## Prerequisites

1. [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index) installed
2. A Snowflake connection configured (e.g., `MainAnthonyAccount`)
3. A Bigdata.com API key from [Developer Platform](https://platform.bigdata.com/api-keys)

## Deployment

```bash
# Install/upgrade the app
snow app run --connection <CONNECTION_NAME>
```

Or use the Makefile:

```bash
make run
```

## Consumer Setup

After installation, the consumer must configure:

1. **Secret** containing the Bigdata.com API key
2. **External Access Integration** allowing connections to:
   - `api.bigdata.com`
   - `agents.bigdata.com`
   - `mcp.bigdata.com`

These are configured through the app's reference callbacks during setup.

## Documentation

- [Bigdata.com API Docs](https://docs.bigdata.com/)
- [Search API](https://docs.bigdata.com/api-reference/search/search-documents)
- [Research Agent](https://docs.bigdata.com/api-reference/research-agent/research-agent)
- [MCP Reference](https://docs.bigdata.com/mcp-reference/introduction)
- [MCP find_companies](https://docs.bigdata.com/mcp-reference/tools/find-companies)
- [MCP bigdata_search](https://docs.bigdata.com/mcp-reference/tools/bigdata-search)
- [MCP bigdata_company_tearsheet](https://docs.bigdata.com/mcp-reference/tools/bigdata-company-tearsheet)
