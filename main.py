import typer
import os
from rich import print
from PIL import Image, ImageDraw, ImageFont  # Import PIL functions
import svgwrite  # Import svgwrite functions
from yaml import load  # Import yaml functions
from alive_progress import alive_bar  # Import alive_bar function

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class myTemplate:  # Your template
    def __init__(self, data, dir):  # Constructor
        self.name = data["name"]  # Saves Name input as a self object
        self.birthday = data["details"][
            "birthday"
        ]  # Saves Description input as a self object
        self.gender = data["details"]["gender"]
        self.owners = ",".join(data["owners"])  # Saves Owners input as a self object
        self.image = os.path.join(dir, data["picture"])  # Saves Image input as a self object
        if not os.path.exists(self.image):
            self.image = "" # If image does not exist, set it to empty string

        print("Pet's information: :dog:")  # Prints
        print(f"Name: {self.name}")  # Prints Name
        print(f"Birthday: {self.birthday}")  # Prints Description
        print(f"Gender: {self.gender}")  # Print
        print(f"Owners: {self.owners}")
        print("------------------")

    def draw(self):
        """
        Draw Function
        ------------------
        Draws the template
        """
        img = Image.open(r".\assets\template.png", "r").convert("RGB")  # Opens Template Image

        if self.gender == "male":
            print("Include [bold blue]male[/bold blue] icon. :blue_heart:")
            genderpict = Image.open(r".\assets\male.png")  # Opens
        elif self.gender == "female":
            print("Include [bold pink]female[/bold pink] icon. :heart:")
            genderpict = Image.open(r".\assets\female.png")  # Opens*
        else:
            print("Include [bold]unknown[/bold] icon. :broken_heart:")
            genderpict = Image.open(r".\assets\unknown.png")
        img.paste(genderpict, (900, 20), genderpict)  # Pastes image into template

        if self.image != "":
            print("Include pet's picture. :camera:")
            pasted = Image.open(self.image).convert("RGBA")  # Opens Selected Image
            pasted = pasted.resize(
                (278, int(pasted.size[1] * (278 / pasted.size[0])))
            )  # Resize image to width fit black area's width
            pasted = pasted.crop((0, 0, 278, 322))  # Crop height
            img.paste(pasted, (31, 141))  # Pastes image into template

        print("Fill form. :pencil:")
        imgdraw = ImageDraw.Draw(img)  # Create a canvas
        font = ImageFont.truetype("c:\\WINDOWS\\Fonts\\COUR.TTF", 48)  # Loads font
        imgdraw.text((515, 142), self.name, (0, 0, 255), font=font)  # Draws name
        imgdraw.text(
            (515, 221), self.birthday, (0, 0, 255), font=font
        )  # Draws description
        imgdraw.text((515, 300), self.owners, (0, 0, 255), font=font)  # Draws owners
        img.save(r".\out.png")  # Saves output
        print("------------------")
        print("Image saved as [bold red]out.png[/bold red]. :star:")
        print("------------------")

    def png_to_svg(self, png_path, svg_path):
        print("Generate SVG file.")
        # Charger l'image PNG
        img = Image.open(png_path)
        img = img.convert("RGBA")
        pixels = img.load()

        # Créer un dessin SVG
        dwg = svgwrite.Drawing(svg_path, size=(img.width, img.height))

        with alive_bar(
            img.height * img.width,
            title="Reading pixels",
            force_tty=True,
            stats="(eta:{eta})",
        ) as bar:
            # Dessiner chaque pixel non transparent
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = pixels[x, y]
                    if a != 0:  # Si le pixel n'est pas transparent
                        if r == g == b == 0:  # Si le pixel est noir
                            dwg.add(dwg.circle(center=(x, y), r=0.5))
                        else:
                            dwg.add(
                                dwg.circle(
                                    center=(x, y),
                                    r=0.5,
                                    fill="#{0:02x}{1:02x}{2:02x}".format(r, g, b),
                                )
                            )
                        bar()

        # Sauvegarder le fichier SVG
        dwg.save()
        print("------------------")
        print("Image saved as [bold red]out.svb[/bold red]. :star:")
        print("------------------")


def loadYaml(file):  # Load yaml file
    with open(file, "r") as f:
        return load(f, Loader=Loader)


def main(input, gensvg: bool = False):
    data = loadYaml(input)
    dir = os.path.dirname(input)
    amaztemp = myTemplate(data, dir)
    amaztemp.draw()
    if gensvg:
        amaztemp.png_to_svg("out.png", "out.svg")


if __name__ == "__main__":
    typer.run(main)
