tools = [
    {
        "name": "wiki_search",
        "description": "Searches Wikipedia for the given query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for Wikipedia",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "random_joke",
        "description": "Generates a random joke",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "google_search",
        "description": "Search Google for the given query and return the results",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location"],
        },
    },
]
