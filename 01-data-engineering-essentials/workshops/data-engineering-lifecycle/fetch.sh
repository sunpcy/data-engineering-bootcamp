#!/bin/bash

API_KEY='$2a$10$lPIF1M5BGO1UUsfoVuBlPukdEtYbFdS/r0jXjNRG4RqN8txCWZw3K'
COLLECTION_ID=6742fc4de41b4d34e459b0ec

curl -XGET \
    -H "X-Master-key: $API_KEY" \
    "https://api.jsonbin.io/v3/c/$COLLECTION_ID/bins"
