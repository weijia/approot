def retrieve_param(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    return data