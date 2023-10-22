const searchEndpoint = '/api/start_search';
const domainPattern = 'https:\/\/(?:.*?\\.)*(\\w+?)\\.[a-z]{2,}\/?';


window.addEventListener('load', () => {
  let form = document.querySelector('#search-bar form');

  form.addEventListener('submit', event => {
    let username = document.querySelector('#search-bar form input').value;

    // Prevent default form submission
    event.preventDefault();

    if (username.length > 2) {
      return startSearch(username);
    }

    document.querySelector('#search-bar form input').focus();
  })
})

/**
 * Invoked as soon as a search is started
 *
 * Mainly adjusts visual components and initializes
 * result boxes with their corresponding link
 */
const prepareResultsPage = username => {
  document.title = `Tracer | Results for ${username}`;

  let searchBar = document.getElementById('search-bar');
  let input = searchBar.getElementsByTagName('input')[0];
  let searchButton = searchBar.getElementsByTagName('button')[0];
  let infoFooter = document.getElementById('info');

  // Move the search bar up
  searchBar.style.marginTop = '1%';

  infoFooter.style.top = 'inherit';
  infoFooter.style.marginTop = '30px';

  input.setAttribute('disabled', '');
  input.style.color = '#6272a4';
  input.style.borderBottomColor = input.style.color;

  searchButton.innerHTML = 'Back Home';
  searchButton.type = 'button';

  searchButton.onclick = () => {
    window.open('/', '_self');
  }

  // Initialize the result boxes
  for (let box of document.getElementsByClassName('result-box')) {
    let url = box.getAttribute('id').replace('{}', username);
    let domain = url.match(domainPattern)[1]; // Get the domain of the pre-init url

    box.style.display = "inherit"; // Make the box visible
    box.setAttribute('id', domain);
    box.addEventListener('click', () => {
      window.open(url);
    });
  }
}

/**
 * Start the search
 *
 * Send a POST request to the server with the specified
 * username
 */
const startSearch = username => {
  let request = new XMLHttpRequest();
  request.open('POST', searchEndpoint, true);
  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

  request.onreadystatechange = () => {
    if (request.readyState == 4 && request.status == 200) {
      prepareResultsPage(username);
      getResults();
    }
  }

  request.send(`username=${username}`);
}

/**
 * Retrieve the results from the server
 *
 * This is done by recursively sending GET
 * requests to the server
 */
const getResults = () => {
  let request = new XMLHttpRequest();
  request.open('GET', searchEndpoint, true);

  request.onreadystatechange = () => {
    if (request.readyState == 4) {
      if (request.status == 200 && request.responseText !== 'FINISHED') {
        let response;

        try {
          response = JSON.parse(request.responseText)['result'];
        } catch (e) {
          return getResults();
        }

        let box = document.getElementById(response[1].match(domainPattern)[1]);

        box.style.color = (response[0] ? "#50fa7b" : "#ff5555");
        box.style.borderColor = box.style.color;

        // Avoid too many boxes on small devices by removing failed ones
        if (!response[0] && window.innerWidth < 992) {
          document.getElementById('results').removeChild(box);
        }

        return getResults();
      } else {
        return null;
      }
    }
  }

  request.send();
}
