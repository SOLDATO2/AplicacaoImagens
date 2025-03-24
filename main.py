import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

ALTURA = 1600
LARGURA = 1024


def gaussianblur_img_widget(img_rgb):

    KSIZE = (15, 15)
    SIGMA_X = 0
    img_blur = cv2.GaussianBlur(img_rgb, KSIZE, SIGMA_X)
    
    height, width, channel = img_blur.shape
    bytes_per_line = width * channel
    qimg = QImage(
        img_blur.data, width, height, bytes_per_line, QImage.Format_RGB888
    )
    return QPixmap.fromImage(qimg)

PROFUNDIDADE_IMG = -1
def sharpening(img_rgb):
    """
    Aplica um filtro de nitidez (sharpen) usando convolução 2D.
    'img_rgb' deve ser um array NumPy em espaço de cor RGB.
    """
    kernel = np.array([
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ])
    img_sharpened = cv2.filter2D(img_rgb, PROFUNDIDADE_IMG, kernel)
    return img_sharpened

def sharpen_img_widget(img_rgb):
    """
    Aplica o sharpening (nitidez) em uma imagem (RGB) e
    retorna um QPixmap para exibição em widgets PyQt.
    """
    img_sharp = sharpening(img_rgb)
    height, width, channel = img_sharp.shape
    bytes_per_line = width * channel
    qimg = QImage(
        img_sharp.data, width, height, bytes_per_line, QImage.Format_RGB888
    )
    return QPixmap.fromImage(qimg)

def rotate_45_img_widget(img_rgb):
    """
    Rotaciona a imagem em 45 graus (no sentido anti-horário).
    Retorna um QPixmap para exibição em widgets PyQt.
    """
    height, width, channel = img_rgb.shape

    center = (width / 2, height / 2)

    angle = 45 
    scale = 1.0
    rot_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    rotated = cv2.warpAffine(img_rgb, rot_matrix, (width, height))

    height_r, width_r, channel_r = rotated.shape
    bytes_per_line = width_r * channel_r
    qimg = QImage(
        rotated.data, width_r, height_r, bytes_per_line, QImage.Format_RGB888
    )
    return QPixmap.fromImage(qimg)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("processamento de imagens")
        
        #caminho
        self.image_path = None

        #widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        #label
        self.image_label = QLabel("Nenhuma imagem selecionada")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        #anexo
        self.attach_button = QPushButton("Anexar Imagem")
        self.attach_button.clicked.connect(self.abrir_img)
        self.layout.addWidget(self.attach_button)
        
        #blur
        self.blur_button = QPushButton("Aplicar blur")
        self.blur_button.clicked.connect(self.blur_img)
        self.layout.addWidget(self.blur_button)
        
        #sharpness
        self.sharpen_button = QPushButton("Aplicar sharpness")
        self.sharpen_button.clicked.connect(self.sharpness_img)
        self.layout.addWidget(self.sharpen_button)

        #rotacao
        self.rotate_button = QPushButton("Rotacionar 45 garus")
        self.rotate_button.clicked.connect(self.aplicar_rotacao)
        self.layout.addWidget(self.rotate_button)
    
    def abrir_img(self):

        options = QFileDialog.Options() #pega opcoes de imagem
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione uma imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif)",
            options=options
        )
        
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path) #pixmap do qt pra manipular imagens
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio
                ))
            else:
                self.image_label.setText("Erro ao carregar imagem")

    def blur_img(self):

        
        img_bgr = cv2.imread(self.image_path)
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        pixmap_blur = gaussianblur_img_widget(img_rgb)
    
        self.mostrar_pixmap(pixmap_blur, "Imagem com Blur")

    def sharpness_img(self):
        
        img_bgr = cv2.imread(self.image_path)
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        pixmap_sharp = sharpen_img_widget(img_rgb)
        
        self.mostrar_pixmap(pixmap_sharp, "Imagem com Sharpness")

    def aplicar_rotacao(self):
                
        img_bgr = cv2.imread(self.image_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        pixmap_rotated = rotate_45_img_widget(img_rgb)

        self.mostrar_pixmap(pixmap_rotated, "Imagem Rotacionada")

    def mostrar_pixmap(self, pixmap: QPixmap, title: str):

        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout(dialog)
        
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(pixmap.scaled(
            ALTURA, LARGURA, Qt.KeepAspectRatio))
        layout.addWidget(label)
        
        dialog.resize(ALTURA, LARGURA)
        dialog.exec_()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.resize(ALTURA, LARGURA)
    window.show()
    sys.exit(app.exec_())
