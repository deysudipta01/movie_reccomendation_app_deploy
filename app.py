from flask import Flask ,request, render_template
import pickle
import requests
import pandas as pd
#from PIL import Image

# movies = pickle.load(open('model/movie_dict.pkl'),'rb')
movies_=pickle.load(open('model/new_movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_)
similarity = pickle.load(open('model/new_similarity.pkl','rb'))

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")










def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=0a172a3f349c894da20f50c090440bfe&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']




def recommend(movie):
    index= movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster = []
    for i in distances[1:11]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return    recommended_movies_name, recommended_movies_poster

@app.route("/newpage")
def newpage():
    return render_template("newpage.html")

@app.route("/recommendation",methods=['GET','POST'])
def recommendation():
    movie_list=movies['title'].values
    status=False
    if request.method=='POST':
        try:
            if request.form:
                movies_name=request.form['movies']
                # print movies name
                recommended_movies_name , recommended_movies_poster =recommend(movies_name)
                status=True

                return render_template("prediction.html",movies_name=recommended_movies_name,poster=recommended_movies_poster,movie_list=movie_list,status=status)



        except Exception as e:
            error={'error':e}
            return render_template("prediction.html",error=error,movie_list=movie_list,status=status)

    else:
        return render_template("prediction.html",movie_list=movie_list,status=status)




if __name__=='__main__':
    app.debug=True
    app.run()