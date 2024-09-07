from pymongo import mongo_client
connection_string="mongodb+srv://ancientlearning71:1bp5hNR4YOam3gsL@firstcluster.bp2vi.mongodb.net/?retryWrites=true&w=majority&appName=firstcluster"
client=mongo_client(connection_string)
database= client['Farmer']
collection= database['Farmer Data']
documents=collection.find() 
for document in documents:
    print (document)
print("your record are here See!")