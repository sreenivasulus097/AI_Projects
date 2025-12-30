# test_web_search.py
from web_search_tool import WebSearchTool

tool = WebSearchTool()

results = tool.search_profiles(
    "Elon Musk CEO Tesla LinkedIn profile"
)

print("\n--- RESULTS ---")
if not results:
    print("❌ No results found")
else:
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")

from extractor import ProfileExtractor

extractor = ProfileExtractor()

structured_profiles = []

for result in results:
    profile = extractor.extract(result)
    if profile["confidence"] >= 0.4:
        structured_profiles.append(profile)

print("\n📊 Extracted Profiles:")
for p in structured_profiles:
    print(p)
