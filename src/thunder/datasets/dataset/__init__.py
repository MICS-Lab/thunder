# import downloaders
# import split generators
from .bach import create_splits_bach, download_bach
from .bracs import create_splits_bracs, download_bracs
from .break_his import create_splits_break_his, download_break_his
from .ccrcc import create_splits_ccrcc, download_ccrcc
from .crc import create_splits_crc, download_crc
from .esca import create_splits_esca, download_esca
from .mhist import create_splits_mhist, download_mhist
from .ocelot import create_splits_ocelot, download_ocelot
from .pannuke import create_splits_pannuke, download_pannuke
from .patch_camelyon import (create_splits_patch_camelyon,
                             download_patch_camelyon)
from .segpath_epithelial import (create_splits_segpath_epithelial,
                                 download_segpath_epithelial)
from .segpath_lymphocytes import (create_splits_segpath_lymphocytes,
                                  download_segpath_lymphocytes)
from .tcga_crc_msi import create_splits_tcga_crc_msi, download_tcga_crc_msi
from .tcga_tils import create_splits_tcga_tils, download_tcga_tils
from .tcga_uniform import create_splits_tcga_uniform, download_tcga_uniform
from .wilds import create_splits_wilds, download_wilds
from .spider_breast import create_splits_spider_breast, download_spider_breast
from .spider_colorectal import create_splits_spider_colorectal, download_spider_colorectal
from .spider_skin import create_splits_spider_skin, download_spider_skin
from .spider_thorax import create_splits_spider_thorax, download_spider_thorax
