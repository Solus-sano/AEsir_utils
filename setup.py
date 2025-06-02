from setuptools import setup, find_packages

setup(
    name="AEsir_utils",  
    version="0.2.0",      
    author="Solus-sano",   
    author_email="liangzhj56@mail2.sysu.edu.cn",  
    description="some useful tools, for data visualization, detection tools, diffusion tools, llm prompts generation, etc.",
    long_description_content_type="text/markdown",
    url="https://github.com/Solus-sano/AEsir_utils",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
    install_requires=[  
                           
    ],
)