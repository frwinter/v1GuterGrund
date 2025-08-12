from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse

class EmbedView(TemplateView):
    template_name = 'events/embed.html'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.GET.get('format') == 'js':
            content = render_to_string('events/embed.js', self.get_context_data())
            return HttpResponse(content, content_type='application/javascript')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter-Logik hier
        return context