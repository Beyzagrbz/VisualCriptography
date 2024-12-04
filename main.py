import numpy as np
from PIL import Image
import os
from dithering import floyd_steinberg_dithering
from visual_crypto import VisualCrypto

def main():
    # Çıktı klasörünü oluştur
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Görüntüyü yükle ve gri seviyeye dönüştür
    try:
        image = Image.open('input.png').convert('L')
    except:
        print("Lütfen 'input.png' dosyasını proje klasörüne ekleyin!")
        return
    
    # Görüntü boyutunu küçült (isteğe bağlı)
    # image = image.resize((256, 256), Image.LANCZOS)
    
    # Görüntüyü kaydet
    image.save('output/1_grayscale.png')
    
    # Dithering uygula ve eşikleme yap
    binary_image = floyd_steinberg_dithering(image)
    binary_array = np.array(binary_image)
    binary_image = Image.fromarray((binary_array > 127).astype(np.uint8) * 255)
    binary_image.save('output/2_dithered.png')
    
    # Görsel şifreleme
    vc = VisualCrypto(k=3)
    shares = vc.generate_shares(binary_image)
    
    # Payları kaydet
    for i, share in enumerate(shares):
        share.save(f'output/3_share_{i+1}.png')
    
    # Payları birleştir
    combined = vc.combine_shares(shares)
    combined.save('output/4_combined.png')
    
    print("İşlem tamamlandı! Çıktılar 'output' klasöründe.")

if __name__ == "__main__":
    main()