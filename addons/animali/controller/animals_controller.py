from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import datetime
import traceback


class AnimalsController(CustomerPortal):

    @http.route(
        ['/my/animals'],
        type='http',
        auth='user',
        website=True
    )
    def portal_my_animals(self, **kw):

        partner = request.env.user.partner_id

        animals = request.env['gestione.animals'].search([
            ('partner_id', '=', partner.id)
        ])

        values = {
            'animals': animals,
            'page_name': 'animals_list',
        }

        return request.render(
            'animali.portal_my_animals',
            values
        )


    @http.route(
        ['/my/animals/<int:animal_id>'],
        type='http',
        auth='user',
        website=True
    )
    def portal_my_animal_detail(self, animal_id, **kw):

        partner = request.env.user.partner_id

        animal = request.env['gestione.animals'].browse(animal_id)

        if not animal.exists() or animal.partner_id != partner:
            return request.not_found()

        values = {
            'animal': animal,
            'page_name': 'animal_detail',
        }

        return request.render(
            'animali.portal_animal_page',
            values
        )


    @http.route(
        ['/my/animals/<int:animal_id>/certificate'],
        type='http',
        auth='user',
        website=True
    )
    def portal_my_animal_certificate(self, animal_id, **kw):
        try:
            partner = request.env.user.partner_id

            animal = request.env['gestione.animals'].browse(animal_id)

            if not animal.exists() or animal.partner_id != partner:
                return request.not_found()

            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base_url') or 'http://localhost:8069'
            
            current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M')

            pdf_content, content_type = request.env[
                'ir.actions.report'
            ].sudo()._render_qweb_pdf(
                'animali.action_report_animal_certificate',
                [animal.id],
                data={
                    'base_url': base_url,
                    'current_datetime': current_datetime
                }
            )

            headers = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf_content)),
                (
                    'Content-Disposition',
                    'attachment; filename="certificato_%s.pdf"' % animal.name
                ),
            ]

            return request.make_response(
                pdf_content,
                headers=headers
            )
        except Exception as e:
            traceback.print_exc()
            raise e