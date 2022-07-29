# Movie Recommendation
Using Matrix Factorization for movie recommendationvusing MovieLens 1 million movie rewiews dataset. https://grouplens.org/datasets/movielens/1m/

I have used matrix factorization based prediction method because it is easy to scale to massive data sets. When we use a distance based prediction method we run into the risk of overfitting ratings matrix. 

In this project I performed matrix factorization usinf SVD(Singular Value Decomposition) which is used to break down a matrix R into lower ranks. It mathematically decomposes R into two unitary matrices and a diagonal matrix. R = U.Σ.Vt where R is user ratings matrix, U is user 'Features' matrix, sigma is the diagonal matrix of singular values and vt represents the movies feature matrix.
