// Snowflake animation
const CANVAS_SELECTOR = ".snowoverlay";
const SNOWFLAKE_AMOUNT = 60;
const SNOWFLAKE_SIZE = { min: 1.5, max: 4 };
const SNOWFLAKE_SPEED = { min: 0.3, max: 1 };

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

for (let i = 0; i < SNOWFLAKE_AMOUNT; i++) {
  snowflakes.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    size: randomRange(SNOWFLAKE_SIZE.min, SNOWFLAKE_SIZE.max),
    speed: randomRange(SNOWFLAKE_SPEED.min, SNOWFLAKE_SPEED.max)
  });
}

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

// Panel slider control
const container = document.getElementById('container');
document.getElementById('signUp').addEventListener('click', () => {
  container.classList.add("right-panel-active");
});
document.getElementById('signIn').addEventListener('click', () => {
  container.classList.remove("right-panel-active");
});

// ---------
// Dummy user data (simulate database)
const dummyUser = {
  email: "dhruvraj0602@gmail.com",
  password: "123456789"
};

const signUpForm = document.getElementById('signUpForm');

if (signUpForm) {
  signUpForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = this.querySelector('input[placeholder="Name"]').value.trim();
    const email = this.querySelector('input[type="email"]').value.trim();
    const password = this.querySelector('input[type="password"]').value;

    if (!name || !email || !password) {
      alert('Please fill in all fields.');
      return;
    }

    // Check if input matches dummy user data exactly
    if (email === dummyUser.email && password === dummyUser.password) {
      alert('Registration successful! Redirecting to home page...');
      window.location.href = 'index.html'; 
    } else {
      alert('Registration failed: Email or password does not match the required data.');
    }
  });
}
