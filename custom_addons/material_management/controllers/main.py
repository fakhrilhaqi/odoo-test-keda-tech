import json
from odoo import http
from odoo.http import request

class MaterialManagement(http.Controller):

    # get all materials
    @http.route('/api/materials', type='json', auth='user', methods=['GET'])
    def get_materials(self,material_type=None, **kwargs):
        domain = []
        if material_type:
            domain.append(('type', '=', material_type))
        materials = request.env['material.material'].search(domain)
        data = [{
            'id': material.id,
            'code': material.code,
            'name': material.name,
            'type': material.type,
            'buy_price': material.buy_price,
            'supplier_id': material.supplier_id.id,
        } for material in materials]
        return {'status':200, 'data':data}

    #update material
    @http.route('/api/material/<int:material_id>',type='json',auth='user',methods=['PUT'])
    def update_material(self,material_id,**payload):
        material = request.env['material.material'].browse(material_id)
        if not material.exists():
            return {'status':404, 'message':'Material not found'}

        if 'buy_price' in payload and payload['buy_price'] < 100:
            return {'status':400, 'message':'Buy Price must be greater than 100.'}

        material.write(payload)
        return {'status':200, 'message':'Material updated successfully'}

    #delete material
    @http.route('/api/material/<int:material_id>',type='json',auth='user',methods=['DELETE'])
    def delete_material(self,material_id,**kwargs):
        material = request.env['material.material'].browse(material_id)
        if not material.exists():
            return {'status':404, 'message':'Material not found'}

        material.unlink()
        return {'status':200, 'message':'Material deleted successfully'}