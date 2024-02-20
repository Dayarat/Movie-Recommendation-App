from rec_sys.rec_func import recommender
from h2o_wave import Q, main, app, ui
from fuzzywuzzy import process
from typing import Any
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

def search_movies(movie_name: str) -> list[tuple[Any, Any | int, Any] | tuple[Any, Any | int]]:
    """
    Find similar movies name wise (using Levenshtein distance).
    """
    return process.extract(movie_name, recommender.movie_names)


@app("/recommender")
async def serve(q: Q):
    """
    Displays the recommended movies according to the input.
    If the user cannot find the movie, user can find the movies that matches to the given input.
    """
    
    stylesheet_path, = await q.site.upload([os.path.join(current_dir, 'css/main.css')])
    # Use the uploaded file path in the `ui.stylesheet`.
    q.page['meta'] = ui.meta_card(
      box='', 
      stylesheets=[
        ui.stylesheet(stylesheet_path)
      ]
    )
    
    msg = ""
    
    if not q.client.initialized:
        q.client.initialized = True
    
    if q.args.search:
        del q.page["movies"]
        q.args.search_box_input = q.args.search_box_input.strip()
        if q.args.search_box_input in recommender.movie_names:
            result = recommender.recommend(q.args.search_box_input)

            msg = f"If you liked {q.args.search_box_input}, you may also like these movies!"
            add_movie_cards(result, q)

        elif q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Movie name cannot be blank."

        else:
            msg = f'"{q.args.search_box_input}" is not in our database or an invalid movie name. \
            Use the "Find Movie" button to find movies'

    if q.args.find_movies:
        q.args.search_box_input = q.args.search_box_input.strip()
        if q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Movie name cannot be blank."
        else:
            for i in range(1, 6):
                del q.page[f"movie{i}"]
            add_similar_movies(q)

    add_search_box(q, msg)
    add_header(q)
    add_footer(q)
    

    await q.page.save()


def add_similar_movies(q: Q):
    similar_movies = search_movies(q.args.search_box_input)
    q.page["movies"] = ui.form_card(
        box="2 4 10 7",
        items=[
            ui.copyable_text(
                value=movie[0],
                name=f"movie_match{i+1}",
                label=f"{movie[1]}% match",
            )
            for i, movie in enumerate(similar_movies)
        ],
    )


def add_movie_cards(result, q: Q):
    for i in range(1, 6):
        q.page[f"movie{i}"] = ui.tall_article_preview_card(
            box=f"{2*i} 4 2 7",
            title=f"{result[i-1].title}",
            subtitle=f"{result[i-1].director}",
            value=f"{result[i-1].year}",
            name="tall_article",
            image=f"{result[i-1].image}",
            items=[
                ui.text(f"Director: {result[i-1].director}", size="l"),
                ui.text(f"IMDb Rating: {result[i-1].rating}", size="m"),
            ],
        )


def add_header(q: Q):
    q.page["header"] = ui.header_card(
        box="2 1 10 1",
        title="Find Your Movie",
        subtitle="A system to find the movie you were searching for",
        icon="Movie",
        items=[
            ui.link(
                name="github_btn",
                path="https://github.com/Dayarat/Movie-Recommendation-App",
                label="GitHub",
                button=True,
            )
        ],
    )


def add_search_box(q: Q, msg):
    q.page["search_box"] = ui.form_card(
        box="2 2 10 2",
        items=[
            ui.textbox(
                name="search_box_input",
                label="Movie Name",
                value=q.args.search_box_input,
            ),
            ui.buttons(
                items=[
                    ui.button(
                        name="search",
                        label="Search",
                        primary=True,
                        icon="MovieSearch",
                    ),
                    ui.button(name="find_movies", label="Find Movie", primary=False),
                ]
            ),
            ui.text(msg, size="m", name="msg_text"),
        ],
    )


# Function add_footer remains the same as in the previous example

# Define function to add footer to UI
def add_footer(q: Q):
    caption = """<div style="text-align: center; color: white; background-color: #007BFF; padding: 10px;">
                    Created by Kavindu Sandruwan. ----->
                    <a href="https://wave.h2o.ai/docs/getting-started" style="color: white; text-decoration: none;" target="_blank">h2o Wave</a>
                 </div>"""
    q.page["footer"] = ui.footer_card(
        box="2 11 10 2",
        caption=caption,
        items=[
            ui.inline(
                justify="end",
                items=[
                    ui.links(
                        label="Contact Me",
                        width="200px",
                        items=[
                            ui.link(
                                name="github",
                                label="GitHub",
                                path="https://github.com/Dayarat/Movie-Recommendation-App",
                                target="_blank",
                            ),
                            ui.link(
                                name="linkedin",
                                label="LinkedIn",
                                path="https://www.linkedin.com/in/kavindu-sandaruwan-699973249/",
                                target="_blank",
                            ),
                        ],
                    ),
                ],
            ),
            
        ],
    )
