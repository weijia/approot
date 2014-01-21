INSTALLED_APPS += (
    'pagination',
)

MIDDLEWARE_CLASSES += (
    #'libs.objsys.middleware.XsSharingMiddleware',
    'pagination.middleware.PaginationMiddleware',
)
