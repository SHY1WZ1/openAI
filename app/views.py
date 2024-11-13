from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import openai
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TextFileForm, PromptForm
from .models import TextFile

openai.api_key = settings.OPENAI_API_KEY


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
    file_obj = TextFile.objects.get(id=file_id)
    file_path = file_obj.file.path
    # Read the contents of the uploaded file
    with open(file_path, "r") as file:
        file_content = file.read()

    if request.method == "POST":
        prompt_form = PromptForm(request.POST)
        if prompt_form.is_valid():
            prompt = prompt_form.cleaned_data["prompt"]

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
                temperature=0.7,  # Controls creativity
                top_p=1.0,  # Controls diversity of responses
            )

            # Extract the modified text from the response
            modified_text = response.choices[0].message.content

            # Save the modified content back into the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modified_text)

            # Save the modified text to a new model or file
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
