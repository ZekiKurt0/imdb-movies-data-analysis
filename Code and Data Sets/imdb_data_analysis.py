import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob 
import random

#                                                       MERGE CSV FILES WTIH DROP DUPLICATES(movie_id)


files_list = ["action.csv","adventure.csv","animation.csv","biography.csv","crime.csv","family.csv","fantasy.csv","film-noir.csv","history.csv","horror.csv","mystery.csv","romance.csv","scifi.csv","sports.csv","thriller.csv","war.csv"]

reading_csv = (pd.read_csv(files) for files in files_list)
all_movies = pd.concat(reading_csv,ignore_index=True).drop_duplicates(subset=["movie_id","movie_name"])   

all_movies = pd.DataFrame(all_movies)


all_movies=all_movies.drop(columns=["certificate","gross(in $)"])        

all_movies=all_movies.dropna(subset=["rating"])

all_movies=all_movies.dropna(subset=["year"])

# YEAR
all_movies = all_movies[~all_movies.year.str.contains("II", na=False)]
all_movies = all_movies[~all_movies.year.str.contains("I", na=False)]
all_movies["year"] = pd.to_numeric(all_movies["year"], errors="coerce")
all_movies = all_movies.dropna(subset=["year"])
all_movies["year"] = all_movies["year"].astype(int)

# RUNTİME

all_movies.runtime = all_movies.runtime.str.replace("min","")
all_movies.runtime = all_movies.runtime.str.replace(",","")
all_movies.runtime = all_movies.runtime.fillna("93")
all_movies.runtime = all_movies.runtime.astype("int64")
all_movies.runtime = all_movies.runtime.replace(5538,138)



# GENRE

random.seed(42)      
all_movies=all_movies.reset_index(drop=True)    # repair index
all_movies.genre=all_movies.genre.str.split(",")
for i in all_movies.index:
    genre_list = all_movies.at[i, 'genre'] 
    chosen_genre = random.choice(genre_list).strip()  
    all_movies.at[i, 'genre'] = chosen_genre 
all_movies = all_movies[~all_movies["genre"].isin(["Adult","Reality-TV","News"])]    # REMOVED 3 GENRE BECAUSE THEY HAD FEW MOVIES

# ratıng

" ıts okey  we dont need to edit"



# description
all_movies.description = all_movies["description"].str.replace("Add a Plot","No description")


# director and director_id

all_movies = all_movies.dropna(subset=["director"])


#star and star_id
all_movies = all_movies.dropna(subset=["star"])




# votes
"its okey we dont need to edit"

#-------------------------------------------------------------------- DATA ANALYSİS AND VISULATION-----------------------------------------------------------------------------------------------------------





#                                                            THE PIE CHART OF TOTAL NUMBER OF MOVIES BY GENRES

the_total_movies_by_genre=all_movies.movie_id.groupby(all_movies.genre).count()

"""
the_total_movies_by_genre.plot(kind="pie",figsize=(16,9),autopct='%1.1f%%', pctdistance=0.85, startangle=140,textprops={'fontweight': 'bold'})
plt.title("THE MOVIES BY GENRE(1894-2023)",fontdict={'family':"DejaVu Sans"},weight="bold")
plt.xticks(weight="bold",fontfamily="DejaVu Sans")
plt.ylabel("Genres",weight="bold")  
plt.axis('equal')
plt.show()"""




the_average_rating_of_movies_by_genres=all_movies.rating.groupby(all_movies.genre).mean()


all_movies["evaluation"] = pd.cut(all_movies["rating"],bins=[0,2.0,4.0,6.0,8.0,10.0],labels=["Awful(0-2.0)","Bad(2.0-4.0)","Medium(4.0-6.0)","Good(6.0-8.0)","Perfect(8.0-10.0)"])



#                                       THE RATING DISTRIBUTION OF EACH GENRES
"""
the_evaluations_rating_by_genres = all_movies.groupby(['genre','evaluation']).size().unstack(fill_value=0)
colors =  ["#8B0000", "#E74C3C", "#F39C12", "#2E8B57", "#1F618D"]
the_evaluations_rating_by_genres.plot(kind='barh',
                                      figsize=(16,9),
                                      stacked=True,
                                      color=colors[:the_evaluations_rating_by_genres.shape[1]],
                                      alpha = 0.9)

plt.title('Rating distribution of each genres(1894-2023)'.upper(), fontsize=16,weight="bold",fontfamily="DejaVu Sans")
plt.xlabel('Number of Movies', fontsize=12,weight="bold",fontfamily="DejaVu Sans")
plt.ylabel('Genres', fontsize=12,weight="bold",fontfamily="DejaVu Sans")
plt.legend(title='Evaluation', title_fontsize=10,)
plt.xticks(rotation=90,weight="bold",fontfamily="DejaVu Sans",fontsize=10)
plt.yticks(weight="bold",fontfamily="DejaVu Sans")
plt.grid(False)
plt.tight_layout()
plt.show()"""




