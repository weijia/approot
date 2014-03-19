INSTALLED_APPS += (
    'pagination',
)

MIDDLEWARE_CLASSES += (
    #'objsys.middleware.XsSharingMiddleware',
    'pagination.middleware.PaginationMiddleware',
)
