import json
import os
from concurrent.futures import ThreadPoolExecutor
import openai
import dspy
import instructor
from format import ImageAnalyzer
from openai import OpenAI
from loguru import logger
from PIL import Image
from format import get_guide_class
from tqdm import tqdm
from dotenv import load_dotenv
import whisper

from pypdf import PdfReader

# API key from .env
load_dotenv()

data_folder_path = './data'
MAX_DIMENSION = 500


def run_process_analysis(process_id: str):
    logger.info(f"Running process {process_id}")
    openai_key = os.getenv("OLLAMA_API_KEY")
    client = instructor.from_openai(OpenAI(api_key=openai_key))
    # lm = dspy.OllamaLocal(model="llava:13b")
    # lm = dspy.OllamaLocal(model="llama3.1:13b"")
    # dspy.settings.configure(lm=lm)

    # Initialize the model
    # client = instructor.from_openai(
    #    OpenAI(base_url="http://localhost:11434/v1", api_key="ollama",  # required, but unused
    #           ), mode=instructor.Mode.JSON, )

    # Create process folder
    process_folder = f"{data_folder_path}/{process_id}"
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True)

    # Check if descriptions file already exists
    if not os.path.exists(f"{process_folder}/descriptions.json"):
        logger.info(f"Generating descriptions for process {process_id}")

        # Load and sort images by timestamp
        images = []
        file_names = sorted(
            [file_name for file_name in os.listdir(process_folder) if file_name.endswith((".jpg", ".jpeg", ".png"))],
            key=lambda x: os.path.getmtime(os.path.join(process_folder, x))
        )
        logger.info(f"Found {len(file_names)} images in {process_folder}")

        # Load images
        for file_name in file_names:
            file_path = os.path.join(process_folder, file_name)
            # resized_image_path = rescale_and_save_image(file_path)  # Rescale and save
            images.append(instructor.Image.from_path(file_path))  # Load resized image

        # Placeholder for descriptions
        image_descriptions = [""] * len(images)  # Pre-allocate based on the number of images

        # Using ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            # Submit tasks and keep track of futures with their respective indices
            futures = {executor.submit(process_image, client, image): idx for idx, image in enumerate(images)}

            # Process the futures in the order they were submitted
            for future in tqdm(futures, desc="Processing images"):
                idx = futures[future]  # Get the index from the dictionary
                description = future.result()  # Get the result from the future
                image_descriptions[idx] = description  # Store the result in the original order

        # Convert to dictionary format
        image_descriptions_dict = {f"image_{i + 1}": desc for i, desc in enumerate(image_descriptions)}
        logger.info(f"Processed image descriptions: {image_descriptions_dict}")

        # Convert the descriptions dictionary to JSON
        json_output = json.dumps(image_descriptions_dict, indent=4)

        # Save the descriptions to a JSON file
        with open(f"{process_folder}/descriptions.json", "w") as f:
            json.dump(image_descriptions_dict, f, indent=4)
    else:
        logger.info(f"Reusing descriptions for process {process_id}")
        with open(f"{process_folder}/descriptions.json", "r") as f:
            image_descriptions = json.load(f)
            json_output = json.dumps(image_descriptions, indent=4)
        # Print or save the JSON output
        logger.info(f"JSON output:\n{json_output}")

    #################################################################################################################
    # WHISPER AUDIO TRANSCRIPTION
    #################################################################################################################

    # Run the transcription
    transcription_text = ""
    # transcription_text = transcribe_first_mp3(data_folder_path)

    # prompt = f"""You are tasked with creating a user manual based on descriptions of a series of images.
    #     1. Identify the relevant object that is most likely described.
    #     2. Think about what the user is trying to achieve.
    #     3. Generate a single, clear instruction for each image, ensuring that it directly relates to the corresponding description, with a total of exactly {len(image_descriptions)} steps. Babies will die if the number of steps is smaller than the requested number of steps. Ensure that the image references are correct and in the original order.
    #
    #     Note:Don't invent steps that are not described so far. Give out json.
    #
    #     Here is some context from the audio transcription:\n{transcription_text}\n
    #     Here are the image descriptions:\n"""

    # Optional: Save the transcription to a file
    # if transcription_text:
    #     with open(os.path.join(data_folder_path, "transcription.txt"), "w") as f:
    #         f.write(transcription_text)
    #     print("Transcription saved to transcription.txt")
    #################################################################################################################

    #################################################################################################################
    # PDF File
    #################################################################################################################

    # Run the transcription
    # pdf_parsed = ...

    # Create the prompt for the user guide
    # prompt = f"""You are tasked with creating a user manual based on descriptions of a series of images.
    #     1. Identify the relevant object that is most likely described.
    #     2. Think about what the user is trying to achieve.
    #     3. Generate a single, clear instruction for each image, ensuring that it directly relates to the corresponding description, with a total of exactly {len(image_descriptions)} steps. Babies will die if the number of steps is smaller than the requested number of steps. Ensure that the image references are correct and in the original order.
    #
    #     Note: Don't invent steps that are not described so far. Give out json.
    #
    #     Here is some context from the PDF:\n{pdf_context_text[:2000]}\n
    #     Here is some context from the audio transcription:\n{audio_transcription_text}\n
    #     Here are the image descriptions:\n"""
    #################################################################################################################



    prompt = f"""You are tasked with creating a user manual based on descriptions of a series of images. 
    1. Identify the relevant object that is most likely described.
    2. Think about what the user is trying to achieve.
    3. Generate a single, clear instruction for each image, ensuring that it directly relates to the corresponding description, with a total of exactly {len(image_descriptions)} steps. Babies will die if the number of steps is smaller than the requested number of steps. Ensure that the image references are correct and in the original order. 
    
    Note:Don't invent steps that are not described so far. Give out json. 
    
    Here are the image descriptions:\n"""


    for idx, description in enumerate(image_descriptions):
        prompt += f"image_{idx + 1}: {description}\n"

    logger.info(f"Prompt:\n{prompt}")

    # Query the model separately for each image
    response = client.chat.completions.create(model="gpt-4o",
                                              response_model=get_guide_class(len(image_descriptions)),
                                              messages=[{"role": "user", "content": [prompt]}],
                                              max_retries=20, )

    r = response.model_dump()
    logger.info(f"Object: {json.dumps(r, indent=4)}")

    # Remove the goal attribute from the response
    r.pop("goal", None)

    with open(f"{process_folder}/result.json", "w") as f:
        json.dump(r, f, indent=4)


