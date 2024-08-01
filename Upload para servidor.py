import requests

url = "https://sigahomol.meioambiente.go.gov.br/api/v2/uploads/upload"
files= [
    ('cpg_file',('teste.cpg',open('C:/Users/raissa.alves/Desktop/teste/teste.cpg','rb'),'application/octet-stream')),
    ('dbf_file',('teste.dbf',open('C:/Users/raissa.alves/Desktop/teste/teste.dbf','rb'),'application/octet-stream')),
    ('prj_file',('teste.prj',open('C:/Users/raissa.alves/Desktop/teste/teste.prj','rb'),'application/octet-stream')),
    ('shp_file',('teste.shp',open('C:/Users/raissa.alves/Desktop/teste/teste.shp','rb'),'application/octet-stream')),
    ('shx_file',('teste.shx',open('C:/Users/raissa.alves/Desktop/teste/teste.shx','rb'),'application/octet-stream'))
]
headers = {
  'Authorization': 'Basic td4g9GVCrrqEUo6akcyuz9s4aQZN9m'
}

response = requests.request("POST", url, headers=headers, files=files)
print(response.text)
