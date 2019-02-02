{
  "graphiteHost": "graphite-server",
  "graphitePort": 2003,
  "port": 8125,
  "flushInterval": 30000,
  "deleteGauges": true,
  "servers": [
    { server: "./servers/udp", address: "0.0.0.0", port: 8125 }
  ]
}

