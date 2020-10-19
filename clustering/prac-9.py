# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# Nạp các gói thư viện cần thiết
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ### 1. Chuẩn bị dữ liệu

# Đọc dữ liệu từ tập tin csv
# df = pd.read_csv('https://raw.githubusercontent.com/ltdaovn/dataset/master/flowers.csv')
df = pd.read_csv('datasets/flowers.csv')
X = df.iloc[:, :].values


clusters = []

for i in range(1, 10):
    km = KMeans(n_clusters=i).fit(X)
    # inertia: tổng bình phương khoảng cách của các mẫu đến trung tâm cụm gần gần của chúng
    clusters.append(km.inertia_)

# fig, ax = plt.subplots(figsize=(8, 6))
# sns.lineplot(x=list(range(1, 10)), y=clusters, ax=ax)
# ax.set_title('Đồ thị Elbow')
# ax.set_xlabel('Số lượng nhóm')
# ax.set_ylabel('Giá trị Inertia')
# plt.show()


# Qua đồ thị trên, chúng ta thấy số lượng clusters thích hợp từ 2->4
# ==> Chọn 3 clusters
# Sử dụng TSNE
# Giảm chiều dữ liệu từ 4 -> 2
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(X)
X_ = tsne_results

# ### 2. Thiết lập kích thước figure

plt.rcParams['figure.figsize'] = (14, 7)

# ### 3. Tiến hành gom nhóm
# 3.1 Sử dụng **KMEANS**

km3 = KMeans(n_clusters=3, random_state=2020)
y_label = km3.fit_predict(X) + 1
# Vẽ biểu đồ
plt.subplot(2, 2, 1)
sns.scatterplot(X_[:, 0], X_[:, 1],
                hue=y_label,
                palette=sns.color_palette('hls', 3))
plt.title('KMeans with 3 Clusters')
print('Nhóm 1:', len(y_label[y_label == 1]))
print('Nhóm 2:', len(y_label[y_label == 2]))
print('Nhóm 3:', len(y_label[y_label == 3]))

# 3.2. Sử dụng giải thuật **Agglomerative Hierarchical Clustering**

agglom = AgglomerativeClustering(n_clusters=3, linkage='average')
y_label = agglom.fit_predict(X) + 1
# Vẽ biểu đồ
# X['Labels'] = agglom.labels_
plt.subplot(2, 2, 2)
sns.scatterplot(X_[:, 0], X_[:, 1],
                hue=y_label,
                palette=sns.color_palette('hls', 3))
plt.title('Agglomerative with 3 Clusters')
print('Nhóm 1:', len(y_label[y_label == 1]))
print('Nhóm 2:', len(y_label[y_label == 2]))
print('Nhóm 3:', len(y_label[y_label == 3]))

# 3.3. Sử dụng giải thuật **DBSCAN**

db = DBSCAN(eps=11, min_samples=6)
y_label = db.fit_predict(X)

plt.subplot(2, 2, 3)
sns.scatterplot(X_[:, 0], X_[:, 1],
                hue=y_label,
                palette=sns.color_palette('hls', np.unique(db.labels_).shape[0]))
plt.title('DBSCAN with epsilon 11, min samples 6')

# 3.4. Sử dụng giải thuật **MeanShift**

bandwidth = estimate_bandwidth(X, quantile=0.1)
ms = MeanShift(bandwidth).fit(X)
y_label = ms.fit_predict(X)

plt.title('DBSCAN with epsilon 11, min samples 6')
plt.subplot(2, 2, 4)
labels = np.unique(ms.labels_)
sns.scatterplot(X_[:, 0], X_[:, 1],
                hue=y_label,
                style=y_label,
                s=60,
                palette=sns.color_palette('hls', np.unique(ms.labels_).shape[0]))
plt.title('MeanShift')
# plt.show()

# ### 4. Hiển thị đồ thị

plt.tight_layout()
# plt.show()
# prac-9.py to display 4 figures in one


plt.savefig('figure9.png', dpi=500)
plt.axis('off')
