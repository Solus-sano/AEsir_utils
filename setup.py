from setuptools import setup, find_packages

setup(
    name="AEsir_utils",  
    version="0.1.0",      
    author="Solus-sano",   
    author_email="liangzhj56@mail2.sysu.edu.cn",  
    description="A brief description of your project",
    long_description="useful tools",
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
    # entry_points={
    #     "console_scripts": [
    #         "script1=your_project.script1:main",  
    #     ],
    # },
)