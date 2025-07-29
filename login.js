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
