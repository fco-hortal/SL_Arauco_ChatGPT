from qvd import qvd_reader
df = qvd_reader.read('Precio_venta.qvd')
print(df.head())