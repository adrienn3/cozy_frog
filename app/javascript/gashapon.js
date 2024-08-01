document.addEventListener("turbo:load", function () {
  console.log("Turbo load event fired");

  function initializeGashapon() {
    const canvas = document.getElementById("gashaponCanvas");
    if (!canvas) {
      console.log("Canvas not found, waiting...");
      return;
    }
    console.log("Canvas found, initializing...");
    const ctx = canvas.getContext("2d");

    const machine = new Image();
    const knob = new Image();
    const capsule = new Image();

    let knobRotation = 0;
    let capsuleY = -50;
    let capsuleFalling = false;
    let twisting = false;

    machine.src = "/assets/gasha.webp";
    knob.src = "/assets/knob.webp";
    capsule.src = "/assets/capsule.webp";

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.drawImage(machine, 0, 0, 300, 300);

      ctx.save();
      ctx.translate(100, 250);
      ctx.rotate((knobRotation * Math.PI) / 180);
      ctx.drawImage(knob, -20, -20, 40, 40);
      ctx.restore();

      if (capsuleFalling) {
        ctx.drawImage(capsule, 90, capsuleY, 20, 20);
        capsuleY += 2;
        if (capsuleY > 280) {
          capsuleFalling = false;
          fetch("/pull_item", { method: "GET" })
            .then((response) => response.json())
            .then((data) => {
              const pulledItem = document.createElement("div");
              pulledItem.textContent = `You pulled: ${data.pulled}`;
              pulledItem.style.position = "absolute";
              pulledItem.style.top = "50%";
              pulledItem.style.left = "50%";
              pulledItem.style.transform = "translate(-50%, -50%)";
              pulledItem.style.backgroundColor = "white";
              pulledItem.style.padding = "10px";
              pulledItem.style.border = "1px solid black";
              document.body.appendChild(pulledItem);
              canvas.remove();
            })
            .catch((error) => console.error("Error:", error));
        }
      }

      if (twisting) {
        twistKnob();
      }

      requestAnimationFrame(draw);
    }

    function twistKnob() {
      knobRotation += 5;
      if (knobRotation >= 360) {
        knobRotation = 0;
        capsuleFalling = true;
        capsuleY = 50;
        twisting = false;
      }
    }

    canvas.addEventListener("click", function () {
      twisting = true;
    });

    draw();
  }

  function observeDOM() {
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (mutation.addedNodes.length) {
          initializeGashapon();
        }
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  observeDOM();
});
