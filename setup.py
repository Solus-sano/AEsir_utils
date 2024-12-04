from setuptools import setup, find_packages

setup(
    name="AEsir_utils",  
    version="0.1.0",      
    author="Solus-sano",   
    author_email="liangzhj56@mail2.sysu.edu.cn",  
    description="A brief description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_project",  # 替换为你的GitHub链接
    packages=find_packages(),  # 自动查找所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 替换为你的许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定支持的Python版本
    install_requires=[       # 可选，列出依赖
        # "numpy",  # 示例
    ],
    entry_points={
        "console_scripts": [
            "script1=your_project.script1:main",  # 替换为你的脚本入口
        ],
    },
)