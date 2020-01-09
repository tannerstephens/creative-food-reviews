window.onload = function() {
  const usernameInput = document.querySelector("#username");
  const passwordInput = document.querySelector("#password");
  const confirmInput = document.querySelector("#confirm");
  const userAvailable = document.querySelector("#userAvailable");
  const passwordMatch = document.querySelector("#passwordMatch");
  const submitButton = document.querySelector("#submit");

  let usertimeout = null;
  let usernameGood = false;
  let passwordGood = false;

  function verify() {
    submitButton.disabled = !(usernameGood && passwordGood);
  }

  usernameInput.oninput = function() {
    clearTimeout(usertimeout);

    usertimeout = setTimeout(function() {
      const username = usernameInput.value;

      if (username == '') {
        return;
      }
    
      fetch('/api/userValid/' + username)
        .then(function(response) {
          return response.json();
        })
        .then(function(json) {
          if (json.available == false) {
            userAvailable.classList.remove('is-hidden');
            usernameGood = false;
          } else {
            userAvailable.classList.add('is-hidden');
            usernameGood = true;
          }
          verify();
        });
      }, 750);
  };
  
  confirmInput.oninput = function() {
    const confirmValue = confirmInput.value;
    const password = passwordInput.value;

    if (confirmValue === password) {
      passwordGood = true;
      passwordMatch.classList.add('is-hidden');
    } else {
      passwordGood = false;
      passwordMatch.classList.remove('is-hidden');
    }

    verify();
  }
};
