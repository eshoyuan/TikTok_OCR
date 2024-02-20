# TikTok OCR

This is SEU_309's Solution for [Low-resolution TikTok ID Recognition Competition held by ByteDance](https://security.bytedance.com/fe/2022/ai-challenge#/challenge).

## Usage

1. Install PaddlePaddle. 

   You can refer to  https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/quickstart_en.md#1-installation.

2. Install third-party libraries.

   `pip install -r requirements.txt`

3. Prepare the dataset.

   Unzip archive in `./data/`. Your directory & file structure should look like this, 

   ```
   Tiktok_OCR 
   │
   └───data
   │   │   train.txt
   │   │   eval.txt
   │   │
   │   └───train_set_random
   │   |   │   v0d00fg10000cb9gacjc77u3gp5qggd0_0_.jpg
   │   |   │   ...
   │   │
   │   └───test_set_random
   │       │   v0d00fg10000cb9gacjc77u3gp5qggd0_2_.jpg
   │   	│   ...
   
   ```

4. Execute the shell script.

   `sh run.sh ` 

## Details

More details can be found in our report [(English)](./report.md)/[(Chinese)](./report_cn.md).
