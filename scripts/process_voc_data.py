import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
from ultralytics.utils.downloads import download

def convert_label(path, lb_path, year, image_id):
    """Конвертирует аннотации в формате VOC в формат YOLO, извлекая координаты ограничивающих рамок и ID классов."""

    def convert_box(size, box):
        dw, dh = 1.0 / size[0], 1.0 / size[1]
        x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
        return x * dw, y * dh, w * dw, h * dh

    # Чтение XML аннотации
    in_file = open(path / f"VOC{year}/Annotations/{image_id}.xml")
    out_file = open(lb_path, "w")
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    # Список классов
    names = list(yaml["names"].values())  # names list
    for obj in root.iter("object"):
        cls = obj.find("name").text
        if cls in names and int(obj.find("difficult").text) != 1:
            xmlbox = obj.find("bndbox")
            bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ("xmin", "xmax", "ymin", "ymax")])
            cls_id = names.index(cls)  # class id
            out_file.write(" ".join(str(a) for a in (cls_id, *bb)) + "\n")

def convert_data():
    dir = Path("/app/datasets/")  # root dir

    # Конвертация данных
    path = dir / "images/VOCdevkit"
    for year, image_set in [("2007", "val"), ("2007", "test")]:
        imgs_path = dir / "images" / f"{image_set}{year}"
        lbs_path = dir / "labels" / f"{image_set}{year}"
        imgs_path.mkdir(exist_ok=True, parents=True)
        lbs_path.mkdir(exist_ok=True, parents=True)

        with open(path / f"VOCtrainval_06-Nov-2007/ImageSets/Main/{image_set}.txt") as f:
            image_ids = f.read().strip().split()
        for id in tqdm(image_ids, desc=f"{image_set}{year}"):
            f = path / f"VOC{year}/JPEGImages/{id}.jpg"  # old img path
            lb_path = (lbs_path / f.name).with_suffix(".txt")  # new label path
            f.rename(imgs_path / f.name)  # move image
            convert_label(path, lb_path, year, id)  # convert labels to YOLO format

if __name__ == "__main__":
    convert_data()