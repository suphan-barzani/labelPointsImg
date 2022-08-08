
import os
import tempfile

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from libs.yolo_io import YoloReader

def create_subimage(image, shape):
    x_min = shape[1][0][0]
    y_min = shape[1][0][1]
    
    x_max = shape[1][2][0]
    y_max = shape[1][2][1]

    return image.copy(QRect(x_min, y_min, x_max-x_min, y_max-y_min))

# This method takes an annotation file and extract the patches into different image files.
def create_patch_files(labelfile):
    formats = [f'{fmt.data().decode("ascii").lower()}'
               for fmt in QImageReader.supportedImageFormats()]
    image_file_names = [labelfile[:-3] + ext for ext in formats]

    imagefile = None

    for filename in image_file_names:
        if os.path.exists(filename):
            imagefile = filename

    if imagefile is None:
        return

    reader = QImageReader(imagefile)
    reader.setAutoTransform(True)
    image = reader.read()

    t_yolo_parse_reader = YoloReader(labelfile, image)
    shapes = t_yolo_parse_reader.get_shapes()

    tmpdirname = tempfile.gettempdir()

    to_return = []
    
    for i, shape in enumerate(shapes):
        patch = create_subimage(image, shape)

        filename = os.path.basename(labelfile)[:-4]
        filename = f'{filename}_{i}.points.jpg'
        filename = os.path.join(tmpdirname, filename)

        patch.save(filename)

        to_return.append(filename)
    
    return to_return

DEFAULT_POINT_FILL_COLOR = QColor(255, 0, 0, 255)

class Point:
    point_size = 16
    scale = 1.0
    vertex_point_color = DEFAULT_POINT_FILL_COLOR

    def __init__(self, pos):
        self.x = pos.x()
        self.y = pos.y()
    
    def paint(self, painter):
        d = self.point_size / self.scale
        
        path = QPainterPath()
        path.addEllipse(self.x, self.y, d / 2.0, d / 2.0)
        
        painter.drawPath(path)
        painter.fillPath(path, DEFAULT_POINT_FILL_COLOR)
