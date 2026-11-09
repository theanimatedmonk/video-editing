// Tia's blob avatar (a Rive file), stepped by the video's timeline instead of
// its own clock, so preview and render show the same frame.
//
// Rive draws at the artboard's full size on a canvas of its own. Each frame is then
// copied down to the visible canvas with high-quality smoothing, because a GPU
// shrinking a big canvas in one jump leaves stair-stepped edges. Set the visible
// canvas's width and height to about twice its size on screen.
//
//   TiaBlob.create(canvas, { src, states }).then((blob) => {
//     tl.fromTo(blob, { t: 0 }, { t: 13, duration: 13, ease: "none" }, 0);
//   });
//
// `states` is a list of { at, state } in seconds: 0 idle, 1 thinking,
// 2 retrieving, 3 executing, 4 planning, 5 done. Setting `t` simulates the
// blob up to that time (its jelly physics only runs forward, so going back
// replays from the start).
(function () {
  const STEP = 1 / 60;

  function stateAt(states, t) {
    let s = states.length ? states[0].state : 0;
    for (const k of states) if (t >= k.at) s = k.state;
    return s;
  }

  function create(canvas, { src, states = [], artboard = "Blob", stateMachine = "Blob", drawSize = 512, crop = null, triggers = [], wasm = "assets/vendor/rive/rive.wasm", fallback = "assets/vendor/rive/rive_fallback.wasm" }) {
    const R = window.rive;
    if (!R) return Promise.reject(new Error("Rive runtime missing"));
    R.RuntimeLoader.setWasmUrl(wasm);
    const drawn = document.createElement("canvas");
    drawn.width = drawn.height = drawSize; // the blob's artboard size, so nothing is scaled inside Rive
    const view = canvas.getContext("2d");
    return new Promise((resolve, reject) => {
      const r = new R.Rive({
        src,
        canvas: drawn,
        artboard,
        stateMachines: stateMachine,
        autoplay: true,
        autoBind: true,
        enableGPUCanvas: true,
        drawOptimization: R.DrawOptimizationOptions ? R.DrawOptimizationOptions.AlwaysDraw : undefined,
        layout: new R.Layout({ fit: R.Fit.Cover, alignment: R.Alignment.Center }),
        onLoad: () => {
          // The video's clock is the only clock. Without these, Rive redraws by itself on real
          // time when the canvas is shown (jolting the jelly) and shrinks the canvas to its
          // on-screen size (pixelating it).
          r.stopRendering();
          r.resizeDrawingSurfaceToCanvas = () => {};
          r.drawFrame = () => {};
          r.scheduleRendering = () => {};
          let clock = 0; // ms of blob time drawn so far
          let simT = 0;
          let lastState = -1;
          let fired = 0;
          const fireTriggers = (t) => {
            while (fired < triggers.length && t >= triggers[fired].at) {
              const vm = r.viewModelInstance;
              const prop = vm && vm.trigger(triggers[fired].name);
              if (prop) prop.trigger();
              fired++;
            }
          };
          const setState = (n) => {
            if (n === lastState) return;
            const vm = r.viewModelInstance;
            const prop = vm && vm.number("state");
            if (prop) prop.value = n;
            lastState = n;
          };
          const advance = (dt) => {
            r.lastRenderTime = clock;
            clock += dt * 1000;
            r._hasZeroSize = false;
            r.draw(clock);
          };
          const present = () => {
            view.clearRect(0, 0, canvas.width, canvas.height);
            view.imageSmoothingEnabled = true;
            view.imageSmoothingQuality = "high";
            if (crop) view.drawImage(drawn, crop[0] * drawSize, crop[1] * drawSize, crop[2] * drawSize, crop[3] * drawSize, 0, 0, canvas.width, canvas.height);
            else view.drawImage(drawn, 0, 0, canvas.width, canvas.height);
          };
          const restart = () => {
            r.reset({ artboard, stateMachines: stateMachine, autoplay: true, autoBind: true });
            r.stopRendering();
            clock = 0;
            simT = 0;
            lastState = -1;
            fired = 0;
          };
          const blob = {
            rive: r,
            get t() {
              return simT;
            },
            set t(v) {
              if (v < simT - 1e-4) restart();
              if (simT === 0) {
                setState(stateAt(states, 0));
                fireTriggers(0);
                advance(0);
              }
              while (simT < v - 1e-6) {
                const dt = Math.min(STEP, v - simT);
                simT += dt;
                setState(stateAt(states, simT));
                fireTriggers(simT);
                advance(dt);
              }
              present();
            },
          };
          blob.t = 0;
          resolve(blob);
        },
        onLoadError: (e) => {
          // Try the fallback build once (no WebGL 2 features).
          if (wasm !== fallback) create(canvas, { src, states, artboard, stateMachine, drawSize, crop, triggers, wasm: fallback, fallback }).then(resolve, reject);
          else reject(e);
        },
      });
    });
  }

  // The logo's tile and all of its soft glow on the artboard, for showing just the mark.
  // The tile fills half of this square, so give a canvas twice the size you want the tile.
  window.TiaBlob = { create, LOGO_TILE: [0.2, 0.13, 0.6, 0.6] };
})();
