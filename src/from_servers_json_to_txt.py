import requests
import json

# read the JSON targeted by url and write to file fout.
def write_text(url,fout,url_only=False):
    
    out=open(fout,"w")

    # Send a GET request and check for errors
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if response code is not 2xx
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit(1)

    # Parse the JSON data
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        exit(1)

    for item in data.get("servers"):
        if url_only:
            out.write( "%s\n" % item["url"] )
        else:
            out.write( "%s, %s, %s, %s, %s\n" % ( item["url"], item["title"], item["id"], item["contact"], item["contactID"] ) )
    out.close()

# write the JSON from the legacy JSON file.  Note the JSON copy is the one humans should modify.
def write_json(url,fout):
    # Send a GET request and check for errors
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if response code is not 2xx
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit(1)
    
    servers=[]
    for item in response.text.splitlines():
        fields= item.split(',')
        server= {
            "url":fields[0].strip(),
            "title":fields[1].strip(),
            "id": fields[2].strip(), 
            "contact": fields[3].strip(),
            "contactID": fields[4].strip() }
        servers.append(server)
    
    ff = { "servers": servers }
    out= open(fout,"w")
    out.write( json.dumps(ff,indent=4) )
    out.write("\n")
    out.close()
        


#write_json("https://raw.githubusercontent.com/hapi-server/servers/20240208-all-json/dev.txt","dev.json")
write_text("https://raw.githubusercontent.com/hapi-server/servers/20240208-all-json/all.json","all_.txt")
write_text("https://raw.githubusercontent.com/hapi-server/servers/20240208-all-json/all.json","all.txt",url_only=True)
write_text("https://raw.githubusercontent.com/hapi-server/servers/20240208-all-json/dev.json","dev.txt")
