from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Canvas, Pixel
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@require_POST
@login_required
def place_pixel(request):
    data = json.loads(request.body)
    canvas_id = data.get('canvas_id')
    x = data.get('x')
    y = data.get('y')
    color = data.get('color')
    
    # Vérifier si l'utilisateur peut placer un pixel (cooldown)
    canvas = get_object_or_404(Canvas, id=canvas_id)
    last_pixel = Pixel.objects.filter(
        canvas=canvas,
        placed_by=request.user
    ).order_by('-placed_at').first()
    
    if last_pixel:
        time_since_last = timezone.now() - last_pixel.placed_at
        if time_since_last.total_seconds() < canvas.cooldown:
            return JsonResponse({
                'error': 'You must wait before placing another pixel'
            }, status=400)
    
    # Créer le nouveau pixel
    pixel = Pixel.objects.create(
        canvas=canvas,
        x=x,
        y=y,
        color=color,
        placed_by=request.user
    )
    
    return JsonResponse({'success': True})

class CanvasCreationForm(forms.ModelForm):
    class Meta:
        model = Canvas
        fields = ['title', 'width', 'height', 'cooldown']
        widgets = {
            'width': forms.NumberInput(attrs={'min': 1, 'max': 128}),
            'height': forms.NumberInput(attrs={'min': 1, 'max': 128}),
            'cooldown': forms.NumberInput(attrs={'min': 0})
        }

def get_pixels(request, pk):
    canvas = get_object_or_404(Canvas, pk=pk)
    pixels = Pixel.objects.filter(canvas=canvas).values('x', 'y', 'color')
    return JsonResponse(list(pixels), safe=False)

@login_required
def canvas_list(request):
    canvases = Canvas.objects.all().order_by('-created_at')
    return render(request, 'canvas/canvas_list.html', {'canvases': canvases})

@login_required
def canvas_create(request):
    if request.method == 'POST':
        form = CanvasCreationForm(request.POST)
        if form.is_valid():
            canvas = form.save(commit=False)
            canvas.creator = request.user
            canvas.save()
            messages.success(request, 'Your canvas has been created!')
            return redirect('canvas:canvas-detail', pk=canvas.pk)
    else:
        form = CanvasCreationForm()
    return render(request, 'canvas/canvas_form.html', {'form': form})

@login_required
def canvas_detail(request, pk):
    canvas = get_object_or_404(Canvas, pk=pk)
    context = {
        'canvas': canvas,
        'pixels': Pixel.objects.filter(canvas=canvas).select_related('placed_by')
    }
    return render(request, 'canvas/canvas_detail.html', context)

@login_required
def canvas_detail(request, pk):
    canvas = get_object_or_404(Canvas, pk=pk)
    context = {
        'canvas': canvas,
        'canvas_id': canvas.id,
        'canvas_cooldown': int(canvas.cooldown),  # Conversion explicite en entier
    }
    return render(request, 'canvas/canvas_detail.html', context)