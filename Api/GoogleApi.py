from googleapiclient.discovery import build  # Import the library
import json

api_key = "my-secret-api-key"
cse_id = "my-secret-custom-search-id "

with open("resources/settings.json", "r") as f:
    data = json.load(f)
    p = data["cplusplus-Api"]
    api_key = p["Api-key"]
    cse_id = p["cse-id"]

# Credits: https://towardsdatascience.com/current-google-search-packages-
# using-python-3-7-a-simple-tutorial-3606e459e0d4


def google_query(query, api_key, cse_id, **kwargs):
    query_service = build("customsearch", "v1", developerKey=api_key)
    query_results = (
        query_service.cse()
        .list(q=query, cx=cse_id, **kwargs)  # Query  # CSE ID
        .execute()
    )
    return query_results["items"]


my_results_list = []
my_results = google_query("C++ for loop", api_key, cse_id, num=1)
# print(my_results[0]["link"])
for result in my_results:
    my_results_list.append(result["link"])
    # print(result["link"])