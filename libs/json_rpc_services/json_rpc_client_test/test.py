from jsonrpc.proxy import ServiceProxy

s = ServiceProxy('http://localhost:8110/json_rpc_services/json/')

s.json_rpc_services.hello('Sam')
