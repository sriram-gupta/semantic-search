def getProductMapping():
    return {
  "mappings": {
    "properties": {
      "_timestamp": {
        "enabled": true
      },
      "complete_text_emb": {
        "type": "dense_vector",
        "dims": 384
        
      }
    }
  }
}