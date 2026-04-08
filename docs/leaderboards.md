# Leaderboards

## Updates
* **2026-04-08**: **[Per-dataset linear probing performance]** GenBio-PathFM added to the per-dataset linear probing table.
* **2026-04-08**: **[SPIDER Leaderboard]** GenBio-PathFM added to the SPIDER leaderboard.
* **2026-04-08**: **[Up-to-date Rank-sum Leaderboard]** GenBio-PathFM added to the updated rank-sum leaderboard.
* **2026-04-01**: **[Per-dataset linear probing performance]** A new table with all linear probing results was added.
* **2025-12-07**: **[SPIDER Leaderboard]** OpenMidnight added to the SPIDER leaderboard.
* **2025-12-07**: **[Up-to-date Rank-sum Leaderboard]** OpenMidnight added to the updated rank-sum leaderboard.
* **2025-11-21**: **[SPIDER Leaderboard]** H0-mini added to the SPIDER leaderboard.
* **2025-11-21**: **[Up-to-date Rank-sum Leaderboard]** H0-mini added to the updated rank-sum leaderboard.
* **2025-11-14**: **[SPIDER Leaderboard]** DINOv3-S, DINOv3-B, DINOv3-L, GIGAPATH, KAIKO-S/16, KAIKO-B/16 added to the SPIDER leaderboard.
* **2025-11-14**: **[Up-to-date Rank-sum Leaderboard]** GIGAPATH, KAIKO-S/16, KAIKO-B/16 added to the updated rank-sum leaderboard.
* **2025-10-30**: **[Up-to-date Rank-sum Leaderboard]** A new up-to-date rank-sum leaderboard was added. This is an update of the rank-sum leaderboard (Table 4) in our [paper](https://arxiv.org/abs/2507.07860) with new datasets and models, e.g. here we added results for SPIDER datasets and DINOv3 model variants.
* **2025-10-27**: **[Original (paper) Rank-sum Leaderboard]**  Our arXiv paper was updated and now the rank-sum table in it (Table 4) matches exactly our **Original (paper) Rank-sum Leaderboard**.
* **2025-10-06**: **[Zero-shot VLM Classification Leaderboard]** A new zero-shot classification task was integrated into THUNDER. Results are presented in a dedicated leaderboard below.
* **2025-09-30**: **[SPIDER Leaderboard]** Four SPIDER datasets have been integrated into THUNDER. We have created a leaderboard dedicated to SPIDER datasets below.
* **2025-09-01**: **[Original (paper) Rank-sum Leaderboard]** Segmentation results were updated (small changes based on improved performance for all models on the *ocelot* dataset only -> [Related commit](https://github.com/MICS-Lab/thunder/commit/5f6d6e7cdd6a1df5affed2dac47233f80ce5a205)). Segmentation and global rankings do no thus match exactly (a few small differences only) Table 4 from the current version of our [paper](https://arxiv.org/abs/2507.07860). The paper will be updated soon. **[This was now updated on 2025-10-30]**

---

## 🏆 Up-to-date Rank-sum Leaderboard

This leaderboard is an updated version of the rank-sum table (Table 4) in our original [paper](https://arxiv.org/abs/2507.07860).

The following was added (compared with paper results):

* **New datasets**: SPIDER datasets (SPIDER-Breast, SPIDER-Colorectal, SPIDER-skin, SPIDER-thorax -- only classification tasks, i.e. all tasks except segmentation).
* **New models**: DINOv3 model variants (DINOv3-S, DINOv3-B, DINOv3-L), GIGAPATH, KAIKO-S/16, KAIKO-B/16, OpenMidnight, GenBio-PathFM.

<div class="table-responsive-sm">
  <table id="ranksumTableUpToDate" class="table table-hover table-bordered table-sm nowrap">
    <thead class="align-middle text-center">
      <tr>
        <th>Model</th>
        <th>Domain</th>
        <th>Type</th>
        <th>KNN &uarr;</th>
        <th>Lin. prob. &uarr;</th>
        <th>Few-shot &uarr;</th>
        <th>Seg.&uarr;</th>
        <th>Calib. &darr;</th>
        <th>Adv. attack &darr;</th>
        <th>Rank sum &darr;</th>
      </tr>
    </thead>
    <tbody>
          <tr><td>HIBOU-B</td><td>Histopathology</td><td>VM</td><td>78.9 (12)</td><td>81.2 (16)</td><td>76.3 (7)</td><td>67.8 (10)</td><td>3.2 (4)</td><td>52.7 (17)</td><td>66 (10)</td></tr>
          <tr><td>HIBOU-L</td><td>Histopathology</td><td>VM</td><td>78.6 (15)</td><td>83.7 (7)</td><td>73.8 (13)</td><td>68.6 (6)</td><td>4.7 (16)</td><td>39.5 (9)</td><td>66 (10)</td></tr>
          <tr><td>H-OPTIMUS-0</td><td>Histopathology</td><td>VM</td><td>81.4 (6)</td><td>83.8 (6)</td><td>76.2 (8)</td><td>65.2 (13)</td><td>4.0 (10)</td><td>43.9 (14)</td><td>57 (8)</td></tr>
          <tr><td>H-OPTIMUS-1</td><td>Histopathology</td><td>VM</td><td>82.5 (4)</td><td>85.1 (3)</td><td>77.3 (4)</td><td>64.5 (15)</td><td>3.5 (6)</td><td>57.4 (20)</td><td>52 (6)</td></tr>
          <tr><td>MIDNIGHT</td><td>Histopathology</td><td>VM</td><td>79.9 (8)</td><td>84.7 (5)</td><td>71.5 (18)</td><td>68.8 (5)</td><td>2.9 (2)</td><td>37.0 (6)</td><td>44 (4)</td></tr>
          <tr><td>PHIKON</td><td>Histopathology</td><td>VM</td><td>75.7 (19)</td><td>80.9 (18)</td><td>73.6 (14)</td><td>68.0 (9)</td><td>5.8 (20)</td><td>33.5 (3)</td><td>83 (17)</td></tr>
          <tr><td>PHIKON2</td><td>Histopathology</td><td>VM</td><td>73.9 (20)</td><td>79.7 (19)</td><td>71.8 (17)</td><td>67.4 (11)</td><td>3.9 (9)</td><td>43.8 (13)</td><td>89 (18)</td></tr>
          <tr><td>UNI</td><td>Histopathology</td><td>VM</td><td>80.8 (7)</td><td>83.5 (8)</td><td>78.1 (3)</td><td>67.8 (10)</td><td>3.8 (8)</td><td>40.3 (10)</td><td>46 (5)</td></tr>
          <tr><td>UNI2-H</td><td>Histopathology</td><td>VM</td><td>83.3 (2)</td><td>85.7 (1)</td><td>79.8 (1)</td><td>69.0 (4)</td><td>3.9 (9)</td><td>31.7 (2)</td><td>19 (1)</td></tr>
          <tr><td>VIRCHOW</td><td>Histopathology</td><td>VM</td><td>77.4 (18)</td><td>82.8 (11)</td><td>71.8 (17)</td><td>69.2 (2)</td><td>4.5 (14)</td><td>38.3 (7)</td><td>69 (11)</td></tr>
          <tr><td>VIRCHOW2</td><td>Histopathology</td><td>VM</td><td>82.9 (3)</td><td>84.8 (4)</td><td>73.9 (12)</td><td>69.3 (1)</td><td>3.9 (9)</td><td>31.1 (1)</td><td>30 (2)</td></tr>
          <tr><td>CONCH</td><td>Histopathology</td><td>VLM</td><td>78.8 (13)</td><td>81.9 (13)</td><td>73.4 (15)</td><td>68.3 (7)</td><td>4.1 (11)</td><td>57.3 (19)</td><td>78 (14)</td></tr>
          <tr><td>CONCH&nbsp;1.5</td><td>Histopathology</td><td>VLM</td><td>79.9 (8)</td><td>82.4 (12)</td><td>75.0 (11)</td><td>68.8 (5)</td><td>4.6 (15)</td><td>75.8 (30)</td><td>81 (16)</td></tr>
          <tr><td>KEEP</td><td>Histopathology</td><td>VLM</td><td>81.5 (5)</td><td>83.2 (9)</td><td>77.1 (5)</td><td>68.0 (9)</td><td>4.0 (10)</td><td>44.9 (15)</td><td>53 (7)</td></tr>
          <tr><td>MUSK</td><td>Histopathology</td><td>VLM</td><td>77.7 (17)</td><td>81.1 (17)</td><td>71.9 (16)</td><td>65.1 (14)</td><td>4.0 (10)</td><td>71.9 (29)</td><td>103 (19)</td></tr>
          <tr><td>PLIP</td><td>Histopathology</td><td>VLM</td><td>70.2 (25)</td><td>74.0 (27)</td><td>64.1 (22)</td><td>58.5 (26)</td><td>4.5 (14)</td><td>60.8 (21)</td><td>135 (25)</td></tr>
          <tr><td>QUILTNET</td><td>Histopathology</td><td>VLM</td><td>70.4 (24)</td><td>73.9 (28)</td><td>65.6 (20)</td><td>58.9 (25)</td><td>5.8 (20)</td><td>55.6 (18)</td><td>135 (25)</td></tr>
          <tr><td>DINOv2-B</td><td>Natural-image</td><td>VM</td><td>69.0 (27)</td><td>76.6 (24)</td><td>60.2 (24)</td><td>59.8 (23)</td><td>5.0 (18)</td><td>66.1 (24)</td><td>140 (26)</td></tr>
          <tr><td>DINOv2-L</td><td>Natural-image</td><td>VM</td><td>70.6 (23)</td><td>77.0 (23)</td><td>58.7 (25)</td><td>59.6 (24)</td><td>4.9 (17)</td><td>64.4 (23)</td><td>135 (25)</td></tr>
          <tr><td>ViT-B/16</td><td>Natural-image</td><td>VM</td><td>66.2 (28)</td><td>74.7 (26)</td><td>57.3 (27)</td><td>61.0 (21)</td><td>4.0 (10)</td><td>47.0 (16)</td><td>128 (24)</td></tr>
          <tr><td>ViT-L/16</td><td>Natural-image</td><td>VM</td><td>69.3 (26)</td><td>75.5 (25)</td><td>56.9 (28)</td><td>63.1 (18)</td><td>4.3 (13)</td><td>43.9 (14)</td><td>124 (23)</td></tr>
          <tr><td>CLIP-B/32</td><td>Natural-image</td><td>VLM</td><td>63.0 (30)</td><td>68.8 (30)</td><td>52.3 (29)</td><td>56.0 (27)</td><td>4.9 (17)</td><td>63.6 (22)</td><td>155 (28)</td></tr>
          <tr><td>CLIP-L/14</td><td>Natural-image</td><td>VLM</td><td>65.7 (29)</td><td>73.6 (29)</td><td>58.1 (26)</td><td>60.8 (22)</td><td>3.8 (8)</td><td>70.5 (28)</td><td>142 (27)</td></tr>
          <tr><td>DINOv3-B</td><td>Natural-image</td><td>VM</td><td>70.6 (23)</td><td>77.4 (21)</td><td>64.8 (21)</td><td>63.4 (17)</td><td>3.7 (7)</td><td>70.1 (27)</td><td>116 (22)</td></tr>
          <tr><td>DINOv3-S</td><td>Natural-image</td><td>VM</td><td>72.0 (21)</td><td>77.1 (22)</td><td>65.7 (19)</td><td>62.0 (20)</td><td>2.8 (1)</td><td>66.9 (25)</td><td>108 (20)</td></tr>
          <tr><td>DINOv3-L</td><td>Natural-image</td><td>VM</td><td>71.5 (22)</td><td>77.9 (20)</td><td>61.8 (23)</td><td>62.6 (19)</td><td>3.0 (3)</td><td>68.9 (26)</td><td>113 (21)</td></tr>
          <tr><td>GIGAPATH</td><td>Histopathology</td><td>VM</td><td>79.5 (10)</td><td>82.9 (10)</td><td>75.5 (9)</td><td>63.5 (16)</td><td>3.4 (5)</td><td>42.1 (11)</td><td>61 (9)</td></tr>
          <tr><td>KAIKO-S/16</td><td>Histopathology</td><td>VM</td><td>78.2 (16)</td><td>81.7 (14)</td><td>75.1 (10)</td><td>66.8 (12)</td><td>4.6 (15)</td><td>42.5 (12)</td><td>79 (15)</td></tr>
          <tr><td>KAIKO-B/16</td><td>Histopathology</td><td>VM</td><td>78.7 (14)</td><td>81.4 (15)</td><td>76.4 (6)</td><td>66.8 (12)</td><td>5.0 (18)</td><td>38.8 (8)</td><td>73 (12)</td></tr>
          <tr><td>H0-mini</td><td>Histopathology</td><td>VM</td><td>79.7 (9)</td><td>83.8 (6)</td><td>75.0 (11)</td><td>69.1 (3)</td><td>3.8 (8)</td><td>34.3 (4)</td><td>41 (3)</td></tr>
          <tr><td>OpenMidnight</td><td>Histopathology</td><td>VM</td><td>79.3 (11)</td><td>84.7 (5)</td><td>43.7 (30)</td><td>69.1 (3)</td><td>5.4 (19)</td><td>38.3 (7)</td><td>75 (13)</td></tr>
          <tr><td>GenBio-PFM</td><td>Histopathology</td><td>VM</td><td>83.4 (1)</td><td>85.3 (2)</td><td>79.4 (2)</td><td>68.2 (8)</td><td>4.2 (12)</td><td>34.9 (5)</td><td>30 (2)</td></tr>
    </tbody>
  </table>
</div>

---

## 🏆 Original (paper) Rank-sum Leaderboard

This leaderboard exactly reproduces the rank-sum table (Table 4) presented in our original [paper](https://arxiv.org/abs/2507.07860). 

<div class="table-responsive-sm">
  <table id="ranksumTableOriginal" class="table table-hover table-bordered table-sm nowrap">
    <thead class="align-middle text-center">
      <tr>
        <th>Model</th>
        <th>Domain</th>
        <th>Type</th>
        <th>KNN &uarr;</th>
        <th>Lin. prob. &uarr;</th>
        <th>Few-shot &uarr;</th>
        <th>Seg.&uarr;</th>
        <th>Calib. &darr;</th>
        <th>Adv. attack &darr;</th>
        <th>Rank sum &darr;</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>HIBOU-B</td><td>Histopathology</td><td>VM</td><td>75.8 (10)</td><td>78.0 (14)</td><td>74.2 (6)</td><td>67.8 (10)</td><td>3.7 (2)</td><td>52.8 (14)</td><td>56 (7)</td></tr>
      <tr><td>HIBOU-L</td><td>Histopathology</td><td>VM</td><td>75.2 (12)</td><td>81.2 (7)</td><td>70.4 (12)</td><td>68.6 (6)</td><td>5.5 (18)</td><td>40.0 (5)</td><td>60 (8)</td></tr>
      <tr><td>H-OPTIMUS-0</td><td>Histopathology</td><td>VM</td><td>79.2 (5)</td><td>81.4 (5)</td><td>73.4 (7)</td><td>65.2 (13)</td><td>4.7 (13)</td><td>44.2 (9)</td><td>52 (6)</td></tr>
      <tr><td>H-OPTIMUS-1</td><td>Histopathology</td><td>VM</td><td>80.5 (3)</td><td>83.3 (2)</td><td>74.8 (4)</td><td>64.5 (15)</td><td>4.1 (4)</td><td>58.0 (17)</td><td>45 (5)</td></tr>
      <tr><td>MIDNIGHT</td><td>Histopathology</td><td>VM</td><td>78.2 (8)</td><td>82.9 (3)</td><td>70.6 (11)</td><td>68.8 (4)</td><td>3.2 (1)</td><td>36.3 (4)</td><td>31 (3)</td></tr>
      <tr><td>PHIKON</td><td>Histopathology</td><td>VM</td><td>72.8 (14)</td><td>78.4 (13)</td><td>72.2 (10)</td><td>68.0 (9)</td><td>6.4 (22)</td><td>34.4 (3)</td><td>71 (11)</td></tr>
      <tr><td>PHIKON2</td><td>Histopathology</td><td>VM</td><td>70.1 (15)</td><td>76.5 (15)</td><td>70.1 (13)</td><td>67.4 (12)</td><td>4.6 (11)</td><td>45.6 (11)</td><td>77 (12)</td></tr>
      <tr><td>UNI</td><td>Histopathology</td><td>VM</td><td>78.8 (6)</td><td>81.3 (6)</td><td>76.4 (2)</td><td>67.8 (11)</td><td>4.3 (7)</td><td>42.8 (7)</td><td>39 (4)</td></tr>
      <tr><td>UNI2-H</td><td>Histopathology</td><td>VM</td><td>81.7 (1)</td><td>83.9 (1)</td><td>78.4 (1)</td><td>69.0 (3)</td><td>4.5 (8)</td><td>34.3 (2)</td><td>16 (1)</td></tr>
      <tr><td>VIRCHOW</td><td>Histopathology</td><td>VM</td><td>74.2 (13)</td><td>80.2 (10)</td><td>68.5 (15)</td><td>69.2 (2)</td><td>5.5 (20)</td><td>41.0 (6)</td><td>66 (10)</td></tr>
      <tr><td>VIRCHOW2</td><td>Histopathology</td><td>VM</td><td>81.2 (2)</td><td>82.7 (4)</td><td>72.6 (9)</td><td>69.3 (1)</td><td>4.6 (10)</td><td>33.6 (1)</td><td>27 (2)</td></tr>
      <tr><td>CONCH</td><td>Histopathology</td><td>VLM</td><td>77.3 (9)</td><td>80.2 (11)</td><td>73.1 (8)</td><td>68.3 (7)</td><td>4.3 (6)</td><td>55.0 (15)</td><td>56 (7)</td></tr>
      <tr><td>CONCH&nbsp;1.5</td><td>Histopathology</td><td>VLM</td><td>78.6 (7)</td><td>80.8 (9)</td><td>74.6 (5)</td><td>68.8 (5)</td><td>4.9 (14)</td><td>75.3 (23)</td><td>63 (9)</td></tr>
      <tr><td>KEEP</td><td>Histopathology</td><td>VLM</td><td>79.7 (4)</td><td>81.1 (8)</td><td>75.8 (3)</td><td>68.0 (8)</td><td>4.7 (12)</td><td>44.7 (10)</td><td>45 (5)</td></tr>
      <tr><td>MUSK</td><td>Histopathology</td><td>VLM</td><td>75.6 (11)</td><td>79.0 (12)</td><td>70.0 (14)</td><td>65.1 (14)</td><td>4.5 (9)</td><td>69.3 (22)</td><td>82 (13)</td></tr>
      <tr><td>PLIP</td><td>Histopathology</td><td>VLM</td><td>67.8 (19)</td><td>71.0 (22)</td><td>63.4 (17)</td><td>58.5 (22)</td><td>4.9 (15)</td><td>56.9 (16)</td><td>111 (18)</td></tr>
      <tr><td>QUILTNET</td><td>Histopathology</td><td>VLM</td><td>68.3 (17)</td><td>71.0 (21)</td><td>65.7 (16)</td><td>58.9 (21)</td><td>7.0 (23)</td><td>52.7 (13)</td><td>111 (18)</td></tr>
      <tr><td>DINOv2-B</td><td>Natural-image</td><td>VM</td><td>67.9 (18)</td><td>74.8 (17)</td><td>61.0 (18)</td><td>59.8 (19)</td><td>5.5 (21)</td><td>65.8 (20)</td><td>113 (19)</td></tr>
      <tr><td>DINOv2-L</td><td>Natural-image</td><td>VM</td><td>69.6 (16)</td><td>75.3 (16)</td><td>59.2 (19)</td><td>59.6 (20)</td><td>5.3 (17)</td><td>64.5 (19)</td><td>107 (17)</td></tr>
      <tr><td>ViT-B/16</td><td>Natural-image</td><td>VM</td><td>64.4 (21)</td><td>71.9 (19)</td><td>57.8 (21)</td><td>61.0 (17)</td><td>3.9 (3)</td><td>46.8 (12)</td><td>93 (14)</td></tr>
      <tr><td>ViT-L/16</td><td>Natural-image</td><td>VM</td><td>67.5 (20)</td><td>72.8 (18)</td><td>56.5 (22)</td><td>63.1 (16)</td><td>5.0 (16)</td><td>44.1 (8)</td><td>100 (15)</td></tr>
      <tr><td>CLIP-B/32</td><td>Natural-image</td><td>VLM</td><td>61.9 (23)</td><td>65.8 (23)</td><td>53.3 (23)</td><td>56.0 (23)</td><td>5.5 (19)</td><td>60.4 (18)</td><td>129 (20)</td></tr>
      <tr><td>CLIP-L/14</td><td>Natural-image</td><td>VLM</td><td>64.2 (22)</td><td>71.3 (20)</td><td>58.2 (20)</td><td>60.8 (18)</td><td>4.2 (5)</td><td>67.8 (21)</td><td>106 (16)</td></tr>
    </tbody>
  </table>
</div>

---

## 🏆 SPIDER Leaderboard

F1-score on test sets of SPIDER datasets and average across datasets for the *knn* and *linear probing* tasks. The considered datasets are:

* *Br*: [SPIDER-Breast](https://huggingface.co/datasets/histai/SPIDER-breast)
* *Co*: [SPIDER-Colorectal](https://huggingface.co/datasets/histai/SPIDER-colorectal)
* *Sk*: [SPIDER-skin](https://huggingface.co/datasets/histai/SPIDER-skin)
* *Th*: [SPIDER-thorax](https://huggingface.co/datasets/histai/SPIDER-thorax)

<div class="table-responsive-sm">
    <table id="spiderTable" class="table table-hover table-bordered table-sm nowrap">
        <thead class="align-middle text-center">
          <tr>
            <th rowspan="2">Model</th>
            <th rowspan="2">Domain</th>
            <th rowspan="2">Type</th>
            <th colspan="5">KNN &uarr;</th>
            <th colspan="5">Linear probing &uarr;</th>
          </tr>
          <tr>
            <th>Br</th><th>Co</th><th>Sk</th><th>Th</th><th>Avg</th>
            <th>Br</th><th>Co</th><th>Sk</th><th>Th</th><th>Avg</th>
          </tr>
      </thead>
        <tbody>
          <tr><td>HIBOU-B</td><td>Histopathology</td><td>VM</td><td>83.3 (2)</td><td>88.1 (1)</td><td>87.7 (8)</td><td>93.4 (3)</td><td>88.1 (5)</td><td>86.6 (4)</td><td>90.7 (2)</td><td>91.1 (9)</td><td>94.5 (4)</td><td>90.7 (5)</td></tr>
          <tr><td>HIBOU-L</td><td>Histopathology</td><td>VM</td><td>83.6 (1)</td><td>88.1 (1)</td><td>90.7 (3)</td><td>93.5 (2)</td><td>89.0 (1)</td><td>88.0 (1)</td><td>89.8 (8)</td><td>93.3 (2)</td><td>94.1 (6)</td><td>91.3 (1)</td></tr>
          <tr><td>H-OPTIMUS-0</td><td>Histopathology</td><td>VM</td><td>81.7 (6)</td><td>87.8 (3)</td><td>89.3 (5)</td><td>93.8 (1)</td><td>88.2 (4)</td><td>87.2 (2)</td><td>89.9 (7)</td><td>91.9 (6)</td><td>94.4 (5)</td><td>90.8 (4)</td></tr>
          <tr><td>H0-mini</td><td>Histopathology</td><td>VM</td><td>80.9 (9)</td><td>88.0 (2)</td><td>86.2 (11)</td><td>92.8 (6)</td><td>87.0 (8)</td><td>86.0 (7)</td><td>90.2 (6)</td><td>90.4 (12)</td><td>93.4 (11)</td><td>90.0 (9)</td></tr>
          <tr><td>H-OPTIMUS-1</td><td>Histopathology</td><td>VM</td><td>83.0 (3)</td><td>87.8 (3)</td><td>91.1 (2)</td><td>91.5 (13)</td><td>88.3 (3)</td><td>86.1 (6)</td><td>90.3 (5)</td><td>92.3 (4)</td><td>93.6 (10)</td><td>90.6 (6)</td></tr>
          <tr><td>KAIKO--S/16</td><td>Histopathology</td><td>VM</td><td>76.8 (19)</td><td>85.4 (9)</td><td>82.4 (17)</td><td>92.7 (7)</td><td>84.3 (14)</td><td>83.1 (13)</td><td>88.4 (12)</td><td>88.6 (14)</td><td>93.1 (13)</td><td>88.3 (14)</td></tr>
          <tr><td>KAIKO--B/16</td><td>Histopathology</td><td>VM</td><td>77.8 (16)</td><td>85.3 (10)</td><td>82.5 (16)</td><td>92.0 (12)</td><td>84.4 (13)</td><td>81.9 (15)</td><td>88.5 (11)</td><td>87.4 (17)</td><td>93.3 (12)</td><td>87.8 (15)</td></tr>
          <tr><td>MIDNIGHT</td><td>Histopathology</td><td>VM</td><td>77.1 (18)</td><td>84.9 (12)</td><td>85.7 (12)</td><td>92.7 (7)</td><td>85.1 (12)</td><td>86.1 (6)</td><td>89.6 (10)</td><td>91.0 (10)</td><td>94.4 (5)</td><td>90.3 (7)</td></tr>
          <tr><td>OpenMidnight</td><td>Histopathology</td><td>VM</td><td>78.3 (15)</td><td>83.5 (15)</td><td>84.0 (13)</td><td>91.3 (15)</td><td>84.3 (14)</td><td>84.5 (12)</td><td>88.3 (13)</td><td>90.5 (11)</td><td>93.7 (9)</td><td>89.2 (12)</td></tr>
          <tr><td>GenBio-PFM</td><td>Histopathology</td><td>VM</td><td>80.6 (10)</td><td>88.0 (2)</td><td>92.2 (1)</td><td>93.0 (5)</td><td>88.5 (2)</td><td>86.2 (5)</td><td>90.5 (3)</td><td>93.5 (1)</td><td>94.6 (3)</td><td>91.2 (2)</td></tr>
          <tr><td>PHIKON</td><td>Histopathology</td><td>VM</td><td>78.9 (14)</td><td>85.1 (11)</td><td>83.2 (15)</td><td>89.7 (18)</td><td>84.2 (15)</td><td>84.9 (11)</td><td>88.5 (11)</td><td>87.9 (15)</td><td>92.4 (14)</td><td>88.4 (13)</td></tr>
          <tr><td>PHIKON2</td><td>Histopathology</td><td>VM</td><td>80.2 (11)</td><td>86.5 (7)</td><td>83.3 (14)</td><td>91.4 (14)</td><td>85.3 (11)</td><td>86.0 (7)</td><td>89.7 (9)</td><td>87.2 (19)</td><td>94.7 (2)</td><td>89.4 (11)</td></tr>
          <tr><td>GIGAPATH</td><td>Histopathology</td><td>VM</td><td>81.5 (7)</td><td>87.4 (4)</td><td>86.9 (10)</td><td>92.4 (10)</td><td>87.1 (7)</td><td>85.5 (10)</td><td>90.3 (5)</td><td>91.3 (7)</td><td>93.8 (8)</td><td>90.2 (8)</td></tr>
          <tr><td>UNI</td><td>Histopathology</td><td>VM</td><td>81.3 (8)</td><td>88.0 (2)</td><td>87.2 (9)</td><td>91.2 (16)</td><td>86.9 (9)</td><td>85.7 (8)</td><td>90.4 (4)</td><td>91.2 (8)</td><td>93.9 (7)</td><td>90.3 (7)</td></tr>
          <tr><td>UNI2-H</td><td>Histopathology</td><td>VM</td><td>82.6 (4)</td><td>87.1 (6)</td><td>90.5 (4)</td><td>92.5 (9)</td><td>88.2 (4)</td><td>86.7 (3)</td><td>90.5 (3)</td><td>92.5 (3)</td><td>95.1 (1)</td><td>91.2 (2)</td></tr>
          <tr><td>VIRCHOW</td><td>Histopathology</td><td>VM</td><td>79.3 (13)</td><td>87.8 (3)</td><td>88.8 (7)</td><td>92.3 (11)</td><td>87.0 (8)</td><td>86.2 (5)</td><td>90.2 (6)</td><td>91.3 (7)</td><td>94.7 (2)</td><td>90.6 (6)</td></tr>
          <tr><td>VIRCHOW2</td><td>Histopathology</td><td>VM</td><td>82.3 (5)</td><td>88.0 (2)</td><td>89.1 (6)</td><td>92.6 (8)</td><td>88.0 (6)</td><td>87.2 (2)</td><td>90.8 (1)</td><td>92.0 (5)</td><td>93.9 (7)</td><td>91.0 (3)</td></tr>
          <tr><td>CONCH</td><td>Histopathology</td><td>VLM</td><td>75.1 (21)</td><td>84.5 (13)</td><td>81.7 (18)</td><td>91.1 (17)</td><td>83.1 (18)</td><td>82.1 (14)</td><td>87.9 (14)</td><td>87.3 (18)</td><td>91.0 (16)</td><td>87.1 (17)</td></tr>
          <tr><td>CONCH&nbsp;1.5</td><td>Histopathology</td><td>VLM</td><td>75.9 (20)</td><td>84.2 (14)</td><td>83.3 (14)</td><td>91.4 (14)</td><td>83.7 (17)</td><td>81.6 (16)</td><td>87.4 (15)</td><td>87.0 (20)</td><td>92.1 (15)</td><td>87.0 (18)</td></tr>
          <tr><td>KEEP</td><td>Histopathology</td><td>VLM</td><td>79.8 (12)</td><td>87.2 (5)</td><td>87.2 (9)</td><td>93.1 (4)</td><td>86.8 (10)</td><td>85.6 (9)</td><td>89.7 (9)</td><td>89.3 (13)</td><td>93.8 (8)</td><td>89.6 (10)</td></tr>
          <tr><td>MUSK</td><td>Histopathology</td><td>VLM</td><td>77.2 (17)</td><td>85.7 (8)</td><td>82.5 (16)</td><td>91.1 (17)</td><td>84.1 (16)</td><td>80.6 (17)</td><td>87.9 (14)</td><td>87.6 (16)</td><td>93.3 (12)</td><td>87.4 (16)</td></tr>
          <tr><td>PLIP</td><td>Histopathology</td><td>VLM</td><td>69.4 (23)</td><td>79.9 (16)</td><td>74.4 (19)</td><td>86.4 (19)</td><td>77.5 (19)</td><td>77.1 (21)</td><td>84.7 (21)</td><td>82.1 (22)</td><td>88.6 (19)</td><td>83.1 (22)</td></tr>
          <tr><td>QUILTNET</td><td>Histopathology</td><td>VLM</td><td>69.9 (22)</td><td>77.7 (22)</td><td>73.4 (21)</td><td>85.3 (20)</td><td>76.6 (20)</td><td>77.0 (22)</td><td>82.9 (23)</td><td>81.2 (26)</td><td>88.5 (20)</td><td>82.4 (25)</td></tr>
          <tr><td>DINOv2-B</td><td>Natural-image</td><td>VM</td><td>64.0 (29)</td><td>77.5 (23)</td><td>70.4 (26)</td><td>78.1 (25)</td><td>72.5 (26)</td><td>76.0 (24)</td><td>83.9 (22)</td><td>80.1 (27)</td><td>87.6 (24)</td><td>81.9 (27)</td></tr>
          <tr><td>DINOv2-L</td><td>Natural-image</td><td>VM</td><td>66.1 (27)</td><td>79.0 (19)</td><td>71.4 (25)</td><td>78.5 (24)</td><td>73.8 (25)</td><td>74.0 (26)</td><td>85.3 (17)</td><td>82.1 (22)</td><td>87.7 (23)</td><td>82.3 (26)</td></tr>
          <tr><td>ViT-B/16</td><td>Natural-image</td><td>VM</td><td>63.6 (30)</td><td>76.7 (24)</td><td>68.7 (27)</td><td>77.0 (27)</td><td>71.5 (27)</td><td>78.2 (20)</td><td>84.7 (21)</td><td>81.2 (26)</td><td>87.9 (22)</td><td>83.0 (23)</td></tr>
          <tr><td>ViT-L/16</td><td>Natural-image</td><td>VM</td><td>66.5 (26)</td><td>78.7 (21)</td><td>71.8 (24)</td><td>81.8 (21)</td><td>74.7 (23)</td><td>79.3 (18)</td><td>85.1 (18)</td><td>81.3 (25)</td><td>88.5 (20)</td><td>83.5 (20)</td></tr>
          <tr><td>DINOv3-B</td><td>Natural-image</td><td>VM</td><td>65.8 (28)</td><td>78.9 (20)</td><td>73.2 (22)</td><td>80.5 (23)</td><td>74.6 (24)</td><td>76.5 (23)</td><td>84.8 (20)</td><td>81.6 (24)</td><td>90.0 (18)</td><td>83.2 (21)</td></tr>
          <tr><td>DINOv3-L</td><td>Natural-image</td><td>VM</td><td>66.9 (24)</td><td>79.8 (17)</td><td>73.1 (23)</td><td>81.6 (22)</td><td>75.3 (22)</td><td>78.3 (19)</td><td>86.3 (16)</td><td>82.5 (21)</td><td>90.1 (17)</td><td>84.3 (19)</td></tr>
          <tr><td>DINOv3-S</td><td>Natural-image</td><td>VM</td><td>66.8 (25)</td><td>79.5 (18)</td><td>73.9 (20)</td><td>81.6 (22)</td><td>75.5 (21)</td><td>75.0 (25)</td><td>85.0 (19)</td><td>81.8 (23)</td><td>88.2 (21)</td><td>82.5 (24)</td></tr>
          <tr><td>CLIP-B/32</td><td>Natural-image</td><td>VLM</td><td>57.0 (32)</td><td>71.0 (26)</td><td>63.7 (29)</td><td>73.7 (28)</td><td>66.3 (29)</td><td>69.0 (28)</td><td>81.3 (25)</td><td>75.8 (29)</td><td>84.7 (26)</td><td>77.7 (29)</td></tr>
          <tr><td>CLIP-L/14</td><td>Natural-image</td><td>VLM</td><td>62.5 (31)</td><td>74.6 (25)</td><td>66.5 (28)</td><td>77.4 (26)</td><td>70.2 (28)</td><td>73.6 (27)</td><td>82.8 (24)</td><td>78.5 (28)</td><td>86.7 (25)</td><td>80.4 (28)</td></tr>
        </tbody>
    </table>
</div>

---

## 🏆 Zero-shot VLM Classification Leaderboard

F1-score on test sets of all supported datasets and average across datasets for the *zero-shot classification* task. Only VLM models with publicly released patch-level text encoders are included.

<div class="table-responsive-sm">
    <table id="zeroshotTable" class="table table-hover table-bordered table-sm nowrap pivot w-100" style="width:100%">
        <thead class="align-middle text-center">
          <tr>
            <th>Model</th>
            <th>Domain</th>
            <th>Type</th>
            <th>bach</th>
            <th>bracs</th>
            <th>break_his</th>
            <th>ccrcc</th>
            <th>crc</th>
            <th>esca</th>
            <th>mhist</th>
            <th>patch_camelyon</th>
            <th>tcga_crc_msi</th>
            <th>tcga_tils</th>
            <th>tcga_uniform</th>
            <th>wilds</th>
            <th>spider_breast</th>
            <th>spider_colorectal</th>
            <th>spider_skin</th>
            <th>spider_thorax</th>
            <th>Avg</th>
        </tr>
      </thead>
        <tbody>
          <tr><td>CONCH</td><td>Histopathology</td><td>VLM</td><td>56.1 (3)</td><td>37.9 (2)</td><td>53.6 (1)</td><td>56.9 (2)</td><td>51.8 (4)</td><td>40.1 (1)</td><td>60.8 (2)</td><td>57.8 (3)</td><td>21.6 (4)</td><td>47.4 (5)</td><td>37.9 (2)</td><td>83.2 (2)</td><td>30.7 (3)</td><td>31.4 (3)</td><td>35.1 (3)</td><td>43.0 (3)</td><td>46.6 (3)</td></tr>
          <tr><td>KEEP</td><td>Histopathology</td><td>VLM</td><td>63.4 (1)</td><td>34.2 (3)</td><td>45.0 (3)</td><td>69.1 (1)</td><td>80.6 (1)</td><td>33.3 (2)</td><td>41.3 (7)</td><td>71.4 (1)</td><td>15.5 (6)</td><td>55.5 (2)</td><td>44.9 (1)</td><td>89.4 (1)</td><td>37.7 (1)</td><td>44.4 (1)</td><td>60.7 (1)</td><td>51.8 (2)</td><td>52.4 (1)</td></tr>
          <tr><td>MUSK</td><td>Histopathology</td><td>VLM</td><td>62.5 (2)</td><td>38.6 (1)</td><td>52.6 (2)</td><td>50.7 (3)</td><td>57.9 (3)</td><td>25.9 (4)</td><td>63.8 (1)</td><td>53.5 (5)</td><td>22.7 (3)</td><td>50.1 (3)</td><td>32.4 (3)</td><td>71.2 (3)</td><td>36.3 (2)</td><td>36.2 (2)</td><td>48.5 (2)</td><td>55.2 (1)</td><td>47.4 (2)</td></tr>
          <tr><td>PLIP</td><td>Histopathology</td><td>VLM</td><td>42.7 (4)</td><td>25.9 (5)</td><td>25.6 (5)</td><td>38.2 (5)</td><td>61.4 (2)</td><td>31.5 (3)</td><td>53.9 (5)</td><td>46.1 (7)</td><td>16.3 (5)</td><td>64.1 (1)</td><td>10.3 (5)</td><td>51.0 (6)</td><td>14.6 (4)</td><td>28.3 (4)</td><td>23.5 (4)</td><td>22.6 (4)</td><td>34.7 (4)</td></tr>
          <tr><td>QUILTNET</td><td>Histopathology</td><td>VLM</td><td>30.3 (5)</td><td>29.1 (4)</td><td>37.5 (4)</td><td>24.2 (6)</td><td>44.2 (5)</td><td>14.2 (5)</td><td>57.1 (4)</td><td>65.8 (2)</td><td>50.4 (1)</td><td>47.6 (4)</td><td>12.3 (4)</td><td>44.3 (7)</td><td>13.9 (5)</td><td>25.0 (5)</td><td>18.5 (5)</td><td>19.7 (5)</td><td>33.4 (5)</td></tr>
          <tr><td>CLIP-B/32</td><td>Natural-image</td><td>VLM</td><td>13.2 (7)</td><td>7.5 (7)</td><td>18.7 (6)</td><td>21.8 (7)</td><td>24.4 (7)</td><td>9.8 (7)</td><td>42.2 (6)</td><td>48.1 (6)</td><td>13.9 (7)</td><td>21.6 (7)</td><td>2.0 (7)</td><td>56.8 (5)</td><td>3.9 (7)</td><td>6.1 (7)</td><td>4.3 (7)</td><td>5.5 (6)</td><td>18.7 (7)</td></tr>
          <tr><td>CLIP-L/14</td><td>Natural-image</td><td>VLM</td><td>27.1 (6)</td><td>19.2 (6)</td><td>5.8 (7)</td><td>40.6 (4)</td><td>41.1 (6)</td><td>10.4 (6)</td><td>58.0 (3)</td><td>55.6 (4)</td><td>49.4 (2)</td><td>25.4 (6)</td><td>7.4 (6)</td><td>70.2 (4)</td><td>7.3 (6)</td><td>16.0 (6)</td><td>6.6 (6)</td><td>5.4 (7)</td><td>27.8 (6)</td></tr>
        <tbody>
    </table>
</div>

---

## 🏆 Per-dataset linear probing performance

<div class="table-responsive-sm">
    <table id="perDatasetLinearTable" class="table table-hover table-bordered table-sm nowrap w-100">
        <thead class="align-middle text-center">
          <tr>
            <th rowspan="2">Model</th>
            <th rowspan="2">Domain</th>
            <th rowspan="2">Type</th>
            <th colspan="17">Linear probing performance (F1-score) &uarr;</th>
          </tr>
          <tr>
            <th>bach <th>bracs</th><th>break-h</th><th>ccrcc</th><th>crc</th><th>esca</th><th>mhist</th><th>pcam</th><th>tc-crc</th><th>tc-tils</th><th>tc-unif</th><th>wilds</th><th>spi-br</th><th>spi-co</th><th>spi-sk</th><th>spi-th</th><th>Avg</th>
          </tr>
      </thead>
        <tbody>
          <tr><td>HIBOU-B</td><td>Histopathology</td><td>VM</td><td>65.6<br>(20)</td><td>61.7<br>(8)</td><td>59.6<br>(25)</td><td>84.3<br>(16)</td><td>93.9<br>(7)</td><td>77.5<br>(16)</td><td>76.5<br>(30)</td><td>93.4<br>(6)</td><td>66.2<br>(10)</td><td>89.6<br>(11)</td><td>70.2<br>(18)</td><td>97.1<br>(10)</td><td>86.6<br>(4)</td><td>90.7<br>(2)</td><td>91.1<br>(9)</td><td>94.5<br>(4)</td><td>81.2<br>(16)</td></tr>
          <tr><td>HIBOU-L</td><td>Histopathology</td><td>VM</td><td>76.5<br>(8)</td><td>62.7<br>(5)</td><td>69.4<br>(13)</td><td>88.4<br>(11)</td><td>93.0<br>(13)</td><td>77.5<br>(16)</td><td>81.3<br>(14)</td><td>93.3<br>(7)</td><td>68.1<br>(2)</td><td>90.3<br>(7)</td><td>75.2<br>(14)</td><td>98.1<br>(5)</td><td>88.0<br>(1)</td><td>89.8<br>(8)</td><td>93.3<br>(2)</td><td>94.1<br>(6)</td><td>83.7<br>(7)</td></tr>
          <tr><td>H-OPT-0</td><td>Histopathology</td><td>VM</td><td>69.7<br>(15)</td><td>61.1<br>(10)</td><td>66.0<br>(18)</td><td>90.8<br>(6)</td><td>93.5<br>(10)</td><td>83.5<br>(9)</td><td>82.8<br>(5)</td><td>93.0<br>(9)</td><td>67.3<br>(5)</td><td>91.0<br>(2)</td><td>79.3<br>(5)</td><td>98.7<br>(2)</td><td>87.2<br>(2)</td><td>89.9<br>(7)</td><td>91.9<br>(6)</td><td>94.4<br>(5)</td><td>83.8<br>(6)</td></tr>
          <tr><td>H0-mini</td><td>Histopathology</td><td>VM</td><td>71.3<br>(12)</td><td>60.7<br>(11)</td><td>69.0<br>(14)</td><td>90.2<br>(8)</td><td>95.8<br>(1)</td><td>84.4<br>(7)</td><td>79.9<br>(18)</td><td>94.3<br>(2)</td><td>66.5<br>(8)</td><td>91.7<br>(1)</td><td>78.2<br>(9)</td><td>98.2<br>(4)</td><td>86.0<br>(7)</td><td>90.2<br>(6)</td><td>90.4<br>(12)</td><td>93.4<br>(11)</td><td>83.8<br>(6)</td></tr>
          <tr><td>H-OPT-1</td><td>Histopathology</td><td>VM</td><td>72.5<br>(11)</td><td>64.3<br>(2)</td><td>76.0<br>(9)</td><td>91.7<br>(4)</td><td>94.6<br>(4)</td><td>87.1<br>(2)</td><td>82.0<br>(10)</td><td>93.3<br>(7)</td><td>67.9<br>(4)</td><td>91.0<br>(2)</td><td>81.0<br>(3)</td><td>98.2<br>(4)</td><td>86.1<br>(6)</td><td>90.3<br>(5)</td><td>92.3<br>(4)</td><td>93.6<br>(10)</td><td>85.1<br>(3)</td></tr>
          <tr><td>KAIKO-S</td><td>Histopathology</td><td>VM</td><td>72.6<br>(10)</td><td>61.5<br>(9)</td><td>69.4<br>(13)</td><td>84.9<br>(15)</td><td>92.3<br>(16)</td><td>76.8<br>(18)</td><td>81.4<br>(13)</td><td>90.4<br>(16)</td><td>62.6<br>(18)</td><td>90.1<br>(9)</td><td>75.7<br>(12)</td><td>95.9<br>(14)</td><td>83.1<br>(13)</td><td>88.4<br>(12)</td><td>88.6<br>(14)</td><td>93.1<br>(13)</td><td>81.7<br>(14)</td></tr>
          <tr><td>KAIKO-B</td><td>Histopathology</td><td>VM</td><td>69.6<br>(16)</td><td>59.4<br>(15)</td><td>67.2<br>(16)</td><td>81.7<br>(18)</td><td>94.5<br>(5)</td><td>78.5<br>(15)</td><td>78.3<br>(25)</td><td>90.4<br>(16)</td><td>67.0<br>(6)</td><td>90.2<br>(8)</td><td>79.1<br>(6)</td><td>95.6<br>(16)</td><td>81.9<br>(15)</td><td>88.5<br>(11)</td><td>87.4<br>(17)</td><td>93.3<br>(12)</td><td>81.4<br>(15)</td></tr>
          <tr><td>MIDNIGHT</td><td>Histopathology</td><td>VM</td><td>87.9<br>(1)</td><td>63.8<br>(3)</td><td>56.7<br>(26)</td><td>90.8<br>(6)</td><td>95.6<br>(2)</td><td>86.2<br>(4)</td><td>80.2<br>(16)</td><td>93.5<br>(5)</td><td>65.6<br>(12)</td><td>91.0<br>(2)</td><td>85.2<br>(1)</td><td>98.3<br>(3)</td><td>86.1<br>(6)</td><td>89.6<br>(10)</td><td>91.0<br>(10)</td><td>94.4<br>(5)</td><td>84.7<br>(5)</td></tr>
          <tr><td>O-Midnight</td><td>Histopathology</td><td>VM</td><td>84.6<br>(3)</td><td>59.4<br>(15)</td><td>77.3<br>(7)</td><td>92.0<br>(3)</td><td>94.2<br>(6)</td><td>79.8<br>(14)</td><td>81.8<br>(11)</td><td>93.2<br>(8)</td><td>66.3<br>(9)</td><td>91.0<br>(2)</td><td>82.8<br>(2)</td><td>96.5<br>(12)</td><td>84.5<br>(12)</td><td>88.3<br>(13)</td><td>90.5<br>(11)</td><td>93.7<br>(9)</td><td>84.7<br>(5)</td></tr>
          <tr><td>GenBio-PFM</td><td>Histopathology</td><td>VM</td><td>78.1<br>(5)</td><td>60.1<br>(12)</td><td>76.6<br>(8)</td><td>91.6<br>(5)</td><td>95.6<br>(2)</td><td>84.7<br>(6)</td><td>83.2<br>(3)</td><td>93.8<br>(3)</td><td>68.0<br>(3)</td><td>90.6<br>(5)</td><td>79.9<br>(4)</td><td>98.2<br>(4)</td><td>86.2<br>(5)</td><td>90.5<br>(3)</td><td>93.5<br>(1)</td><td>94.6<br>(3)</td><td>85.3<br>(2)</td></tr>
          <tr><td>PHIKON</td><td>Histopathology</td><td>VM</td><td>69.3<br>(17)</td><td>56.9<br>(17)</td><td>60.0<br>(24)</td><td>89.8<br>(9)</td><td>92.1<br>(17)</td><td>76.7<br>(19)</td><td>78.1<br>(26)</td><td>90.9<br>(13)</td><td>63.1<br>(17)</td><td>90.1<br>(9)</td><td>76.6<br>(11)</td><td>97.8<br>(6)</td><td>84.9<br>(11)</td><td>88.5<br>(11)</td><td>87.9<br>(15)</td><td>92.4<br>(14)</td><td>80.9<br>(18)</td></tr>
          <tr><td>PHIKON2</td><td>Histopathology</td><td>VM</td><td>64.7<br>(21)</td><td>58.2<br>(16)</td><td>53.0<br>(28)</td><td>76.7<br>(26)</td><td>92.0<br>(18)</td><td>77.3<br>(17)</td><td>79.2<br>(22)</td><td>90.8<br>(14)</td><td>61.1<br>(20)</td><td>91.0<br>(2)</td><td>77.7<br>(10)</td><td>95.8<br>(15)</td><td>86.0<br>(7)</td><td>89.7<br>(9)</td><td>87.2<br>(19)</td><td>94.7<br>(2)</td><td>79.7<br>(19)</td></tr>
          <tr><td>GIGAPATH</td><td>Histopathology</td><td>VM</td><td>70.7<br>(13)</td><td>62.7<br>(5)</td><td>65.4<br>(20)</td><td>88.1<br>(12)</td><td>94.7<br>(3)</td><td>81.7<br>(12)</td><td>81.7<br>(12)</td><td>93.5<br>(5)</td><td>68.0<br>(3)</td><td>89.1<br>(13)</td><td>74.4<br>(16)</td><td>94.8<br>(17)</td><td>85.5<br>(10)</td><td>90.3<br>(5)</td><td>91.3<br>(7)</td><td>93.8<br>(8)</td><td>82.9<br>(10)</td></tr>
          <tr><td>UNI</td><td>Histopathology</td><td>VM</td><td>73.0<br>(9)</td><td>59.4<br>(15)</td><td>70.8<br>(12)</td><td>90.7<br>(7)</td><td>93.1<br>(12)</td><td>83.4<br>(10)</td><td>82.4<br>(8)</td><td>93.8<br>(3)</td><td>65.9<br>(11)</td><td>90.1<br>(9)</td><td>75.3<br>(13)</td><td>97.2<br>(9)</td><td>85.7<br>(8)</td><td>90.4<br>(4)</td><td>91.2<br>(8)</td><td>93.9<br>(7)</td><td>83.5<br>(8)</td></tr>
          <tr><td>UNI2-H</td><td>Histopathology</td><td>VM</td><td>84.7<br>(2)</td><td>65.4<br>(1)</td><td>78.4<br>(4)</td><td>89.5<br>(10)</td><td>93.9<br>(7)</td><td>86.4<br>(3)</td><td>78.6<br>(23)</td><td>95.0<br>(1)</td><td>66.9<br>(7)</td><td>90.4<br>(6)</td><td>78.8<br>(7)</td><td>98.9<br>(1)</td><td>86.7<br>(3)</td><td>90.5<br>(3)</td><td>92.5<br>(3)</td><td>95.1<br>(1)</td><td>85.7<br>(1)</td></tr>
          <tr><td>VIRCHOW</td><td>Histopathology</td><td>VM</td><td>66.2<br>(19)</td><td>59.8<br>(14)</td><td>62.7<br>(22)</td><td>91.7<br>(4)</td><td>93.7<br>(9)</td><td>84.3<br>(8)</td><td>82.3<br>(9)</td><td>93.6<br>(4)</td><td>65.5<br>(13)</td><td>90.7<br>(4)</td><td>74.8<br>(15)</td><td>97.6<br>(7)</td><td>86.2<br>(5)</td><td>90.2<br>(6)</td><td>91.3<br>(7)</td><td>94.7<br>(2)</td><td>82.8<br>(11)</td></tr>
          <tr><td>VIRCHOW2</td><td>Histopathology</td><td>VM</td><td>76.5<br>(8)</td><td>62.4<br>(6)</td><td>72.5<br>(11)</td><td>93.6<br>(1)</td><td>93.0<br>(13)</td><td>88.9<br>(1)</td><td>83.6<br>(2)</td><td>92.8<br>(10)</td><td>69.6<br>(1)</td><td>90.9<br>(3)</td><td>78.4<br>(8)</td><td>90.0<br>(26)</td><td>87.2<br>(2)</td><td>90.8<br>(1)</td><td>92.0<br>(5)</td><td>93.9<br>(7)</td><td>84.8<br>(4)</td></tr>
          <tr><td>CONCH</td><td>Histopathology</td><td>VLM</td><td>84.4<br>(4)</td><td>60.0<br>(13)</td><td>68.8<br>(15)</td><td>88.1<br>(12)</td><td>93.4<br>(11)</td><td>80.1<br>(13)</td><td>79.7<br>(20)</td><td>90.6<br>(15)</td><td>64.4<br>(15)</td><td>88.1<br>(14)</td><td>68.0<br>(20)</td><td>97.2<br>(9)</td><td>82.1<br>(14)</td><td>87.9<br>(14)</td><td>87.3<br>(18)</td><td>91.0<br>(16)</td><td>81.9<br>(13)</td></tr>
          <tr><td>CONCH&nbsp;1.5</td><td>Histopathology</td><td>VLM</td><td>76.8<br>(7)</td><td>62.4<br>(6)</td><td>75.3<br>(10)</td><td>87.4<br>(13)</td><td>93.8<br>(8)</td><td>82.7<br>(11)</td><td>81.2<br>(15)</td><td>91.4<br>(12)</td><td>62.3<br>(19)</td><td>89.9<br>(10)</td><td>69.4<br>(19)</td><td>96.7<br>(11)</td><td>81.6<br>(16)</td><td>87.4<br>(15)</td><td>87.0<br>(20)</td><td>92.1<br>(15)</td><td>82.4<br>(12)</td></tr>
          <tr><td>KEEP</td><td>Histopathology</td><td>VLM</td><td>77.0<br>(6)</td><td>62.2<br>(7)</td><td>65.9<br>(19)</td><td>93.2<br>(2)</td><td>94.7<br>(3)</td><td>85.8<br>(5)</td><td>76.8<br>(29)</td><td>92.6<br>(11)</td><td>64.9<br>(14)</td><td>89.9<br>(10)</td><td>72.7<br>(17)</td><td>97.4<br>(8)</td><td>85.6<br>(9)</td><td>89.7<br>(9)</td><td>89.3<br>(13)</td><td>93.8<br>(8)</td><td>83.2<br>(9)</td></tr>
          <tr><td>MUSK</td><td>Histopathology</td><td>VLM</td><td>69.9<br>(14)</td><td>63.3<br>(4)</td><td>77.6<br>(6)</td><td>85.3<br>(14)</td><td>91.1<br>(21)</td><td>76.4<br>(20)</td><td>80.0<br>(17)</td><td>89.4<br>(17)</td><td>63.2<br>(16)</td><td>89.4<br>(12)</td><td>66.0<br>(21)</td><td>96.0<br>(13)</td><td>80.6<br>(17)</td><td>87.9<br>(14)</td><td>87.6<br>(16)</td><td>93.3<br>(12)</td><td>81.1<br>(17)</td></tr>
          <tr><td>PLIP</td><td>Histopathology</td><td>VLM</td><td>63.9<br>(23)</td><td>56.5<br>(19)</td><td>47.2<br>(29)</td><td>76.9<br>(25)</td><td>88.2<br>(27)</td><td>65.7<br>(28)</td><td>78.5<br>(24)</td><td>87.9<br>(20)</td><td>56.0<br>(28)</td><td>87.2<br>(16)</td><td>54.9<br>(25)</td><td>89.0<br>(27)</td><td>77.1<br>(21)</td><td>84.7<br>(21)</td><td>82.1<br>(22)</td><td>88.6<br>(19)</td><td>74.0<br>(27)</td></tr>
          <tr><td>QUILTNET</td><td>Histopathology</td><td>VLM</td><td>58.4<br>(26)</td><td>55.9<br>(21)</td><td>62.4<br>(23)</td><td>65.5<br>(29)</td><td>92.5<br>(15)</td><td>61.5<br>(30)</td><td>73.5<br>(31)</td><td>87.4<br>(21)</td><td>59.6<br>(21)</td><td>87.0<br>(17)</td><td>54.1<br>(27)</td><td>94.7<br>(18)</td><td>77.0<br>(22)</td><td>82.9<br>(23)</td><td>81.2<br>(26)</td><td>88.5<br>(20)</td><td>73.9<br>(28)</td></tr>
          <tr><td>DINOv2-B</td><td>Natural-image</td><td>VM</td><td>64.4<br>(22)</td><td>52.9<br>(25)</td><td>77.8<br>(5)</td><td>79.7<br>(22)</td><td>90.3<br>(24)</td><td>73.8<br>(22)</td><td>82.6<br>(7)</td><td>86.3<br>(24)</td><td>58.6<br>(24)</td><td>85.9<br>(20)</td><td>54.4<br>(26)</td><td>90.7<br>(24)</td><td>76.0<br>(24)</td><td>83.9<br>(22)</td><td>80.1<br>(27)</td><td>87.6<br>(24)</td><td>76.6<br>(24)</td></tr>
          <tr><td>DINOv2-L</td><td>Natural-image</td><td>VM</td><td>68.9<br>(18)</td><td>50.6<br>(27)</td><td>78.5<br>(3)</td><td>81.4<br>(20)</td><td>90.7<br>(22)</td><td>72.1<br>(25)</td><td>82.3<br>(9)</td><td>87.2<br>(22)</td><td>59.3<br>(22)</td><td>85.9<br>(20)</td><td>56.2<br>(23)</td><td>90.3<br>(25)</td><td>74.0<br>(26)</td><td>85.3<br>(17)</td><td>82.1<br>(22)</td><td>87.7<br>(23)</td><td>77.0<br>(23)</td></tr>
          <tr><td>ViT-B</td><td>Natural-image</td><td>VM</td><td>57.0<br>(28)</td><td>56.6<br>(18)</td><td>64.5<br>(21)</td><td>79.1<br>(23)</td><td>90.6<br>(23)</td><td>62.7<br>(29)</td><td>77.6<br>(27)</td><td>84.6<br>(27)</td><td>59.1<br>(23)</td><td>85.8<br>(21)</td><td>53.4<br>(29)</td><td>91.3<br>(23)</td><td>78.2<br>(20)</td><td>84.7<br>(21)</td><td>81.2<br>(26)</td><td>87.9<br>(22)</td><td>74.7<br>(26)</td></tr>
          <tr><td>ViT-L</td><td>Natural-image</td><td>VM</td><td>56.9<br>(29)</td><td>54.8<br>(23)</td><td>66.3<br>(17)</td><td>77.1<br>(24)</td><td>92.8<br>(14)</td><td>67.9<br>(26)</td><td>79.8<br>(19)</td><td>85.7<br>(25)</td><td>56.8<br>(27)</td><td>87.5<br>(15)</td><td>55.9<br>(24)</td><td>92.6<br>(22)</td><td>79.3<br>(18)</td><td>85.1<br>(18)</td><td>81.3<br>(25)</td><td>88.5<br>(20)</td><td>75.5<br>(25)</td></tr>
          <tr><td>CLIP-B</td><td>Natural-image</td><td>VLM</td><td>51.1<br>(31)</td><td>52.4<br>(26)</td><td>40.0<br>(30)</td><td>73.7<br>(28)</td><td>87.3<br>(28)</td><td>61.0<br>(31)</td><td>77.5<br>(28)</td><td>82.7<br>(28)</td><td>49.0<br>(31)</td><td>83.8<br>(23)</td><td>47.9<br>(30)</td><td>83.5<br>(28)</td><td>69.0<br>(28)</td><td>81.3<br>(25)</td><td>75.8<br>(29)</td><td>84.7<br>(26)</td><td>68.8<br>(30)</td></tr>
          <tr><td>CLIP-L</td><td>Natural-image</td><td>VLM</td><td>63.5<br>(24)</td><td>56.4<br>(20)</td><td>54.5<br>(27)</td><td>75.9<br>(27)</td><td>88.3<br>(26)</td><td>67.6<br>(27)</td><td>79.6<br>(21)</td><td>85.6<br>(26)</td><td>52.0<br>(30)</td><td>85.0<br>(22)</td><td>54.1<br>(27)</td><td>93.2<br>(21)</td><td>73.6<br>(27)</td><td>82.8<br>(24)</td><td>78.5<br>(28)</td><td>86.7<br>(25)</td><td>73.6<br>(29)</td></tr>
          <tr><td>DINOv3-B</td><td>Natural-image</td><td>VM</td><td>60.3<br>(25)</td><td>55.4<br>(22)</td><td>81.8<br>(2)</td><td>80.7<br>(21)</td><td>89.5<br>(25)</td><td>72.9<br>(23)</td><td>82.7<br>(6)</td><td>88.0<br>(19)</td><td>57.2<br>(26)</td><td>86.7<br>(18)</td><td>56.2<br>(23)</td><td>93.6<br>(20)</td><td>76.5<br>(23)</td><td>84.8<br>(20)</td><td>81.6<br>(24)</td><td>90.0<br>(18)</td><td>77.4<br>(21)</td></tr>
          <tr><td>DINOv3-L</td><td>Natural-image</td><td>VM</td><td>57.9<br>(27)</td><td>54.6<br>(24)</td><td>77.3<br>(7)</td><td>82.5<br>(17)</td><td>91.5<br>(19)</td><td>76.0<br>(21)</td><td>84.1<br>(1)</td><td>88.8<br>(18)</td><td>55.5<br>(29)</td><td>87.0<br>(17)</td><td>59.3<br>(22)</td><td>94.8<br>(17)</td><td>78.3<br>(19)</td><td>86.3<br>(16)</td><td>82.5<br>(21)</td><td>90.1<br>(17)</td><td>77.9<br>(20)</td></tr>
          <tr><td>DINOv3-S</td><td>Natural-image</td><td>VM</td><td>56.4<br>(30)</td><td>56.5<br>(19)</td><td>82.9<br>(1)</td><td>81.6<br>(19)</td><td>91.4<br>(20)</td><td>72.6<br>(24)</td><td>82.9<br>(4)</td><td>86.5<br>(23)</td><td>57.7<br>(25)</td><td>86.3<br>(19)</td><td>53.9<br>(28)</td><td>94.1<br>(19)</td><td>75.0<br>(25)</td><td>85.0<br>(19)</td><td>81.8<br>(23)</td><td>88.2<br>(21)</td><td>77.1<br>(22)</td></tr>
        <tbody>
    </table>
</div>
