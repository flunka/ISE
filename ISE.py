import requests
import json


def send_request(uri, payload=None, method='GET'):
  uri = '/ers/config/{}'.format(uri)

  base_url = "https://ise26.abc.inc:9060"
  url = base_url + uri
  cert = "./ise26-abc-inc.pem"
  headers = {
      'Content-Type': 'application/json',
      'Accept-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic Zmx1bmthOlF3ZXJ0eTEyMw=='
  }
  json_payload = json.dumps(payload) if payload else None
  response = requests.request(method, url, headers=headers, data=json_payload, verify=cert)
  return response


def get_group_id_by_name(name):
  uri = 'identitygroup'
  method = "GET"
  response = send_request(uri=uri, method=method)

  parsed = json.loads(response.text.encode('utf8'))
  resources = parsed['SearchResult']['resources']
  group_id = None
  for resuorce in resources:
    if resuorce['name'] == name:
      group_id = resuorce['id']
  if group_id:
    return group_id
  else:
    raise Exception("Not found identity group {}".format(name))
  # print(json.dumps(parsed, indent=4, sort_keys=True))


def create_user(username, password, group):
  uri = 'internaluser'
  method = "POST"
  try:
    group_id = get_group_id_by_name(group)
  except Exception as e:
    print(e)
    return -1

  payload = {
      "InternalUser": {
          "name": username,
          "password": password,
          "changePassword": False,
          "identityGroups": group_id,
      }
  }
  response = send_request(uri, payload, method)
  if response.status_code == 201:
    print("User {} has been created.".format(username))
    user_id = response.headers['Location'].split('/')[-1]
    return user_id
  else:
    error = json.loads(response.text.encode('utf8'))
    print(error['ERSResponse']['messages'][0]['title'])


def delete_user(user_id):
  uri = 'internaluser/{}'.format(user_id)
  method = "DELETE"
  response = send_request(uri=uri, method=method)
  if response.status_code == 204:
    print("User {} has been deleted.".format(user_id))
  else:
    error = json.loads(response.text.encode('utf8'))
    print(error['ERSResponse']['messages'][0]['title'])


def main():
  user_id = create_user('thomas11', 'Test123', 'Employee')
  delete_user(user_id)


if __name__ == '__main__':
  main()
