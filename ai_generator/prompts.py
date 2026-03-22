SEARCH_DATA_PROMPT = """
Generate a JSON array of 5 test cases for hotel search on Booking.com.
Each object must have exactly these three fields:
- "location": a real city name in India (e.g. Chennai, Mumbai, Delhi, Bangalore, Hyderabad)
- "expected_keyword": same as the city name, used to validate search results
- "description": a short one-line description of the test scenario

Rules:
- Use 5 different cities across India
- Return ONLY the raw JSON array
- Do NOT include any explanation, markdown, code fences, or extra text
- Start your response with [ and end with ]

Example of correct output:
[
  {
    "location": "Chennai",
    "expected_keyword": "Chennai",
    "description": "Search for hotels in Chennai and validate results are returned"
  },
  {
    "location": "Mumbai",
    "expected_keyword": "Mumbai",
    "description": "Search for hotels in Mumbai and verify property cards appear"
  }
]
"""