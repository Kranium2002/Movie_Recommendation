#%%
import pandas as pd;
import numpy as np;
# %%

ratings = [i.strip().split("::") for i in open(r"D:\Projects\Movie_Prediction\ml-1m\ratings.dat",'r').readlines()]
users = [i.strip().split("::") for i in open(r"D:\Projects\Movie_Prediction\ml-1m\users.dat",'r').readlines()]
movies = [i.strip().split("::") for i in open(r"D:\Projects\Movie_Prediction\ml-1m\movies.dat",'r').readlines()]

ratings_df = pd.DataFrame(ratings, columns = ['UserID','MovieID','Rating','Timestamp'])
movies_df = pd.DataFrame(movies, columns = ['MovieID','Title','Genres'])
movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric)

# %%
movies_df.head()

# %%
ratings_df.head()
ratings_df = ratings_df.apply(pd.to_numeric)
# %%
R_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)

# %%
R_df

# %%
R = R_df.to_numpy()
user_ratings_mean = np.mean(R,axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)

# %%
from scipy.sparse.linalg import svds
U, sigma, Vt = svds(R_demeaned, k = 50)
sigma
#%%
sigma = np.diag(sigma)
sigma
# %%
all_pred_ratings = np.dot(np.dot(U,sigma),Vt)+user_ratings_mean.reshape(-1,1)
pred_df = pd.DataFrame(all_pred_ratings,columns = R_df.columns)

# %%
def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.UserID == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'MovieID', right_on = 'MovieID').sort_values(['Rating'], ascending=False))

    print ('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print ('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['MovieID'].isin(user_full['MovieID'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'MovieID',
               right_on = 'MovieID').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations

already_rated, predictions = recommend_movies(pred_df, 1, movies_df, ratings_df, 10)
#%%
already_rated.head(10)
# %%
