# ラズパイでの写真の撮り方

1.  ```bash
    #ラズパイ
    cd py
    python take_pic.py
    ```
2. ```bash
    #自分のpcのターミナル
    scp pi@raspberrypi.local:/home/pi/py/image.jpg <写真をダウンロードしたいディレクトリ>
    ```