import json
import os
import requests
from langchain.tools import tool

class SearchTools:
    @tool("Search the internet")
    def search_internet(self, query):
        """
        Search the internet for the given query and return a formatted string of the top results.

        Args:
            query (str): The search query.

        Returns:
            str: A formatted string containing the top search results.
        """
        top_results_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ.get('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that. There could be an error with your Serper API key."
        
        results = response.json()['organic']
        result_strings = []
        for result in results[:top_results_to_return]:
            try:
                result_strings.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}",
                    "\n---"
                ]))
            except KeyError as e:
                continue
        
        return '\n'.join(result_strings)
