from odoo import http


class Main(http.Controller):

    @http.route('/my', auth='user', type='json')
    def track_order(self, **data):
        pass
