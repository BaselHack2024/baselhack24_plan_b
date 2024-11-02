import json
import os

import dspy
import instructor
from format import ImageAnalyzer
from openai import OpenAI
from loguru import logger
from PIL import Image
from format import get_guide_class
from tqdm import tqdm
from dotenv import load_dotenv

# API key from .env
load_dotenv()


data_folder_path = './data'
MAX_DIMENSION = 500


def run_process_analysis(process_id: str):
    logger.info(f"Running process {process_id}")
    openai_key = os.getenv("OLLAMA_API_KEY")
    client = instructor.from_openai(OpenAI(api_key=openai_key))
    #lm = dspy.OllamaLocal(model="llava:13b")
    # lm = dspy.OllamaLocal(model="llama3.1:13b"")
    # dspy.settings.configure(lm=lm)

    # Initialize the model
    #client = instructor.from_openai(
    #    OpenAI(base_url="http://localhost:11434/v1", api_key="ollama",  # required, but unused
    #           ), mode=instructor.Mode.JSON, )

    #  process folder
    process_folder = f"{data_folder_path}/{process_id}"
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True)

    if not os.path.exists(f"{process_folder}/descriptions.json"):
        logger.info(f"Generating descriptions for process {process_id}")
        # Load and sort images by filename
        images = []
        file_names = sorted(
            [file_name for file_name in os.listdir(process_folder) if file_name.endswith((".jpg", ".jpeg", ".png"))])
        logger.info(f"Found {len(file_names)} images in {process_folder}")

        for file_name in file_names:
            file_path = os.path.join(process_folder, file_name)
            # resized_image_path = rescale_and_save_image(file_path)  # Rescale and save
            images.append(instructor.Image.from_path(file_path))  # Load resized image

        # Placeholder for descriptions
        image_descriptions = {}

        # Query the model separately for each image with progress tracking
        for idx, image in enumerate(tqdm(images, desc="Processing images")):
            # noinspection PyTypeChecker
            response = client.chat.completions.create(model="gpt-4o", response_model=ImageAnalyzer, messages=[
                {"role": "user", "content": [
                    "Describe all visible objects in this image and what the user is doing. Don't mention things you don't see. Give back json containing a description.",
                    image, ], }], max_retries=30, )
            description = response.model_dump()["description"]
            image_descriptions[f"image_{idx + 1}"] = description

        # Convert the descriptions dictionary to JSON
        json_output = json.dumps(image_descriptions, indent=4)

        # Save the descriptions to a JSON file
        with open(f"{process_folder}/descriptions.json", "w") as f:
            f.write(json_output)
    else:
        logger.info(f"Reusing descriptions for process {process_id}")
        with open(f"{process_folder}/descriptions.json", "r") as f:
            image_descriptions = json.load(f)
            json_output = json.dumps(image_descriptions, indent=4)

    # Print or save the JSON output
    logger.info(f"JSON output:\n{json_output}")

    prompt = f"""1. Identify the relevant object that is most likely described.\n2. For each image generate an instruction as part of a step-by-step user manual/guide with exactly !!! {len(image_descriptions)} steps. Babies will die if the number of steps is smaller than the requested number of steps. Always reference the image descriptions. Give out json. 
    Here are the image descriptions:\n"""

    for image_id, description in image_descriptions.items():
        prompt += f"{image_id}: {description}\n"

    logger.info(f"Prompt:\n{prompt}")

    # Query the model separately for each image
    response = client.chat.completions.create(model="gpt-4o",
                                              response_model=get_guide_class(len(image_descriptions)),
                                              messages=[{"role": "user", "content": [prompt]}],
                                              max_retries=20, )

    r = response.model_dump()
    logger.info(f"Object: {r}")

    with open(f"{process_folder}/result.json", "w") as f:
        json.dump(r, f, indent=4)
