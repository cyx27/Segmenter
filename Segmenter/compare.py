from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

# 比较keyword和texts（各一篇文书）
def compare(keyword,text):
    # 文本集和搜索词
    #wenshus = wenshu_requests.getData("李亚飞", 2, "2016-01-01", "2021-12-30", person="李亚飞")[0:-1].split('@')
    #keyword = wenshus[0]
    texts = ['']
    #print(keyword)
    texts.append(text)
    # 1、将【文本集】生成【分词列表】
    texts = [lcut(text) for text in texts]
    #print(texts)
    # 2、基于文本集建立【词典】，并获得
    # 词典特征数
    dictionary = Dictionary(texts)
    num_features = len(dictionary.token2id)
    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
    kw_vector = dictionary.doc2bow(lcut(keyword))
    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tfidf = TfidfModel(corpus)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
    tf_kw = tfidf[kw_vector]
    # 6、相似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    count=0
    for e, s in enumerate(similarities, 1):
        if count==0:
            count+=1
            continue
        print('kw 与 text%d 相似度为：%f' % (e, s))
        return s
