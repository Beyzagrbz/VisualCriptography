import numpy as np
from PIL import Image

class VisualCrypto:
    def __init__(self, k=3):
        self.k = k
        
    def generate_shares(self, binary_image):
        """(3,3) görsel şifreleme şeması için payları oluşturur"""
        img = np.array(binary_image)
        h, w = img.shape
        shares = np.zeros((self.k, h*2, w*2), dtype=np.uint8)
        
        # Temel 2x2 desenler
        patterns = {
            'white': [
                np.array([[1, 0], [0, 1]]),  # Desen 1
                np.array([[0, 1], [1, 0]])   # Desen 2
            ],
            'black': [
                np.array([[1, 1], [0, 0]]),  # Desen 1
                np.array([[0, 0], [1, 1]]),  # Desen 2
                np.array([[1, 0], [1, 0]]),  # Desen 3
                np.array([[0, 1], [0, 1]])   # Desen 4
            ]
        }
        
        # Her piksel için
        for i in range(h):
            for j in range(w):
                if img[i,j] == 255:  # Beyaz piksel
                    # Rastgele bir beyaz desen seç
                    pattern = patterns['white'][np.random.randint(0, len(patterns['white']))]
                    
                    # Her pay için aynı deseni kullan
                    for k in range(self.k):
                        shares[k, i*2:i*2+2, j*2:j*2+2] = pattern * 255
                        
                else:  # Siyah piksel
                    # Her pay için farklı desen seç
                    for k in range(self.k):
                        pattern = patterns['black'][np.random.randint(0, len(patterns['black']))]
                        shares[k, i*2:i*2+2, j*2:j*2+2] = pattern * 255
        
        return [Image.fromarray(share) for share in shares]
    
    def combine_shares(self, shares):
        """Payları birleştirir"""
        # Payları numpy dizilerine dönüştür
        shares_array = [np.array(share) > 127 for share in shares]
        
        # İlk payı al
        combined = shares_array[0].astype(np.uint8)
        
        # Diğer payları OR işlemi ile birleştir
        for share in shares_array[1:]:
            combined = np.logical_or(combined, share)
        
        # Sonucu tersine çevir
        combined = np.logical_not(combined)
        
        # Görüntüye dönüştür
        return Image.fromarray(combined.astype(np.uint8) * 255)
