# Django File Upload and Modification with OpenAI

This Django application allows users to upload text files, modify the content using OpenAI's GPT-4 API, and download the modified files.

## Features

- **File Upload**: Allows users to upload text files.
- **Text Modification**: Users can provide a prompt to modify the uploaded text using OpenAI's GPT-4 model.
- **File Download**: After modification, users can download the updated text file.

## Requirements

- Python 3.x
- Django 3.x or higher
- OpenAI API key

## Installation

### Prerequisites

1. Clone this repository:

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up OpenAI API Key**:
    - Obtain an API key from OpenAI [here](https://platform.openai.com/).
    - Add the OpenAI API key to your `settings.py` or use environment variables to securely store the key.
    
    Example for `settings.py`:

    ```python
    OPENAI_API_KEY = 'your-openai-api-key-here'
    ```

    *Important*: Never expose your API key in public repositories or commit it to version control.

4. **Database Setup**:
    Run the following command to create the necessary database tables:

    ```bash
    python manage.py migrate
    ```

5. **Run the Development Server**:
    Start the Django development server:

    ```bash
    python manage.py runserver
    ```

    Now, you can access the application at `http://127.0.0.1:8000`.

## Views and Workflow

### 1. Upload File - `upload_file(request)`

This view allows users to upload a text file. Once the file is uploaded, it will be stored in the database, and the user will be redirected to the file modification page.

- **URL**: `/upload/`
- **Methods**: 
  - `POST`: Upload a file.
  - `GET`: Display the file upload form.

### 2. Modify File - `modify_file(request, file_id)`

This view allows users to modify the uploaded text file's content by providing a prompt. The file content will be processed by OpenAI's GPT-4 model and modified accordingly. The user will then be redirected to the download page.

- **URL**: `/modify/<file_id>/`
- **Methods**: 
  - `POST`: Submit the prompt to modify the file content.
  - `GET`: Display the current file content and the modification form.

### 3. Download File - `download_file(request, file_id)`

This view allows users to download the modified text file. After the content is processed and saved, users can download the modified file.

- **URL**: `/download/<file_id>/`
- **Methods**: 
  - `GET`: Download the modified text file.

## Form Overview

### 1. TextFileForm
This form is used for uploading a text file. The file is then saved to the database.

### 2. PromptForm
This form is used to submit a prompt to OpenAI to modify the uploaded file content. The prompt guides the AI model on how to alter the text.

## Example Usage

1. **Upload a file**:
    - Go to `/upload/` and upload a text file.
    - Once the upload is successful, you will be redirected to `/modify/<file_id>/`.

2. **Modify the file**:
    - Enter a prompt for modifying the uploaded text (e.g., "Fix spelling and grammar errors").
    - The text will be processed by OpenAI's GPT-4 model and modified.
    - After the modification, you will be redirected to `/download/<file_id>/`.

3. **Download the modified file**:
    - You can now download the modified file by visiting `/download/<file_id>/`.

## Security Considerations

- **API Key**: Make sure to keep your OpenAI API key secure. Do not commit it to version control.
- **File Handling**: The application stores and processes text files. Ensure that uploaded files are properly validated to prevent malicious content from being processed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Troubleshooting

- **File Encoding**: Ensure the uploaded files are UTF-8 encoded to avoid issues when reading and modifying text.
- **API Key Errors**: If you encounter errors related to OpenAI, check if your API key is valid and properly configured in `settings.py`.
- **Model Errors**: If you encounter issues with the model (`gpt-4o`), try switching to `gpt-3.5-turbo` or a different available model in the OpenAI API.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

---

## Example Screenshots

Here you can add some screenshots of your project showing the upload form, modification interface, and the download page.

