from rest_framework.renderers import JSONRenderer

class AxfJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if type(data).__name__ in ["ReturnList", "ReturnDict", "OrderedDict"]:
            result = {
                "code": 200,
                "data": data,
                "msg": "OK"
            }
        elif type(data).__name__ == "dict":
            result = {
                "code": data.get("code", 200),
                "data": data.get("data"),
                "msg": data.get("msg", "OK")
            }
        else:
            print(data, type(data))
            raise Exception("未知的数据类型")
        return super().render(result, accepted_media_type, renderer_context)
