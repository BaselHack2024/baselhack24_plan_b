![Example](assets/header.png)

# El Manual - Taco 'Bout Easy Manuals 
[![](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white 'Jupyter')](http://jupyter.org)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
[![](https://img.shields.io/badge/Pydantic-E92063.svg?style=for-the-badge&logo=Pydantic&logoColor=white 'Pydantic')](https://docs.pydantic.dev/)
[![](https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white 'Pandas')](https://pandas.pydata.org)
[![](https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=NumPy&logoColor=white 'Numpy')](https://numpy.org)
[![](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white 'FastAPI')](https://fastapi.tiangolo.com)
![MUI](https://img.shields.io/badge/MUI-%230081CB.svg?style=for-the-badge&logo=mui&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

## Project Contributors

Part of the team was:

[Michael Beutler](https://github.com/michaelbeutler) <br>
[Basil Holinger](https://github.com/kinba3000) <br>
[Paul Gesser](https://github.com/paulgeser) <br>
[Raquel Lima](https://github.com/raquelima) <br>
[Thierry Grimm](https://github.com/thierrygrimm) <br>
[Nathanel Thomman](https://github.com/nathanaelthomann) <br>
[Micha Thomman](https://github.com/) <br>



## Project Description

elManual is an application that helps you to automatically create user guides for you based on a sequence of images, turning every step into a fiesta! With our AI, you can upload images, and in a flash, it’ll convert them into clear instructions, sprinkled with just the right amount of humor and zest.

The application emphasizes modular design, user-friendly interaction, and robust processing of images to produce step-by-step guidance. Designed with fun in mind, elManual ensures that your documentation is not only informative but also entertaining.

:star2: Highlights:

elManual App: Transform Images and PDFs into Savory, Shareable Instructions!

With elManual, you can upload up to 10 images or PDFs at once, and watch as AI crafts them into clear, delightful instructions. The chatbot refines your text, giving it just the right spice, so every detail is as irresistible as fresh salsa. Rapid image and PDF processing ensures that your content is ready in seconds, making documentation as smooth as guacamole.

Once uploaded, images and PDFs are instantly converted, with instructions formatted to [specify format X] for easy sharing. Whether you’re guiding others through tacos or tech, elManual serves up step-by-step guides that everyone can savor.

Our intuitive chatbot interface supports both new uploads and existing files, making it simple for everyone—from street food vendors to tech experts. The result? Instructions that are the true taco of the town!

Combining culinary creativity with the latest tech, elManual ensures your instructions are always as clear, engaging, and memorable as a great recipe.

## Getting started

### Requirements

Make sure all module requirements are met or install them with:

~~~
python -m pip install -r requirements.txt
~~~


Make sure the OpenAI API key is stored within `/code/api/.env` file and can be read from the programm. 


After the dependencies are installed, you can run the backend with the following command in the app directory:

~~~
uvicorn main:app --reload
~~~

## License

```
El Manual - Taco 'Bout Easy Manuals 

The MIT License (MIT)

Copyright (c) 2024 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software ("El Manual") and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

