def login(request):
       context = RequestContext(request)
       return render_to_response("templates/login.html", context)    


def all_members(request): <--
       return render(request, 'templates/members.html', 
{'members': Member.objects.all()})