// Snowflake animation constants
const CANVAS_SELECTOR = ".snowoverlay";
const SNOWFLAKE_AMOUNT = 60;
const SNOWFLAKE_SIZE = { min: 1.5, max: 4 };
const SNOWFLAKE_SPEED = { min: 0.3, max: 1 };

// Setup canvas for snowflake animation
function setupCanvas() {
  const canvas = document.querySelector(CANVAS_SELECTOR);
  const ctx = canvas.getContext("2d");

  const setCanvasSize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  setCanvasSize();
  window.addEventListener("resize", setCanvasSize);

  return { canvas, ctx };
}

function randomRange(min, max) {
  return Math.random() * (max - min) + min;
}

const { canvas, ctx } = setupCanvas();

let snowflakes = [];

// Initialize snowflakes with random positions, sizes, and speeds
for (let i = 0; i < SNOWFLAKE_AMOUNT; i++) {
  snowflakes.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    size: randomRange(SNOWFLAKE_SIZE.min, SNOWFLAKE_SIZE.max),
    speed: randomRange(SNOWFLAKE_SPEED.min, SNOWFLAKE_SPEED.max)
  });
}

// Draw snowflakes on canvas and update their positions
function drawSnowflakes() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#fff";

  snowflakes.forEach(flake => {
    ctx.beginPath();
    ctx.arc(flake.x, flake.y, flake.size, 0, Math.PI * 2);
    ctx.fill();

    flake.y += flake.speed;
    if (flake.y > canvas.height) {
      flake.y = 0;
      flake.x = Math.random() * canvas.width;
    }
  });

  requestAnimationFrame(drawSnowflakes);
}

drawSnowflakes();


// Dummy user data (simulate database)
const dummyUser = {
  email: "dhruvraj0602@gmail.com",
  password: "123456789"
};

// Sign In form handling
const signInForm = document.getElementById('signInForm');

if (signInForm) {
  signInForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const email = this.querySelector('input[type="email"]').value.trim();
    const password = this.querySelector('input[type="password"]').value;

    if (!email || !password) {
      alert('Please fill in both email and password.');
      return;
    }

    if (email === dummyUser.email && password === dummyUser.password) {
      alert('Sign In successful! Redirecting...');
      window.location.href = 'dashboard.html'; // redirect on success
    } else {
      alert('Incorrect email or password.');
    }
  });
}

// Sign Up form handling (basic validation and alert)
const signUpForm = document.getElementById('signUpForm');

if (signUpForm) {
  signUpForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = this.querySelector('input[type="text"]').value.trim();
    const email = this.querySelector('input[type="email"]').value.trim();
    const password = this.querySelector('input[type="password"]').value;

    if (!name || !email || !password) {
      alert('Please fill in all the fields.');
      return;
    }

    // Here you could add more validation, like email format or password strength

    alert(`Thank you for signing up, ${name}! You can now sign in.`);
    // Optionally reset the form
    this.reset();

    // Switch to sign-in panel after sign-up
    container.classList.remove('right-panel-active');
  });
}

// Toggle between Sign In and Sign Up panels
const container = document.getElementById('container');
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');

signUpButton.addEventListener('click', () => {
  container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
  container.classList.remove('right-panel-active');
});
