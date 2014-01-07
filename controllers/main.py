import base64
from _xmlplus.FtCore import _
import simplejson
import openerp.addons.web.controllers.main as main
from openerp.addons.web_pdf_preview.controllers.main import content_disposition
import openerp.addons.web.http as openerpweb


class Binary2(main.Binary):
    _cp_path = "/web/binary"

    @openerpweb.httprequest
    def saveas_ajax(self, req, data, token):
        jdata = simplejson.loads(data)
        model = jdata['model']
        field = jdata['field']
        data = jdata['data']
        id = jdata.get('id', None)
        filename_field = jdata.get('filename_field', None)
        context = jdata.get('context', {})

        Model = req.session.model(model)
        fields = [field]
        if filename_field:
            fields.append(filename_field)
        if data:
            res = { field: data }
            # FIX  one2many attachment download bug
            if filename_field:
                filename_name = Model.read([int(id)], [filename_field], context)
                res[filename_field] = filename_name and filename_name[0] and filename_name[0][filename_field] or ''
        elif id:
            res = Model.read([int(id)], fields, context)[0]
        else:
            res = Model.default_get(fields, context)
        filecontent = base64.b64decode(res.get(field, ''))
        if not filecontent:
            raise ValueError(_("No content found for field '%s' on '%s:%s'") %
                (field, model, id))
        else:
            filename = '%s_%s' % (model.replace('.', '_'), id)
            if filename_field:
                filename = res.get(filename_field, '') or filename
            return req.make_response(filecontent,
                headers=[('Content-Type', 'application/octet-stream'),
                        ('Content-Disposition', content_disposition(filename, req))],
                cookies={'fileToken': token})