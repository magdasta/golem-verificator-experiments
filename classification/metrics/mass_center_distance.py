from PIL import Image
import sys


class MetricMassCenterDistance:

    def compute_metrics(self, image1, image2):
        if image1.size != image2.size:
            raise Exception("Image sizes differ")
        mass_centers_1 = MetricMassCenterDistance.compute_mass_centers(image1)
        mass_centers_2 = MetricMassCenterDistance.compute_mass_centers(image2)
        max_x_distance = 0
        max_y_distance = 0
        for channel_index in mass_centers_1.keys():
            x1, y1 = mass_centers_1[channel_index]
            x2, y2 = mass_centers_2[channel_index]
            x_distance = abs(x1 - x2)
            y_distance = abs(y1 - y2)
            max_x_distance = max(max_x_distance, x_distance)
            max_y_distance = max(max_y_distance, y_distance)
        return {
            "max_x_mass_center_distance": max_x_distance,
            "max_y_mass_center_distance": max_y_distance
                }

    def get_labels(self):
        return ["max_x_mass_center_distance", "max_y_mass_center_distance"]

    @staticmethod
    def get_at_x_y(pixels, width, x, y):
        return pixels[width * y + x]

    @staticmethod
    def compute_mass_centers(image):
        pixels = image.getdata()
        width, height = image.size
        results = dict()
        for channel_index in range(len(pixels[0])):
            mass_center_x = 0
            mass_center_y = 0
            total_mass = 0
            for x in range(width):
                for y in range(height):
                    mass = MetricMassCenterDistance.get_at_x_y(pixels, width, x, y)[channel_index]
                    mass_center_x += mass * x
                    mass_center_y += mass * y
                    total_mass += mass
            results[channel_index] = mass_center_x / (float(total_mass) * width), \
                                     mass_center_y / (float(total_mass) * height)
        return results


def run():
    first_img = Image.open(sys.argv[1])
    second_img = Image.open(sys.argv[2])

    mass_center_distance = MetricMassCenterDistance()

    print(mass_center_distance.compute_metrics(first_img, second_img))


if __name__ == "__main__":
    run()