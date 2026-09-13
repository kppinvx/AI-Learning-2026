// app.js
import { ChatMistralAI } from "@langchain/mistralai";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const llm = new ChatMistralAI({
  apiKey: process.env.MISTRAL_API_KEY,
  model: "mistral-large-latest",
  temperature: 0,
});

// Pre-built Calculator Tool
const calculatorTool = tool(
  async ({ a, b, operation }) => {
    switch (operation) {
      case "add":
        return String(a + b);
      case "subtract":
        return String(a - b);
      case "multiply":
        return String(a * b);
      case "divide":
        return String(a / b);
      default:
        return "Invalid operation";
    }
  },
  {
    name: "calculator",
    description: "Perform mathematical calculations",
    schema: z.object({
      a: z.number(),
      b: z.number(),
      operation: z.enum([
        "add",
        "subtract",
        "multiply",
        "divide",
      ]),
    }),
  }
);

// Custom Weather Tool (Open-Meteo - Free)
const weatherTool = tool(
  async ({ city }) => {
    const geoRes = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(
        city
      )}&count=1`
    );

    const geoData = await geoRes.json();

    if (!geoData.results?.length) {
      return `City not found: ${city}`;
    }

    const { latitude, longitude } = geoData.results[0];

    const weatherRes = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,weather_code`
    );

    const weatherData = await weatherRes.json();

    return JSON.stringify({
      city,
      temperature: weatherData.current.temperature_2m,
      weatherCode: weatherData.current.weather_code,
    });
  },
  {
    name: "get_weather",
    description: "Get current weather for a city",
    schema: z.object({
      city: z.string(),
    }),
  }
);

// Custom Stock Tool (Yahoo Finance Free API)
const stockTool = tool(
  async ({ symbol }) => {
    const res = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`
    );

    const data = await res.json();

    const price =
      data.chart.result?.[0]?.meta?.regularMarketPrice;

    return `${symbol} current price: ${price}`;
  },
  {
    name: "get_stock_price",
    description: "Get current stock price by stock symbol",
    schema: z.object({
      symbol: z.string(),
    }),
  }
);

const llmWithTools = llm.bindTools([
  calculatorTool,
  weatherTool,
  stockTool,
]);

const response = await llmWithTools.invoke(
  "What is the weather in Ahmedabad and current stock price of AAPL? Also calculate 25 * 4."
);

console.log(response);
console.log("Tool Calls:", response.tool_calls);
