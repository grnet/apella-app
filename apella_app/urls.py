from apimas.container import Container
import api_settings


controller = Container('api')

urlpatterns = [
    controller.create_api_views(api_settings.API_SCHEMA)
]
