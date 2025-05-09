const episodesEl = document.querySelector('.episodes');
const loader = document.querySelector('.loader');

const getPage = async (page) => {
    let res = await axios.post("/getEpisodes", { "page": JSON.stringify(`${page}`) });
    // return res.data;

    // handle 404
    if (res.status != 200) {
        throw new Error(`An error occurred: ${res.status}`);
    }

    return await res.data;
}

const getMedia = async (id, page, limit) => {
    console.log("getMedia");
    async function saveToDb(episode_enabledSettings) {
        let res = await axios.get("/episodes", { "episodes": JSON.stringify(episode_enabledSettings) });
        return res.data;
    }

    const API_URL = "http://api.tvmaze.com/shows/" + id + "/episodes"
    console.log("API_URL", API_URL);
    const response = await fetch(API_URL);
    console.log("response", response);
    // handle 404
    if (!response.ok) {
        throw new Error(`An error occurred: ${response.status}`);
    }
    return await response.json();
}

const getEpisodes = async (page, limit) => {
    console.log("getEpisodes");
    const API_URL = "/getEpisodes"
    console.log("API_URL", API_URL);
    const response = await fetch(API_URL, { method: "post", body: { "page": JSON.stringify(`${page}`), "limit": JSON.stringify(`${limit}`) } });

    // handle 404
    if (!Response.ok) {
        throw new Error(`An error occurred: ${response.status}`);
    }
    return await response.json();
}


// media = Media.query.order_by(Media.ord).all()
// for m in media:                  # Retrieve episodes for each TV Series and insert into 'title' table
//         # if m.id == 490 or m.id == 3513:
// if m.media_type == 'TV':     # Do not include Movies
// url = "http://api.tvmaze.com/shows/" + str(m.id) + "/episodes"
// res = requests.get(url)
// data = res.json()
// for d in data:
//     abbr, season, name, episode = corrections(
//         m.abbr, d['season'], d['name'], d['number'])
// if name not in misnamed_episodes:
// title = Title(abbr = m.abbr, premiered_date = d['airdate'], media_id = m.id,
//     season_id = d['season'], episode_id = episode, title = name, summary = d['summary'])
// db.session.add(title)
// db.session.commit()


// show the episodes
const showEpisodes = (episodes) => {
    episodes.forEach(episode => {
        let date = JSON.stringify(new Date(episode[0].airdate)); //Jsonify changes date format; changing it back here
        date = date.slice(1, 11); //changing it back here

        const episodeEl = document.createElement('tr');
        episodeEl.classList.add(episode[0].abbr);

        episodeEl.innerHTML = `
        <td class="${episode[0].abbr}-logo"></td>
        `;
        episodeEl.innerHTML = `
        <td class="${episode[0].abbr}-logo"></td>
        <td class="episode_id">${episode[0].season_id}-${episode[0].episode_id}</td>
        
        <td class="title"><a href="https://memory-alpha.fandom.com/wiki/${episode[0].title}_(episode)">${episode[0].title}</a>
            </td>
        <td class="airdate">${date}</td>
        `;

        episodesEl.appendChild(episodeEl);

        // <td class="title"><a href="https://memory-alpha.fandom.com/wiki/${episode[6] | replace('?', '%3F')}_(episode)">${episode[6]}</a>
    });
};

const hideLoader = () => {
    loader.classList.remove('show');
};

const showLoader = () => {
    loader.classList.add('show');
};

// load episodes
// const loadEpisodes = async (page, limit) => {
//     // show the loader
//     showLoader();

//     // 0.5 second later
//     setTimeout(async () => {
//         try {
//             // if having more episodes to fetch
//             total = 852
//             if (hasMoreEpisodes(page, retrieved, total)) {
//                 console.log("LOADEPISODES");
//                 // call the API to get episodes
//                 const response = await getPage(page, limit);
//                 console.log("LOADEPISODES - after GET");
//                 // show episodes
//                 showEpisodes(response);
//                 console.log("LOADEPISODES - after SHOW EPISODES");
//                 // update the total
//                 retrieved = response.length;
//                 console.log("TOTAL", total);
//             }
//         } catch (error) {
//             console.log("777777777777");
//             console.log(error.message);
//         } finally {
//             hideLoader();
//         }
//     }, 500);

// };

// load episodes
const loadEpisodes = async (page) => {
    // show the loader
    showLoader();

    try {
        // if having more episodes to fetch
        total = 852

        // call the API to get episodes
        const response = await getPage(page);

        // show episodes
        showEpisodes(response);

        // update the total
        retrieved = response.length;
        console.log("retrieved = ", retrieved);
        console.log("TOTAL", total);
    } catch (error) {
        console.log("777777777777");
        console.log(error.message);
    } finally {
        hideLoader();
    }
};

let currentPage = 1;
let total = 0;
let retrieved = 0;

window.addEventListener('scroll', () => {
    const {
        scrollTop,
        scrollHeight,
        clientHeight
    } = document.documentElement;
    console.log("LISTENER");

    // if (scrollTop + clientHeight >= scrollHeight - 5) {
    if (scrollTop + clientHeight >= scrollHeight) {
        console.log("scrollTop = ", scrollTop);
        console.log("scrollHeight = ", scrollHeight);
        console.log("clientHeight = ", clientHeight);
        console.log(scrollTop + clientHeight);
        console.log(scrollHeight - 5);
        console.log("LISTENER  -  IF");
        currentPage++;
        console.log(total)
        console.log("currPage = ", currentPage)
        loadEpisodes(currentPage);
        console.log("END LISTENER  -  IF");
    }
}, {
    passive: true
});

loadEpisodes(currentPage);