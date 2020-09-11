window.onload = function() {
  const mealName = document.querySelector("#meal");
  const mealSource = document.querySelector("#source");
  const otherSource = document.querySelector("#other");
  const review = document.querySelector("#review");
  const rating = document.querySelector("#rating");
  const file = document.querySelector("#file");
  const fileLabel = document.querySelector("#fileLabel");
  const submit = document.querySelector("#submit");
  const mealchar = document.querySelector("#mealchar");
  const sourcechar = document.querySelector("#sourcechar");

  function verify() {

    const mealSourceGood = ( mealSource.value !== 'other' && mealSource.value.length) ? true : otherSource.value.length;
    const reviewGood = review.value.length;
    // doesnt work for some reason
    const r = parseFloat(rating.value);
    const ratingGood = (r >= 0 && r <= 10);
    const mealNameGood = mealName.value.length;

    const lengths = mealSource.value.length < 100 && mealSource.value.length < 50;

    submit.disabled = !(mealNameGood && mealSourceGood && reviewGood && ratingGood && lengths);
  }

  file.onchange = function(e) {
    const filename = file.value.split(/(\\|\/)/g).pop();

    if ( filename.length >= 13 ) {
      fileLabel.innerHTML = filename.substring(0,10) + '...';
    } else {
      fileLabel.innerHTML = filename;
    }
  }

  mealSource.onchange = function(e) {
    otherSource.disabled = (mealSource.value != 'other');
    verify();
  };

  otherSource.oninput = function(e)  {
    sourcechar.innerHTML = otherSource.value.length + '/50';

    if (otherSource.value.length > 50) {
      sourcechar.classList.add('has-background-danger');
      sourcechar.classList.add('has-text-white');
    } else {
      sourcechar.classList.remove('has-background-danger');
      sourcechar.classList.remove('has-text-white');
    }

    verify();
  };

  review.oninput = verify;

  rating.oninput = verify;

  mealName.oninput = function(e) {
    mealchar.innerHTML = mealName.value.length + '/100';

    if (mealName.value.length > 100) {
      mealchar.classList.add('has-background-danger');
      mealchar.classList.add('has-text-white');
    } else {
      mealchar.classList.remove('has-background-danger');
      mealchar.classList.remove('has-text-white');
    }

    verify()
  };

  verify();
  mealSource.onchange();
  mealName.oninput();
  otherSource.oninput();
};
