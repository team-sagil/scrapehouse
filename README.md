# scrapehouse

- To scrape today's map with the parameters set in oslo-apt/oslo-apt.json
    python3 scrapehouse.py oslo-apt/oslo-apt
    
- outputs are
  - oslo-apt/oslo-apt.map.[date].json
  - oslo-apt/oslo-apt.ad.[ad_id].poi.json
  - oslo-apt/oslo-apt.ad.[ad_id].parsed.json
  
where "add_id"s are reference in the first output. "poi.json" is
downloaded directly, but doesnt' contain all the info. "parsed.json"
however is what's scraped from the html.
