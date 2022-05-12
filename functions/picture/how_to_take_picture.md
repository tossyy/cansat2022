# ラズパイでの写真の撮り方

1.  ```bash
    #ラズパイにて
    cd py
    python take_pic.py
    ```
2. ```bash
    #ラズパイ上では写真を見れないので、自分のpcにダウンロードする
    #自分のpcのターミナルにて
    scp pi@raspberrypi.local:/home/pi/py/image.jpg <写真をダウンロードしたいディレクトリ>
    ```