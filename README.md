

已经有明确链接的数据集

  HICRD数据集
  
    https://data.csiro.au/collection/csiro:49488
  
  Seathru数据集
  
    https://www.kaggle.com/datasets/colorlabeilat/seathru-dataset

  SQUID数据集

    https://zenodo.org/records/5744037

  UVEB数据集

    https://github.com/yzbouc/UVEB

  NYU-U数据集

    https://li-chongyi.github.io/proj_underwater_image_synthesis.html

  SUVE数据集

    https://drive.google.com/drive/folders/1kr3mYyctNbcnJdSR0hjEUkahoDd5cH0h

  TURBID数据集

    http://amandaduarte.com.br/turbid/

  UFO数据集

    https://gitcode.com/open-source-toolkit/c377e

  UGAN数据集
  
    https://www.kaggle.com/datasets/karimraoufmostafa/underwater-imagenet-dataset

  UIEB数据集

    https://li-chongyi.github.io/proj_benchmark.html

  LSUI数据集

    https://drive.google.com/file/d/1M8CxfoeJaH_MCSQRhYxw4MtbaZ87OMYS/view

    项目主页链接：https://github.com/LintaoPeng/U-shape_Transformer_for_Underwater_Image_Enhancement 

  UVE-38k数据集

    https://github.com/TrentQiQ/UVE-38K?tab=readme-ov-file

  EUVP数据集

    https://www.kaggle.com/datasets/pamuduranasinghe/euvp-dataset

  SUID数据集

    https://ieee-dataport.org/open-access/suid-synthetic-underwater-image-dataset

有一些学术占位的数据集

  SynUIEDatasets
  
    https://github.com/yftian2025/SynUIEDatasets

  WaterPairs

     https://github.com/IanDragon/WaterPairs

unzip.py:处理数据集的时候，可能一个数据集里面有很多个压缩包，一个个手动解压太low了。只要把这个脚本放在跟压缩包一个目录下，直接运行就可以批量打开了。但是这个不能解压.rar文件。

spilt.py:就是先删除之前已经划分好的训练测试集。然后划分数据集的时候，将质量高的图像对一半给测试集，一半给训练集。总体划分比例是8：2。
