import json
import os
from concurrent.futures import ThreadPoolExecutor

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