def process_image(client, image):
    # Query the model for the given image
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=ImageAnalyzer,
        messages=[{
            "role": "user",
            "content": [
                "Describe all visible objects in this image and what the user is doing. Don't mention things you don't see. Give back json containing a concise description.",
                image,
            ],
        }],
        max_retries=30,
    )
    return response.model_dump()["description"]


def transcribe_first_mp3(folder_path):
    # Initialize the Whisper model
    model = whisper.load_model("base")  # You can adjust model size based on available resources

    # Find the first MP3 file in the specified folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            mp3_path = os.path.join(folder_path, file_name)
            print(f"Found MP3 file: {mp3_path}")

            # Transcribe the audio file
            transcription_result = model.transcribe(mp3_path)
            transcription_text = transcription_result['text']
            print(f"Transcription:\n{transcription_text}")

            return transcription_text  # Returning in case you want to store or use it later

    print("No MP3 files found in the specified folder.")
    return None


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyPDF."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def create_user_guide(context_text):
    """Generates a user guide outline using context from a PDF."""
    prompt = f"""
    Based on the following reference text, create a structured user guide outline with key sections:

    Reference Text:
    {context_text[:2000]}  # Limit to the first 2000 characters to fit prompt length constraints

    Outline:
    - Provide an overview of the user guide structure.
    - Include main sections such as 'Getting Started', 'Features', 'Troubleshooting', and 'FAQs'.
    - For each section, list a few example points that a user guide would cover.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use a powerful model like "text-davinci-003" for detailed responses
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()
