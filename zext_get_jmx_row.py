#!/usr/bin/python3
# vim: set ai ts=2 sw=2 expandtab :
# Author: Nour Sharabash <nour.sharabash@gmail.com>

import argparse, sys, json, re, socket, os

java_gateway_host = '10.2.2.3'
java_gateway_port = 10052
jmx_user = ''
jmx_pass = ''

def atribuicao():
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        global jmx_key
        global jmx_server
        global jmx_ports
        jmx_key = sys.argv[1]
        jmx_server = sys.argv[2]
        jmx_ports = sys.argv[3].split(",")
    else:
        tomcat = []
        data = {}
        data["port"] = "Sem dados"
        data["name"] = "Sem nome"
        data["object"] = "Sem objeto"
        tomcat.append(data)
        print(json.dumps(tomcat, indent=4))
        exit()

def parse_to_json(data_string):
  json_parse = json.loads(data_string)
  remove_data = json_parse["data"]
  remove_list = remove_data[0]
  final_data = remove_list["value"]
  return(json.loads(final_data))

def get_dados(jmx_port):
  query = { 'request': 'java gateway jmx',
             'conn': jmx_server, 'port': jmx_port,
             'keys': [jmx_key] }
  if jmx_user and jmx_pass:
    query['username'] = args.jmx_user
    query['password'] = args.jmx_pass
  # Original jmx_endpoint
  query['jmx_endpoint'] = 'service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi' % (jmx_server, jmx_port)
  # query['jmx_endpoint'] = 'service:jmx:remote://%s:%s/' % (conn, port)

  query_str = json.dumps(query)
  query_len = len(query_str)
  query_len_hex = '%.16x' % query_len
  query_len_bin = re.sub(r'^(..)(..)(..)(..)(..)(..)(..)(..)', '\\x\\8\\x\\7\\x\\6\\x\\5\\x\\4\\x\\3\\x\\2\\x\\1', query_len_hex)
  query_bin = "ZBXD\\x01%s" % (query_len_bin)
  query_bin = query_bin.encode('latin-1').decode('unicode_escape')
  query_bin += query_str

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((java_gateway_host,java_gateway_port))
    s.send(bytes(query_bin, 'latin-1'))
    size = 1024
    data = s.recv(size)
    full = ''
    started = False
    while len(data):
      data = str(data, 'latin-1')
      if not started:
        if '{' in data:
          data = data[data.index('{'):]
          started = True
        else:
          data = ''
      if started:
        full += data
      data = s.recv(size)
    
    full = parse_to_json(full)
    return(full)

def main():
    atribuicao()
    tomcats = []
    for port in jmx_ports:
        try:  
            dados_tomcat = get_dados(port)
            for dado in dados_tomcat:
                dado["port"] = port
                dado.pop("description")
                dado.pop("type")
                if "context" in jmx_key:
                  contexts = dado["object"].split(",")
                  for context in contexts:
                      if "context" in context:
                          dado["object"] = context.lstrip("context=")
                else:
                  dado.pop("object")
                tomcats.append(dado)
        except:
            dado = {}
            dado["port"] = port
            dado["name"] = "Unknown"
            dado["object"] = "Sem conexao JMX"
            tomcats.append(dado)

    print(json.dumps(tomcats, indent=4))

if __name__ == '__main__': main()
