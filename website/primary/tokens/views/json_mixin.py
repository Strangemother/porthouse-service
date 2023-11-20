
from django.http import JsonResponse


class JSONResponseContent(object):
    json_accept_type = 'application/json'
    json_header_key = 'x-content-type'
    json_method_name = 'as_json_data'

    def render_to_json_response(self, context, **response_kwargs):
        method = getattr(self, self.json_method_name)
        response_data = method(context, **response_kwargs)
        return self.as_json_response(response_data)

    def as_json_response(self, response_data):
        return JsonResponse(response_data)

    def is_ajax_request(self):
        value = self.json_accept_type
        key = self.json_header_key

        return self.request.headers.get(key) == value

    def as_json_data(self, context, **response_kwargs):
        # print('as_json_data')
        return {
            'content': 'json'
        }


class ApplicationHeaderJSONSwitchMixin(JSONResponseContent):

    def render_to_response(self, context, **response_kwargs):
        if self.is_ajax_request():
            return self.render_to_json_response(context, **response_kwargs)

        return super().render_to_response(context, **response_kwargs)
