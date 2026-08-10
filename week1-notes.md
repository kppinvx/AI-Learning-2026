## What is AI Engineer

AI Engineer who develops intelligent applications that utilise data and algorithms to address real world problems.

- Instead of coding they recognise patterns
- Make predictions or understand language
- Working on data collection, cleaning and prepare
- Test and improve algorithms and ensure accuracy

## LLMs providers comparisons

- ChatGPT - Provide more details, fast output
- Gemini - Comparatively less details than ChatGPT and out speed almost same.

## Temperature of the LLM

- For Customer Support Recommended Temperature 0.1–0.3
- For Internal Knowledge/Research Recommended Temperature	0.3–0.5
- For Creative Writing / Idealisation Recommended Temperature	0.6–0.8

## Example of temperature change for the same prompt

Write an essay on current Indian stock market trends and about its future in next 5 years in 100 words.

### Output With Temperature = 0.1
The Indian stock market is currently witnessing a robust bullish trend, driven by strong domestic liquidity, surging retail participation through Systematic Investment Plans (SIPs), and resilient macroeconomic fundamentals. Key sectors like infrastructure, renewable energy, and technology are driving this momentum, pushing benchmarks to historic highs. Over the next five years, the market’s outlook remains exceptionally bright. Powered by India’s rapid GDP growth, rising middle-class wealth, and strategic policy initiatives like "Make in India," the stock market is poised for massive expansion. Despite short-term global volatility, strong corporate earnings and consistent foreign capital inflows will solidify India's position as a premier global investment destination.

### Output With Temperature = 0.9
The Indian stock market is witnessing unprecedented growth, driven by robust macroeconomic fundamentals, rising retail participation through SIPs, and strong domestic institutional inflows. Key sectors like banking, technology, renewable energy, and infrastructure are powering this bullish momentum, making the market resilient to global headwinds. In the next five years, the Indian stock market is projected to reach new heights. Growth will be catalysed by government manufacturing incentives, digital transformation, urbanisation, and a young demographic. While geopolitical risks and inflation may cause temporary volatility, India’s long-term economic story firmly establishes it as one of the world's most lucrative investment destinations.

### Output With Temperature = 1.8
The Indian stock market is experiencing a historic bull run, driven by strong macroeconomic fundamentals, unprecedented retail participation through Systematic Investment Plans (SIPs), and robust domestic institutional support. Key indices like Nifty and Sensex regularly hit record highs, led by banking, infrastructure, and technology sectors. Over the next five years, the market outlook remains exceptionally bullish. As India progresses toward a $5 trillion economy, government initiatives like Production Linked Incentive (PLI) schemes, expanding manufacturing, and the green energy transition will drive sustainable corporate earnings growth. Despite short-term global volatility and geopolitical risks, the Indian equity market promises to remain a compelling destination for long-term wealth creation.

## What is Langchain?

Langchain consist of a large set of the pre-built components. Memory, Tools, RAG, VectorDB, MCP etc are configures using Langchain's pre-built libraries.

## LLMs vs Agent

- LLMs are static brains that answers questions based on what it learned during training.
- Agent has full autonomy with memory and tools to do whatever it thinks it needs to get the task done.
- LLM prompting optimises for clarity, structure and tone.
- Agent prompting optimises for decision making, tool selection, execution flows and constraints.
- LLMs excel at responding to prompts in a general context, but struggle in a specific domain they were never trained on. Prompts are queries people use to seek responses from an LLM. For example, an LLM can provide an answer to how much a computer costs by providing an estimate. However, it can't list the price of a specific computer model that your company sells.

## What does Agent do?

- Understand intent
- Store the company's Knowledge in Vector DB
- Retrieval of knowledge from Vector DB
- Search internal DB for data
- Generate an answer based on data
- Create chat history + memory

## Traditional software vs Agentic software

- Traditional Software uses if else conditions or sequences based on the code that determines how it's run.
- Whereas Agentic software it developed in components and provided to agent for it to decide how best to use its ability.
