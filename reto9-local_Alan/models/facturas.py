from connection.conn import Connection

class Facturas:
    def __init__(self):
        self.model = Connection('facturas')

    def get_facturas(self, order):
        return self.model.get_all(order)

    def get_factura(self, id_object):
        return self.model.get_by_id(id_object)

    def search_factura(self, data):
        return self.model.get_columns(data)

    def insert_factura(self, factura):
        return self.model.insert(factura)

    def update_factura(self, id_object, data):
        return self.model.update(id_object, data)

    def delete_factura(self, id_object):
        return self.model.delete(id_object)
        
    def get_by_id_column(self, id_object,id_column):
        return self.model.get_by_id_column(id_object, id_column)
    
    def get_by_id_column_top(self, id_object):
        return self.model.get_by_id_column_top(id_object)