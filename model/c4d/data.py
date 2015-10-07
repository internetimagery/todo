import c4d

doc = c4d.documents.GetActiveDocument()

def save(doc, data):
    container = c4d.BaseContainer()
    container.SetString(1001, data)
    print doc.GetDataInstance().SetContainer(12345, container)

def load(doc):
    container = doc.GetDataInstance().GetContainer(12345)
    data = container.GetString(1001)

save(doc, "here is saved text")

print load(doc)
