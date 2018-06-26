from PIL import Image
from tkinter import filedialog


class Pixel:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Circle:
    top = Pixel()
    bottom = Pixel()
    left = Pixel()
    right = Pixel()
    color = Pixel()
    diameter = 0
    radius = 0


WHITE = (255, 255, 255)


class ImageProcessor:
    image = None
    array = None
    width, height = 0, 0
    colors = list()
    circles = list()

    counter = 0

    def open_file(self, filename):
        self.image = Image.open(filename)
        self.width, self.height = self.image.size

        self.array = list()

        for y in range(0, self.height):
            line = list()
            for x in range(0, self.width):
                pixel = self.image.getpixel((x, y))
                r, g, b = pixel[0], pixel[1], pixel[2]
                line.append((r, g, b))
            self.array.append(line)

    def find_circles(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                r, g, b = self.array[y][x]
                if r + g + b != 255 * 3:
                    self.circle(Pixel(x, y))

        print(self.counter, "circles found")
        for c in self.colors:
            counter, color = c
            print(color, ": ", counter)
        biggest = self.circles[0]
        for circle in self.circles:
            if circle.diameter > biggest.diameter:
                biggest = circle.diameter
        print(biggest.diameter, "[", biggest.top.x, biggest.top.y, "] [", biggest.bottom.x, biggest.bottom.y, "]")

    def get_adjacent(self, x, y, color):

        adjacent = list()

        # Left
        if x > 0:
            c = self.array[y][x - 1]
            if c == color:
                self.array[y][x - 1] = WHITE
                adjacent.append(Pixel(x - 1, y))

        # Right
        if x < self.width - 1:
            c = self.array[y][x + 1]
            if c == color:
                self.array[y][x + 1] = WHITE
                adjacent.append(Pixel(x + 1, y))

        # Up
        if y > 0:
            c = self.array[y - 1][x]
            if c == color:
                self.array[y - 1][x] = WHITE
                adjacent.append(Pixel(x, y - 1))

        # Down
        if y < self.height - 1:
            c = self.array[y + 1][x]
            if c == color:
                self.array[y + 1][x] = WHITE
                adjacent.append(Pixel(x, y + 1))

        return adjacent

    def add_circle(self, color, left, right, up, down):
        self.counter += 1

        for index, tp in enumerate(self.colors):
            counter, c = tp
            if c == color:
                self.colors[index] = (counter + 1, color)
                return
        self.colors.append((1, color))

        circle = Circle()
        circle.left = left
        circle.right = right
        circle.top = up
        circle.bottom = down

        circle.diameter = circle.right.x - circle.left.x
        circle.radius = circle.diameter / 2

        self.circles.append(circle)

    def circle(self, pixel):
        leftmost = pixel
        rightmost = leftmost
        upmost = leftmost
        downmost = leftmost

        r, g, b = self.array[pixel.y][pixel.x]

        adjacent = self.get_adjacent(pixel.x, pixel.y, (r, g, b))
        self.array[pixel.y][pixel.x] = WHITE

        while True:
            new_adjacent = list()
            for ad in adjacent:

                if ad.x < leftmost.x:
                    leftmost = ad
                if ad.x > rightmost.x:
                    rightmost = ad
                if ad.y < upmost.y:
                    upmost = ad
                if ad.y > downmost.y:
                    downmost = ad

                for a in self.get_adjacent(ad.x, ad.y, (r, g, b)):
                    new_adjacent.append(a)

            adjacent = new_adjacent

            if not adjacent:
                break

        self.add_circle((r, g, b), leftmost, rightmost, upmost, downmost)


def main():

    ip = ImageProcessor()

    filename = filedialog.askopenfilename(initialdir=".",
                                          title="Select image",
                                          filetypes=(("PNG files", "*.png"), ("All files", "*")))

    ip.open_file(filename)
    ip.find_circles()


if __name__ == '__main__':
    main()
