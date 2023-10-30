from django.shortcuts import render
from django.http import JsonResponse
import torch
from torchvision.transforms import transforms
from PIL import Image
from ultralytics import YOLO

from django.core.files.storage import default_storage
from django.http import HttpResponseNotFound

from django.shortcuts import get_object_or_404, redirect
from .models import Photo

# Ensure we're using the GPU, if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def predict_disease(request):
    if request.method == 'POST':
        plant_type = request.POST.get('plant_type')
        image_file = request.FILES.get('image_file')
        file_path = default_storage.save('photos/' + image_file.name, image_file)
        img = Image.open(image_file)
        # Map plant types to model files
        model_mapping = {
            'Corn': 'Corn_best.pt',
            'Grape': 'Grap_best.pt',
            'Paper': 'Paper_best.pt',
            'Peach': 'Peach_best.pt',
            'Apple':'Appel_best.pt',
            'Olive':'Olive_best.pt',
            'Cherry':'Cherry_best.pt',
            'Strawberry':'Strawberry_best.pt',
            'Tomato':'Tomato_best.pt',
            'Potato':'Potato_best.pt',
        }
        model_file = model_mapping.get(plant_type)

        if model_file is None:
            # Handle error: unknown plant type
            raise ValueError(f'Unknown plant type: {plant_type}')

        model = YOLO(f'predictor/models/{model_file}')
        
       

        with torch.no_grad():
            predictions = model(img)
            prediction = predictions[0].probs.data
           
            # Find the index of the maximum value

            max_index = torch.argmax(prediction)

            # Print the index
            print(max_index.item())
            # Accessing the names dictionary
            names_dict = predictions[0].names

            # Print the names dictionary
            print(names_dict)
            prediction = names_dict[max_index.item()]

        
        photo = Photo.objects.create(image=file_path, predicted_disease=prediction)
        photo.save()
        print(photo.id)
        print(photo.image)
        context = {'predicted_disease': prediction, 'image_url': photo.image,'photo':photo}
       

        return render(request, 'results.html', context)

    else:
        photos = Photo.objects.all()
        context = {'photos': photos}
        return render(request, 'upload.html',context)







def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    image_path = photo.image.path
    default_storage.delete(image_path)  # Delete the associated image file
    photo.delete()  # Delete the Photo object from the database
    return redirect('/photos/')  # Replace 'photo_list' with the URL name for displaying the list of uploaded photos


def photo_list(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'photo_list.html', context)