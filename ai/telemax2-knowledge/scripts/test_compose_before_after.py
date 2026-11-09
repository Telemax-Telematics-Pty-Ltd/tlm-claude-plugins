import json
import os
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import compose_before_after as cba  # noqa: E402


class ComposeBeforeAfterTests(unittest.TestCase):
    def test_one_pair_side_by_side_with_a_label_band(self):
        before = Image.new("RGB", (300, 200), (255, 0, 0))
        after = Image.new("RGB", (300, 200), (0, 255, 0))

        image = cba.compose([(before, after)], "BEFORE", "AFTER")

        self.assertEqual((300 + cba.GAP + 300, 200 + cba.LABEL_HEIGHT), image.size)
        self.assertEqual((255, 0, 0), image.getpixel((150, cba.LABEL_HEIGHT + 100)), "before on the left")
        self.assertEqual((0, 255, 0), image.getpixel((300 + cba.GAP + 150, cba.LABEL_HEIGHT + 100)), "after on the right")

    def test_pairs_stack_and_wide_results_shrink_to_the_upload_width(self):
        shot = Image.new("RGB", (1440, 900), "white")

        image = cba.compose([(shot, shot), (shot, shot)], "B", "A")

        self.assertEqual(cba.MAX_WIDTH, image.width)
        full_height = 2 * (900 + cba.LABEL_HEIGHT) + cba.GAP
        self.assertEqual(round(full_height * cba.MAX_WIDTH / (1440 * 2 + cba.GAP)), image.height)

    def test_title_and_captions_add_a_band_above_the_images(self):
        shot = Image.new("RGB", (300, 200), "white")

        plain = cba.compose([(shot, shot)], "B", "A")
        titled = cba.compose([(shot, shot)], "B", "A", title="TLM-1: case", captions=["Expected: x", "Before: y"])

        self.assertGreater(titled.height, plain.height + cba.GAP)
        self.assertEqual(plain.width, titled.width)

    def test_boxes_are_drawn_red_on_before_and_green_on_after(self):
        white = Image.new("RGB", (300, 200), "white")
        box = [{"x": 100, "y": 80, "w": 60, "h": 40}]

        image = cba.compose([(white, white)], "B", "A", boxes=[(box, box)])

        edge_y = cba.LABEL_HEIGHT + 80 - cba.BOX_WIDTH  # inside the top edge of the drawn rectangle
        self.assertEqual(cba.BEFORE_COLOUR, image.getpixel((130, edge_y)))
        self.assertEqual(cba.AFTER_COLOUR, image.getpixel((300 + cba.GAP + 130, edge_y)))
        self.assertEqual((255, 255, 255), image.getpixel((130, cba.LABEL_HEIGHT + 100)), "the box is an outline")

    def test_boxes_come_from_the_sidecar_next_to_the_screenshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            shot = os.path.join(tmp, "before-1-today.png")
            Image.new("RGB", (10, 10)).save(shot)
            self.assertEqual([], cba.load_boxes(shot), "no sidecar, no box")
            with open(os.path.join(tmp, "before-1-today.box.json"), "w", encoding="utf-8") as f:
                json.dump([{"x": 1, "y": 2, "w": 3, "h": 4, "label": "Days included"}], f)
            self.assertEqual("Days included", cba.load_boxes(shot)[0]["label"])

    def test_cli_refuses_an_unpaired_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            one = os.path.join(tmp, "one.png")
            Image.new("RGB", (10, 10)).save(one)
            with self.assertRaises(SystemExit):
                cba.main([os.path.join(tmp, "out.png"), one])


if __name__ == "__main__":
    unittest.main()
