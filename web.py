from kubernetes import client, config
from flask import Flask, render_template, request, redirect 
from flask_mysqldb import MySQL
import yaml
import json 
app = Flask(__name__)

# Configure db
db = yaml.load(open('db1.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
ret = v1.list_pod_for_all_namespaces(watch=False)
ret1 = v1.list_service_for_all_namespaces()

# Add 
uidOR = []
uid = []
nameOR = []
podcol = []
list_label = []
dict_label = {}
for i in ret.items: 
    uidOR.append(i.metadata.ownerReferences.uid)
    uid.append(i.metadata.uid)
    nameOR.append(i.metadata.ownerReferences.name)

    label_json = json.dumps(i.metadata.labels)
    list_label.append(label_json)

mysql = MySQL(app)

@app.route('/', methods=['POST']) 
def index(): 
    # Fetch form data
    userDetails = request.form
    cur = mysql.connection.cursor()
    for i in uid:
        i = userDetails['uid_metadata_pod']
        cur.execute("INSERT INTO pods(uid_metadata_pod) VALUES(%s)",(i))
        mysql.connection.commit()

    for i in uidOR:
        i = userDetails['uid_ownerreferences_metadata_pod']
        cur.execute("INSERT INTO pods(uid_ownerreferences_metadata_pod) VALUES(%s)",(i))
        mysql.connection.commit()
    for i in nameOR:
        i = userDetails['name_pod']
        cur.execute("INSERT INTO pods(name_pod) VALUES(%s)",(i))
        mysql.connection.commit()
    for i in list_label:
        i = userDetails['label']
        cur.execute("INSERT INTO pods(label) VALUES(%s)",(i))
        mysql.connection.commit()
    cur.close()
    return redirect('/pods')
    