from rest_framework.routers import SimpleRouter, Route, DynamicRoute


class BaseRouter(SimpleRouter):
    routes = [
        # 导入接口
        Route(
            url=r'^{prefix}/upload/$',
            mapping={ 'post': 'upload' },
            name='{basename}-upload',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # 导出接口
        Route(
            url=r'^{prefix}/export/$',
            mapping={ 'get': 'export' },
            name='{basename}-export',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                # 批量刪除接口
                'delete': 'bulk_delete' 
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