#                                TOP 40 DIRECTOR(BY NUMBER OF MOVIES) AND THEIR AVERAGE RATING
top_directors_count = all_movies.director.value_counts().head(40)
top_directors = all_movies[all_movies.director.isin(top_directors_count.index)]
average_ratings = top_directors.groupby("director")["rating"].mean()
"""
director_stats = pd.DataFrame({
    "Film Count": top_directors_count, 
    "Average Rating": average_ratings
}).sort_values("Film Count", ascending=True)

plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax1 = plt.subplots(figsize=(16, 9))
sns.set_style("whitegrid")
color1, color2 = "royalblue", "crimson"
ax1.barh(director_stats.index, director_stats["Film Count"], color=color1, alpha=0.7, label="Film Count")
ax1.set_xlabel("Film Count", color=color1, fontsize=12,weight="bold")
ax1.tick_params(axis="x", labelcolor=color1)
ax1.set_yticklabels(director_stats.index, fontweight="bold", fontsize=10)  # İsimleri kalın yap
ax2 = ax1.twiny()
ax2.plot(director_stats["Average Rating"], director_stats.index, color=color2, marker="o", label="Average Rating", linewidth=2)
ax2.set_xlabel("Average Rating", color=color2, fontsize=12,weight="bold")
ax2.tick_params(axis="x", labelcolor=color2)
plt.title("Top 40 Directors: Film Count & Average Rating(1894-2023)", fontsize=18, fontweight="bold")
ax1.legend(loc="lower right")
ax2.legend(loc="upper right")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()"""



#                                               TOP 40 MOVIES(BY VOTES) AND THEIR RAITNG

top_movies_by_votes = all_movies.sort_values(by="votes", ascending=False)[["movie_name","votes","rating"]].head(40)

"""
top_movies_by_votes["short_name"] = top_movies_by_votes["movie_name"].apply(lambda x: x[:24] + "..." if len(x) > 24 else x)
plt.figure(figsize=(25, 15))
sns.set_style("whitegrid")
ax = sns.barplot(data=top_movies_by_votes, y="short_name", x="votes", color="royalblue", label="Votes")
ax2 = ax.twiny()
sns.scatterplot(data=top_movies_by_votes, x="rating", y="short_name", color="red", s=80, ax=ax2, label="Rating")
ax.set_xlabel("Votes", fontsize=12, fontweight="bold", fontfamily="DejaVu Sans")
ax.set_ylabel("Movie Name", fontsize=12, fontweight="bold", fontfamily="DejaVu Sans")
ax2.set_xlabel("Rating", fontsize=12, fontweight="bold", fontfamily="DejaVu Sans", color="red")
ax2.xaxis.label.set_color("red")
ax2.tick_params(axis='x', colors='red')
ax.set_yticklabels(ax.get_yticklabels(), fontweight="bold", fontfamily="DejaVu Sans",fontsize=10,ha="right")
ax.set_xticks(range(0,2700000,500000),[f'{y:,}' for y in range(0,2700000,500000)])
ax.set_xticklabels(ax.get_xticklabels(),fontweight="bold",fontfamily="DejaVu Sans",)
plt.title("Top 40 Movies(by Votes) & Ratings(1894-2023)".upper(), fontsize=15, fontweight="bold", fontfamily="DejaVu Sans")
ax.legend(loc="lower right")
ax2.legend(loc="upper right")
plt.show()"""




#                               TOTAL MOVIE DISTRIBUION OVER YEAR 

"""
plt.figure(figsize=(16,9))
sns.histplot(all_movies["year"], bins=30, kde=True, color="green")
plt.xlabel("Year", fontname="DejaVu Sans", fontsize=12, fontweight="bold")
plt.ylabel("Number of Movies", fontname="DejaVu Sans", fontsize=12, fontweight="bold")
plt.title("Movie Distribution Over the Years(1894-2023)", fontname="DejaVu Sans", fontsize=18, fontweight="bold")
plt.xticks(fontname="DejaVu Sans", fontsize=10, fontweight="bold")
plt.yticks(fontname="DejaVu Sans", fontsize=10, fontweight="bold")
plt.show()"""

