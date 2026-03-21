from google import genai

client = genai.Client(api_key="AIzaSyBTVwv0Eeo0xXgwUVBP2RbJQ6_9XthGQcg")

for m in client.models.list():
    print(m.name)