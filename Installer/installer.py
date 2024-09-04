from os import system, getcwd

file_name = "main"


path = getcwd()
path = path.removesuffix("\\Installer")
path = f"{path}\\Source"

system(f"pyinstaller -w -F {path}\\{file_name}.py")
system(f"move {getcwd()}\\dist\\{file_name}.exe {getcwd()}")
system(f"del {file_name}.spec")
system(f"rd /s /q {getcwd()}\\build")
system(f"rd /s /q {getcwd()}\\dist")