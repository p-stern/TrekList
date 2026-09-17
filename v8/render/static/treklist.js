// Based on code from  https://stackoverflow.com/questions/14544104/checkbox-check-event-listener

const season_checkboxes = document.querySelectorAll("input[type=checkbox][name=season]")
const episode_checkboxes = document.querySelectorAll("input[type=checkbox][name=episode]")
const comments = document.querySelectorAll(".fa-regular");
const lsSeasons = JSON.parse(localStorage.getItem('seasons'));
const lsEpisodes = JSON.parse(localStorage.getItem('episodes'));
const h2 = document.getElementById("watched");
let watched = 0;
let total = 0;
let season_enabledSettings = [];
let episode_enabledSettings = [];
let season_episode = [];

// Use Array.forEach to add to each checkbox.
season_checkboxes.forEach(function () {
  season_value =
    Array.from(season_checkboxes) // Convert checkboxes to an array to use filter and map.
      .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.
});


season_value.forEach(season => {
  // Count the number of episodes (checkboxes) per season
  let cnt = document.querySelectorAll(`input[type=checkbox][name=episode][value^='${season}']`).length;

  // Count the number of double episodes (checkboxes) per season
  let double_episode_cnt = document.querySelectorAll(`input[type=checkbox][name=episode][value^='${season}'][value*='/']`).length;

  full_cnt = cnt + double_episode_cnt
  total += full_cnt;
  season_episode.push({ season, full_cnt });
});

if ((lsSeasons !== null) | (lsEpisodes !== null)) {
  season_enabledSettings = lsSeasons;
  episode_enabledSettings = lsEpisodes;

  check_season_enabledSettings(season_enabledSettings);
  check_episode_enabledSettings(episode_enabledSettings);
};

set_watched_cnt();

// Use Array.forEach to add an event listener to each checkbox.
season_checkboxes.forEach(function (checkbox) {
  checkbox.addEventListener('change', async function () {
    season_enabledSettings =
      Array.from(season_checkboxes) // Convert checkboxes to an array to use filter and map.
        .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
        .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.

    check_season_enabledSettings(season_enabledSettings);

    // If season checkbox is unchecked, uncheck that season's episodes
    if (checkbox.checked === false) {
      for (const episode of episode_enabledSettings) {
        if (episode === checkbox.value) {
          document.getElementById(episode).checked = false;
        }
        else {
          ids = document.querySelectorAll(`[id^="${checkbox.value}"]`);
          ids.forEach(i => i.checked = false);
        }
      }
    }

    episode_enabledSettings =
      Array.from(episode_checkboxes) // Convert checkboxes to an array to use filter and map.
        .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
        .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.

    set_watched_cnt();

    // Save season & episode checkbox info in localStorage
    set_lS();

    // Save episode checkbox info in postgreSQL
    let result = await saveToDb(episode_enabledSettings);
  })
});

// Use Array.forEach to add an event listener to each checkbox.
episode_checkboxes.forEach(function (checkbox) {
  checkbox.addEventListener('change', async function () {
    episode_enabledSettings =
      Array.from(episode_checkboxes) // Convert checkboxes to an array to use filter and map.
        .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
        .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.

    if (checkbox.value.includes("Movie")) {
      chkbx_val = checkbox.value;
    }
    else {
      indexOfHyphen = checkbox.value.indexOf('-');
      chkbx_val = checkbox.value.slice(0, indexOfHyphen); //extract season from episode checkbox
    };


    check_seasons(chkbx_val);

    set_watched_cnt();

    season_enabledSettings =
      Array.from(season_checkboxes) // Convert checkboxes to an array to use filter and map.
        .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
        .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.

    // Save season & episode checkbox info in localStorage
    set_lS();

    // Save episode checkbox info in postgreSQL
    let result = await saveToDb(episode_enabledSettings);
  })
});

// Format to jump to episode 1 or episode 1/2 
function jumpToSeason(abbr, n) {
  if ((abbr === "TOS" & n === "4")) {
    return window.location.assign(`#${abbr}0-0`);
  }
  else if ((abbr === "TNG" & n === "1") || (abbr === "DS9" & n === "1") || (abbr === "DS9" & n === "4") ||
    (abbr === "VOY" & n === "1") || (abbr === "ENT" & n === "1") || (abbr === "PRO" & n === "1")) {
    return window.location.assign(`#${abbr}${n}-1/2`);
  }
  else {
    return window.location.assign(`#${abbr}${n}-1`);
  }
}

function check_season_enabledSettings(season_enabledSettings) {
  for (const season of season_enabledSettings) {
    id = document.querySelector(`input[type=checkbox][name=season][value="${season}"]`);
    id.checked = true;

    if (season.includes("Movie")) {
      document.getElementById(season).checked = true;
    }
    else {
      ids = document.querySelectorAll(`[id^="${season}"]`);
      ids.forEach(i => i.checked = true);
    }
  }
}

function check_episode_enabledSettings(episode_enabledSettings) {
  for (const episode of episode_enabledSettings) {
    id = document.getElementById(episode);
    id.checked = true;
  }
}

function check_seasons(chkbx_val) {
  season_episodes_obj = season_episode.find(obj => obj.season === `${chkbx_val}`);

  checked_episodes = episode_enabledSettings.filter(element => element.includes(`${chkbx_val}`));
  checked_episodes_cnt = checked_episodes.filter(element => element.includes(`${chkbx_val}`)).length;
  douple_episode_cnt = checked_episodes.filter((element) => element.includes('/')).length;

  checked_episodes_cnt += douple_episode_cnt;

  id = document.querySelector(`input[type=checkbox][name=season][value="${chkbx_val}"]`);

  if (season_episodes_obj.full_cnt !== checked_episodes_cnt) {
    // If not all the episodes in a season are checked, uncheck season checkbox
    id.checked = false;
  }
  else {
    // If all the episodes in a season are checked, check season checkbox
    id.checked = true;
  }
}

function set_watched_cnt() {
  douple_episode_cnt = episode_enabledSettings.filter((element) => element.includes('/')).length;
  watched = episode_enabledSettings.length + douple_episode_cnt;
  h2.innerHTML = watched + '/' + total;
}

function set_lS() {
  localStorage.clear();
  localStorage.setItem('seasons', JSON.stringify(season_enabledSettings));
  localStorage.setItem('episodes', JSON.stringify(episode_enabledSettings));
}

async function saveToDb(episode_enabledSettings) {
  let res = await axios.post("/episodes", { "episodes": JSON.stringify(episode_enabledSettings) });
  return res.data;
}

function lsclear() {
  localStorage.clear();
  window.location = "/logout";
}

function loadViewed(viewed) {
  if (episode_enabledSettings.length === 0) {
    for (const v in viewed) {
      episode_enabledSettings.push(viewed[v]);
    }
  }

  // check_season_enabledSettings(season_enabledSettings);
  check_episode_enabledSettings(episode_enabledSettings);

  episode_enabledSettings.forEach(function (episode) {
    if (episode.includes("Movie")) {
      chkbx_val = episode;
    }
    else {
      indexOfHyphen = episode.indexOf('-');
      chkbx_val = episode.slice(0, indexOfHyphen); //extract season from episode checkbox
    }

    check_seasons(chkbx_val);

    id = document.querySelector(`input[type=checkbox][name=season][value="${chkbx_val}"]`);
    if (id.checked === true) {
      if (!season_enabledSettings.includes(`${chkbx_val}`)) {
        season_enabledSettings.push(chkbx_val);
      }
    }

    set_watched_cnt();
  });

  // Save season & episode checkbox info in localStorage
  set_lS();
}