from qadrant_agent import upload_chunks, inspect_collection, search_qdrant

chunks=['duplicate test chunk 1','duplicate test chunk 2']
source='reindex_test.pdf'
print('Uploading first time')
upload_chunks(chunks, source_name=source)
print('Uploading second time')
upload_chunks(chunks, source_name=source)
print('Inspecting collection (first 10 points)')
inspect_collection()
print('Querying for "duplicate test"')
res = search_qdrant('duplicate test', top_k=5)
print('Search results count:', len(res))
print('Sample result:', res[:2])
