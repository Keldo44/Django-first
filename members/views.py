from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
def horari_tarde(request):
  myClasses = Class.objects.all().select_related('subject').order_by('weekday')


  template = loader.get_template('horari_table.html')
  days = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE']
  hour_range = range(15, 19)
  context = {
    'myClasses': myClasses,
    'days': days,
    'hour_range': hour_range,
    'start_hour_limit': hour_range[0],
    'neg_start_hour_limit': -hour_range[0],
  }

  return HttpResponse(template.render(context, request))


def horari(request):
  return render(request, 'horari.html')

def get_txt_file(request):
  template = loader.get_template('file_upload.html')
  return HttpResponse(template.render({}, request))


def upload_file(request):
  if request.method == 'POST':
    # Obtenemos el archivo del diccionario FILES
    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
      messages.error(request, "No se seleccionó ningún archivo.")
      return redirect('file')

    # Validar extensión manualmente (segunda capa de seguridad)
    if not uploaded_file.name.endswith('.txt'):
      messages.error(request, "Error: Solo se permiten archivos .txt")
      return redirect('upload_file')

    # Guardar en el modelo File
    new_file = File(
      filename=uploaded_file.name,
      file=uploaded_file
    )
    new_file.save()

    messages.success(request, f"¡{uploaded_file.name} subido con éxito!")
    return redirect('file_detail', file_id=new_file.id)

  return redirect('/files/list')

def files_list(request):
  files = File.objects.all()
  context = {
    'files': files,
  }
  template = loader.get_template('file_list.html')
  return HttpResponse(template.render(context, request))


def file_detail(request, file_id):
  clases = Class.objects.all()
  for clase in clases:
    clase.delete()
  archivo = get_object_or_404(File, id=file_id)

  # Use 'r' for reading text
  with archivo.file.open('r') as f:
    for line_number, line in enumerate(f, 1):
      # .strip() removes trailing newlines and whitespace
      clean_line = line.strip()

      #<MON,THU,..>_<Block:1,2>_<subjectId:1,2,3...>
      class_parts = clean_line.split('_')

      create_class(class_parts)
  return redirect('/horari/tarde')


def create_class(class_parts):
  days_map = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4}
  hours_map = {'1': ['15:00:00','17:00:00'], '2': ['17:00:00','19:00:00']}
  day_num = days_map.get(class_parts[0])
  hours = hours_map.get(class_parts[1])
  subject_obj = Subject.objects.get(id=int(class_parts[2]))


  new_class = Class(
      subject = subject_obj,
      start_hour = hours[0],
      end_hour = hours[1],
      weekday = day_num
  )

  new_class.save()