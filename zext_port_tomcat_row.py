#!/usr/bin/python3
# vim: set ai ts=2 sw=2 expandtab :

import  json, sys

# Função que faz a atribuicao dos parametros passado caso haja falha os programa é encerrado.
def atribuicao():
    if sys.argv[1] != ' ':
        global ports
        ports = sys.argv[1].split(",")
    else:
        retorno = {}
        tomcat = []
        data = {}
        data["{#ERRO}"] = "Sem dados"
        tomcat.append(data)
        retorno["data"] = tomcat
        print(json.dumps(retorno, indent=4))
        sys.exit()

def main():
    atribuicao()
    retorno = {}
    tomcats = []
    for port in ports:
        dado = {}
        dado["{#PORT}"] = int(port)
        dado["{#ERRO}"] = "Coleta OK"
        tomcats.append(dado)  
    retorno["data"] = tomcats
    print(json.dumps(retorno, indent=4))

if __name__ == '__main__': main()
