# scrapehouse

- To scrape today's map with the parameters set in oslo/oslo.json
    python3 scrapehouse.py oslo/oslo
    
- outputs are
  - oslo/oslo.map.[date].json
  - oslo/oslo.ad.[ad_id].poi.json
  - oslo/oslo.ad.[ad_id].parsed.json
  
where "add_id"s are reference in the first output. "poi.json" is downloaded directly, but doesnt' contain all the info. "parsed.json" however is what's scraped from the html.
