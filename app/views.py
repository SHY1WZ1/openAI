from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import openai
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TextFileForm, PromptForm
from .models import TextFile

openai.api_key = ''

def upload_file(request):
    if request.method == "POST":
        form = TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("modify_file", file_id=form.instance.id)
    else:
        form = TextFileForm()

    return render(request, "upload_file.html", {"form": form})



def modify_file(request, file_id):
    # Retrieve the file object from the database
    file_obj = TextFile.objects.get(id=file_id)
    file_path = file_obj.file.path
    
    # Read the contents of the uploaded file
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    if request.method == "POST":
        prompt_form = PromptForm(request.POST)
        if prompt_form.is_valid():
            prompt = "Create an HTML article using the provided text. Each section should contain:\n\n" \
             "A <h2> tag for the title.\n\n" \
             "A <p> tag for the text content (right side of the section).\n\n" \
             "An <img> tag with the src attribute set to 'image_placeholder.jpg' (left side of the section). Add an alt attribute for each image with a detailed prompt that can be used to generate the image.\n\n" \
             "Include captions under each image using the appropriate HTML <figcaption> tag.\n\n" \
             "The result should include only the content inside the <body> and </body> tags, with no other HTML structure (such as <html>, <head>, etc.)."

            temperature = prompt_form.cleaned_data["temperature"]  # Get temperature from form
            top_p = prompt_form.cleaned_data["top_p"]  # Get top_p from form

            # Ensure the temperature and top_p are within acceptable ranges
            temperature = min(max(temperature, 0.0), 1.0)  # Ensure it's between 0 and 1
            top_p = min(max(top_p, 0.0), 1.0)  # Ensure it's between 0 and 1

            # Call OpenAI API with dynamic temperature and top_p
            response = openai.chat.completions.create(
                model="gpt-4o",  # High-intelligence flagship model for complex, multi-step tasks
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant.",
                    },  
                    {
                        "role": "user",
                        "content": f"Modify the following text based on this prompt: {prompt}\n\nText:\n{file_content}",
                    },
                ],
                max_tokens=1000,  # Limit the length of the response
                temperature=temperature,  # Controls creativity
                top_p=top_p,  # Controls diversity of responses
            )

            # Extract the modified text from the response
            modified_text = response.choices[0].message.content

            # Save the modified content back into the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modified_text)

            # Redirect to the download page after modification
            return redirect("download_file", file_id=file_obj.id)

    else:
        prompt_form = PromptForm()

    return render(
        request,
        "modify_file.html",
        {"file_content": file_content, "form": prompt_form, "file_id": file_id},
    )




def download_file(request, file_id):
    file_obj = TextFile.objects.get(id=file_id)
    file_path = file_obj.file.path

    # Create a file response for the user to download the modified file
    with open(file_path, "r") as file:
        modified_text = file.read()

    response = HttpResponse(modified_text, content_type="text/plain")
    response["Content-Disposition"] = (
        f'attachment; filename="modified_{file_obj.file.name}"'
    )

    return response
