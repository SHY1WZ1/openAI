from django.shortcuts import render, redirect
from django.http import HttpResponse
import openai
from django.conf import settings
from .forms import TextFileForm, PromptForm
from .models import TextFile

# Set up OpenAI API key strictly/from settings
openai.api_key = 'your_api_key'

# View to upload a file
def upload_file(request):
    if request.method == "POST":
        form = TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the file modification page with the file ID
            return redirect("modify_file", file_id=form.instance.id)
    else:
        form = TextFileForm()

    return render(request, "upload_file.html", {"form": form})


# View to modify the uploaded file content
def modify_file(request, file_id):
    # Retrieve the file object from the database using the file ID
    file_obj = TextFile.objects.get(id=file_id)
    file_path = file_obj.file.path

    # Read the file content
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    if request.method == "POST":
        # Process the prompt form submission
        prompt_form = PromptForm(request.POST)
        if prompt_form.is_valid():
            # Define the prompt for OpenAI to modify the text
            prompt = (
                "Create an HTML article using the provided text. Each section should contain:\n\n"
                "A <h2> tag for the title.\n\n"
                "A <p> tag for the text content (right side of the section).\n\n"
                "An <img> tag with the src attribute set to 'image_placeholder.jpg' (left side of the section). "
                "Add an alt attribute for each image with a detailed prompt that can be used to generate the image.\n\n"
                "Include captions under each image using the appropriate HTML <figcaption> tag.\n\n"
                "The result should include only the content inside the <body> and </body> tags"
            )

            # Get values for temperature and top_p from the form
            temperature = prompt_form.cleaned_data["temperature"]
            top_p = prompt_form.cleaned_data["top_p"]

            # Ensure the values are within the valid range of 0 to 1
            temperature = min(max(temperature, 0.0), 1.0)
            top_p = min(max(top_p, 0.0), 1.0)

            # Call OpenAI API to modify the file content based on the provided prompt and parameters
            try:
                response = openai.chat.completions.create(
                    model="gpt-4",  # Specify the model to use
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Modify the following text based on this prompt: {prompt}\n\nText:\n{file_content}"}
                    ],
                    max_tokens=2000,  # Limit the response length
                    temperature=temperature,
                    top_p=top_p,
                )
            except openai.error.OpenAIError as e:
                # Handle any errors from the OpenAI API and provide feedback to the user
                return render(request, "modify_file.html", {"error": "An error occurred with OpenAI. Please try again."})

            # Extract the modified text from the OpenAI API response
            modified_text = response.choices[0].message.content

            # Save the modified content back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modified_text)

            # Redirect to the download page after the file has been modified
            return redirect("download_file", file_id=file_obj.id)
    else:
        prompt_form = PromptForm()

    # Render the file modification page with the original content and form
    return render(
        request,
        "modify_file.html",
        {"file_content": file_content, "form": prompt_form, "file_id": file_id},
    )


# View to download the modified file
def download_file(request, file_id):
    # Retrieve the file object from the database
    file_obj = TextFile.objects.get(id=file_id)
    file_path = file_obj.file.path

    # Read the modified content from the file
    with open(file_path, "r", encoding="utf-8") as file:
        modified_text = file.read()

    # Create an HTTP response to download the modified file
    response = HttpResponse(modified_text, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="modified_{file_obj.file.name}"'

    return response