#                                                 THE AVERAGE DURATIONS OF MOVIES BY GENRES
the_average_durations_by_genres=all_movies.runtime.groupby(all_movies.genre).mean().sort_values(ascending=False)
"""
plt.figure(figsize=(16, 9))
ax = sns.barplot(y=the_average_durations_by_genres.index, x=the_average_durations_by_genres.values, hue=the_average_durations_by_genres.index, palette="viridis", legend=False)
for i, v in enumerate(the_average_durations_by_genres.values):
    ax.text(v, i, f'{v:.1f}', va='center', fontweight='bold', fontfamily='DejaVu Sans')
plt.xlabel("Duration (minute)", fontweight="bold", fontfamily="DejaVu Sans")
plt.ylabel("Genres", fontweight="bold", fontfamily="DejaVu Sans")
plt.xticks(fontweight="bold", fontfamily="DejaVu Sans")
plt.yticks(fontweight="bold", fontfamily="DejaVu Sans")
plt.title("AVERAGE DURATIONS OF MOVIES BY GENRES", fontweight="bold", fontfamily="DejaVu Sans")
plt.show()"""



# HEAT MAP
"""
suitable_subset=all_movies[["runtime","rating","votes","year"]]
plt.figure(figsize=(16,9))
corr=suitable_subset.corr()
sns.heatmap(corr,annot=True)
plt.title("HEAT MAP",weight="bold",fontfamily="DejaVu Sans")
plt.xticks(weight="bold",family="DejaVu Sans")
plt.yticks(weight="bold",family="DejaVu Sans")
plt.show()"""


#                                                   TOP 50 YEAR(BY VOTES) AND AVERAGE RATING

the_total_votes_by_years = all_movies["votes"].groupby(all_movies["year"]).sum().sort_values(ascending=False).head(50)
filtered_movies = all_movies[all_movies["year"].isin(the_total_votes_by_years.index)]
average_rating = filtered_movies.groupby("year")["rating"].mean()
"""
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(16, 9))
color1 = "royalblue"
ax1.bar(the_total_votes_by_years.index, the_total_votes_by_years.values, color=color1, alpha=0.6, label="Total Number of Votes")
ax1.set_xlabel("Year", fontsize=12, fontweight="bold", fontfamily="DejaVu Sans")
ax1.set_ylabel("Total Number of Votes", fontsize=12, color=color1, fontweight="bold", fontfamily="DejaVu Sans")
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_yticks(range(0, 40000000, 10000000), [f'{y:,}' for y in range(0, 40000000, 10000000)], fontweight="bold")
ax1.set_yticklabels(ax1.get_yticklabels(), fontweight="bold", fontfamily="DejaVu Sans")
ax1.set_xticklabels(ax1.get_xticklabels(), fontweight="bold", fontfamily="DejaVu Sans")

ax2 = ax1.twinx()
color2 = "red"
ax2.plot(average_rating.index, average_rating.values, color=color2, marker="o", linewidth=2, markersize=6, label="Average Rating")
ax2.set_ylabel("Average Rating", fontsize=12, color=color2, fontweight="bold", fontfamily="DejaVu Sans")
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_yticklabels(ax2.get_yticklabels(), fontweight="bold", fontfamily="DejaVu Sans")

plt.title("TOP 50 YEAR(BY VOTES) AND AVERAGE RATING", fontsize=18, fontweight="bold", fontfamily="DejaVu Sans")
fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.9), prop={"weight": "bold", "family": "DejaVu Sans"})
plt.show()"""





top_year_by_movie = all_movies.movie_id.groupby(all_movies.year).count().sort_values(ascending=False).head(50).sort_index(ascending=False)


#                                                          TOP 50 YEAR BY  NUMBER OF MOVIE
"""
plt.style.use("ggplot")
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(16, 9))
top_year_by_movie.plot(kind="barh", ax=ax, color=sns.color_palette("Set2", len(top_year_by_movie)))
ax.set_title("Number of Movies by Year(Top 50 1894-2023)".upper(), fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Number of Movies", fontsize=12, fontweight="bold")
ax.set_ylabel("Year", fontsize=12, fontweight="bold")
ax.tick_params(axis="both", labelsize=11)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight("bold")
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.xaxis.grid(True, linestyle="--", alpha=0.7)
for bar in ax.patches:
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', 
            va='center', ha='left', fontsize=10, fontweight="bold")
plt.show()"""

all_movies.to_csv("repaired_all_movies.csv",index=False,encoding='utf-8')  #CONVERT OUR REPAIRED DATA SET TO CSV FILE

