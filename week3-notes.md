## What is Prompt Engineering?
Prompt engineering is the process of crafting and refining prompts to improve the performance of generative AI models. It involves providing specific inputs to tools like ChatGPT, Midjourney, or Gemini, guiding the AI to deliver more accurate and contextually relevant outputs.

## Why Prompt Engineering is Important?
Prompt engineering is important because:
- It bridges the gap between vague, general queries and specific, actionable results.
- It helps mitigate errors, such as generating irrelevant content or incorrect responses.
- It ensures that the AI can handle tasks like creative writing, image generation, or even code development with minimal post-processing needed.

## What is a Prompt?
A prompt is the input or instruction given to an AI model to generate a response. Prompts can be simple (a question) or complex (detailed instructions with context, tone, style, and format specifications). The quality of the AI's response depends directly on how clear, detailed, and structured the prompt is.

Generative AI models, like ChatGPT, can sometimes produce incorrect or misleading outputs. This often happens when a prompt is too vague, lacks necessary details, or doesn't provide clear instructions.

The process of editing and refining the prompt is what we call prompt engineering. Adding specificity and guidance to the prompt improves the output and guides the model apply logical reasoning more effectively.

## Why Did the Updated Prompt Work?
Generative AI models are trained to predict text based on patterns instead of deep reasoning or factual accuracy. By prompting the model to explicitly think through its steps and break down the problem, we reduce the chance of mistakes and make the task easier for the model to handle.

## Difference between simple prompt and refined prompt
### Text
Simple prompt : Write a marketing summary for a new AI tool that helps companies automate tasks.
Refined prompt : Write a 100-word marketing summary for an AI tool called TaskBot, which automates repetitive tasks for small businesses in industries like retail and healthcare. Highlight efficiency and cost savings.

### Image Generation
Simple prompt : A cat sitting on a chair.
Refined prompt : Generate an image of a tabby cat sitting on a wooden chair in a cozy, sunlit room, with soft shadows and warm lighting.

### Code Generation
Simple prompt : Write a NodeJS function to multiply two numbers.
Refined prompt : Write a NodeJS function that multiplies two integers and returns the result. Include error handling for cases where inputs are not integers.

Prompt engineering is an iterative process. The perfect prompt rarely happens on the first try, so it's essential to practice refining your inputs to get the best possible output from generative AI models. As we've seen, adding specificity, providing context, and guiding the model with detailed instructions can significantly improve its responses.

## FAISS vs. Chroma

FAISS is primarily a high-performance library for searching through vectors. It's especially useful when you want direct control over the indexing and similarity-search machinery.
Chroma is more database-like and is convenient for building applications where you want to store documents, embeddings, and metadata together.