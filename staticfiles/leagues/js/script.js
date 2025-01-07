document.addEventListener('DOMContentLoaded', () => {
  const options = document.querySelectorAll('.option');
  const leagueLogo = document.getElementById('league-logo');
  const optionsViewButton = document.getElementById('options-view-button'); // Get the checkbox

  options.forEach(option => {
    option.addEventListener('click', () => {
      const leagueValue = option.querySelector('.opt-val').textContent;
      updateLogo(leagueValue);
      closeOptionsList(); // Close the options list after selection
    });
  });

  function updateLogo(league) {
    let logoUrl = '';
    switch (league) {
      case 'Bundesliga':
        logoUrl = "D:/Web devlopment/Project/logos/bundesliga.jpg"; // Replace with actual URL
        break;
      case 'Laliga':
        logoUrl = "D:/Web devlopment/Project/logos/laliga.png"; // Replace with actual URL
        break;
        case 'Ligue1':
        logoUrl = "D:/Web devlopment/Project/logos/ligue1.png"; // Replace with actual URL
        break;
      case 'Premier':
        logoUrl = "D:/Web devlopment/Project/logos/Premier.jpg"; // Replace with actual URL
        break;
        case 'Serie A':
        logoUrl = "D:/Web devlopment/Project/logos/serie A.png"; // Replace with actual URL
        break;
      // Add cases for other leagues
    }
    if (logoUrl) {
      leagueLogo.src = logoUrl;
      leagueLogo.style.display = 'block';
    }
  }

  function closeOptionsList() {
    optionsViewButton.checked = false; // Uncheck the checkbox to hide the options
  }
});
$("#heart-trigger").click(function () {
  $("li").toggleClass("visible");
});

// Function to create an animated football
function createFootball(containerId) {
  const container = document.getElementById(containerId);
  const football = document.createElement('div');
  football.className = 'football';
  football.style.position = 'absolute';
  football.style.top = '-50px'; // Start above the container
  // Add additional styling for football
  container.appendChild(football);

  // Add animation logic
  let yPos = 0;
  const interval = setInterval(() => {
    yPos++;
    football.style.top = `${yPos}px`;
    if (yPos > window.innerHeight) {
      clearInterval(interval);
      container.removeChild(football);
    }
  }, 10); // Adjust timing to control the speed

  return interval;
}

// Start dropping footballs
let leftAnimation, rightAnimation;
leftAnimation = createFootball('football-container-left');
rightAnimation = createFootball('football-container-right');

// Stop animation on button click
document.getElementById('stop-animation-btn').addEventListener('click', () => {
  clearInterval(leftAnimation);
  clearInterval(rightAnimation);
});
document.getElementById('league-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission
  
  const league = document.getElementById('league-select').value;
  const name = document.getElementById('name-input').value;
  
  console.log('Selected League:', league);
  console.log('Name:', name);
  
  // Here you would typically send the data to a server or perform some action with it
});
