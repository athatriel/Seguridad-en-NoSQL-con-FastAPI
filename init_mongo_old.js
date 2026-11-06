db = db.getSiblingDB('tienda');

db.usuarios.insertMany([
  {
    username: "alberto",
    password: "1234"
  },
  {
    username: "villar",
    password: "abcd"
  }
]);

db.pedidos.insertMany([
  {
    producto: "Portatil Lenovo",
    cantidad: 1
  },
  {
    producto: "Monitor Dell",
    cantidad: 2
  }
]);
