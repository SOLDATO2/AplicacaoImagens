import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QDialog
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

ALTURA = 1600
LARGURA = 1024


def gaussianblur_img_widget(img_rgb):

    KSIZE = (15, 15)
    SIGMA_X = 0
    img_blur = cv2.GaussianBlur(img_rgb, KSIZE, SIGMA_X)
    
    altura, largura, channel = img_blur.shape
    bytes_per_line = largura * channel
    qimg = QImage(
        img_blur.data, largura, altura, bytes_per_line, QImage.Format_RGB888
    )
    return QPixmap.fromImage(qimg)


def sharpening(img_rgb):
    PROFUNDIDADE_IMG = -1
    kernel = np.array([
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ])
    img_sharpened = cv2.filter2D(img_rgb, PROFUNDIDADE_IMG, kernel)
    
    #src = img entrada
    #ddepth = profundidade img saida
    #quando depth recebe -1, a profundidade da imagem de saida eh igual a de entrada
    #kernel = operação de convolução
    #convolução = um deslizamento de um pequeno kernel sobre na imagem de entrada
    #cada pixel eh submetido a uma soma ponderada com o kernel, isso resulta em efeitos visuais
    #como sharpening, desfoque, detecção de bordas, etc
    return img_sharpened

def sharpen_img_widget(img_rgb):

    img_sharp = sharpening(img_rgb)
    altura, largura, channel = img_sharp.shape
    bytes_per_line = largura * channel
    qimg = QImage(
        img_sharp.data, largura, altura, bytes_per_line, QImage.Format_RGB888
    )
    return QPixmap.fromImage(qimg)

def rotacionar_45_img(img_rgb):

    altura, largura, channel = img_rgb.shape

    center = (largura / 2, altura / 2)

    angle = 45 
    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    
    rotated = cv2.warpAffine(img_rgb, rot_matrix, (largura, altura))

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
        self.image_path = None # pega caminho da imagem para usar nos outros botoes

        #widget central para alinhar os outros widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        #wid label
        self.image_label = QLabel("Nenhuma imagem selecionada")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        #wid anexo
        self.attach_button = QPushButton("Anexar Imagem")
        self.attach_button.clicked.connect(self.abrir_img)
        self.layout.addWidget(self.attach_button)
        
        #wid blur
        self.blur_button = QPushButton("Aplicar blur")
        self.blur_button.clicked.connect(self.blur_img)
        self.layout.addWidget(self.blur_button)
        
        #wid sharpness
        self.sharpen_button = QPushButton("Aplicar sharpness")
        self.sharpen_button.clicked.connect(self.sharpness_img)
        self.layout.addWidget(self.sharpen_button)

        #wid rotacao
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
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio
            ))

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
        pixmap_rotated = rotacionar_45_img(img_rgb)

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
