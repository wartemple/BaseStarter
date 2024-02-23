from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            status_code = renderer_context['response'].status_code
        except Exception:
            status_code = 400
        if status_code == 204:
            return super().render(data, accepted_media_type, renderer_context)
        response = {
          'status': 'success',
          'code': status_code,
          'data': data,
          'message': ''
        }
        if not str(status_code).startswith('2'):
            response['status'] = 'error'
            response['data'] = None
            try:
                response['message'] = data['detail']
            except KeyError:
                response['data'] = data
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
