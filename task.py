# -*- coding: utf-8 -*-
import sys, json

# Define Python version:
item = sys.version_info
python_version = int(item.major)

if python_version >= 3:
    import urllib.request
    # Request ==================================================================
    def request(url, method='GET', data=None):
        try:
            req = urllib.request.Request(url,
                headers={'Content-Type':'application/json;charset=UTF-8'},
                method=method)
            if data:
                data = json.dumps(data).encode('utf-8')
                req.add_header('Content-Length', len(data))
            response = urllib.request.urlopen(req, data)
            if method == 'DELETE': return response.status
            return json.loads(response.read().decode('utf-8', 'ignore'))
        except urllib.error.URLError as error:
            return None  # 404
else:
    import urllib2
    # Request ==================================================================
    def request(url, method='GET', data=None):
        try:
            req = urllib2.Request(url,
                json.dumps(data) if data else None, {'Content-Type': 'application/json'})
            req.get_method = lambda: method
            response = urllib2.urlopen(req)
            if method == 'DELETE': return 200
            return json.loads(response.read())
        except urllib2.HTTPError as error:
            return None  # 404

## Test Cases ------------------------------------------------------------------

id = '891'
pet = {
    "id": int(id),
    "category": { "id": 1, "name": "Hunting" },
    "name": "Jack",
    "photoUrls": [ "photo_01.jpg", "photo_02.jpg" ],
    "tags": [
        { "id": 1, "name": "cute" },
        { "id": 2, "name": "home" },
    ],
    "status": "active"
}

# step 1: POST request to create Pet
data = request('https://petstore.swagger.io/v2/pet/', 'POST', pet)

# step 2: Verify
assert type(data['id']) is int
assert (data['category']['id']) is 1
assert (data['category']['name'] == 'Hunting') is True
assert (data['name'] == 'Jack') is True
assert (len(data['photoUrls']) == 2) is True
assert (data['photoUrls'][0] == 'photo_01.jpg') is True
assert (data['photoUrls'][1] == 'photo_02.jpg') is True
assert (len(data['tags']) == 2) is True
assert (data['tags'][0]['id'] == 1) is True
assert (data['tags'][0]['name'] == 'cute') is True
assert (data['tags'][1]['id'] == 2) is True
assert (data['tags'][1]['name'] == 'home') is True
assert (data['status'] == 'active') is True

print('Pet [ ' + str(data['id']) + ' / ' + pet['name'] + ' ] was created.')

# step 3: Update pet's name:
data['name'] = 'Mike'
data = request('https://petstore.swagger.io/v2/pet/', 'POST', data)

# check new name is not Jack but Mike
assert (data['name'] == 'Jack') is False
assert (data['name'] == 'Mike') is True

print('Pet [ ' + str(data['id']) + ' / ' + data['name'] + ' ] was updated.')

# step 4: delete pet by ID
url = 'https://petstore.swagger.io/v2/pet/' + id
status = request(url, 'DELETE')

assert (status == 200) is True
print('Pet [ ' + str(data['id']) + ' / ' + data['name'] + ' ] was deleted.')

# step 5: check that pet was removed
url = 'https://petstore.swagger.io/v2/pet/' + id
result = request(url, 'GET')
assert (result == None) is True

print('All test cases pass successfully.')
