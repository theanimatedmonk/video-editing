// Device rig: a 3D MacBook or iPad from device-stage, driven by the video's
// timeline instead of its own clock.
//
//   const mac = createDevice(el, { model: "macbookPro14", keys: [...] });
//   tl.fromTo(mac, { t: 0 }, { t: 71, duration: 71, ease: "none" }, 0);
//
// Setting `t` (seconds of the video) poses the device and camera from `keys`
// and draws that exact frame, so preview and render always agree.
//
// A key: { at, ease, cut, ...pose }. Between two keys the pose eases from
// the first to the second (the second key's ease, default "power2.inOut").
// `cut: true` on a key jumps to it instead: the earlier pose holds until then.
// Pose fields (any subset; missing ones carry over from the key before):
//   az, el, dist, fov, roll, tx, ty   camera orbit (degrees, cm)
//   rx, ry, rz, x, y, z               device turn (degrees) and position (cm)
//   lid                               a laptop's hinge in degrees (0 shut, 110 open)

import { DeviceStage } from "../vendor/device-stage/stage.js";

const BASE = { az: 0, el: 0, dist: 44, fov: 28, roll: 0, tx: 0, ty: 0, rx: 0, ry: 0, rz: 0, x: 0, y: 0, z: 0, lid: 110 };

function resolveKeys(keys) {
  let prev = { ...BASE };
  return keys
    .slice()
    .sort((a, b) => a.at - b.at)
    .map((k) => {
      const pose = { ...prev };
      for (const f of Object.keys(BASE)) if (k[f] !== undefined) pose[f] = k[f];
      prev = pose;
      return { at: k.at, cut: !!k.cut, ease: window.gsap.parseEase(k.ease || "power2.inOut"), pose };
    });
}

function poseAt(keys, t) {
  if (t <= keys[0].at) return keys[0].pose;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t >= b.at) continue;
    if (b.cut) return a.pose;
    const p = b.ease((t - a.at) / Math.max(b.at - a.at, 1e-6));
    const out = {};
    for (const f in a.pose) out[f] = a.pose[f] + (b.pose[f] - a.pose[f]) * p;
    return out;
  }
  return keys[keys.length - 1].pose;
}

export function createDevice(container, { model, finish = "Space Black", keys, look = {}, glass = false, clearBackdrop = false }) {
  const stage = new DeviceStage(container, {
    lockToggle: false,
    state: {
      shot: "manual",
      playing: false,
      layout: 1,
      interact: "device",
      slots: [{ model, finish, screen: "dom", lid: 110 }],
      device: { rotX: 0, rotY: 0, rotZ: 0, x: 0, y: 0, z: 0, float: 0 },
      look: { backdrop: "Custom", inner: "#0f1830", outer: "#040508", shadow: 0.35, reflections: 0.9, exposure: 1, glare: 0.6, screen: 1, ...look },
      output: { aspect: "fill", height: 1080, fps: 30 },
    },
  });
  // The glass's reflections tint the screen unevenly; keep the screen true unless asked.
  if (!glass && stage.slots[0].dev) stage.slots[0].dev.glass.visible = false;
  // A clear backdrop lets the page's own background show behind the device.
  if (clearBackdrop) stage.scene.background = null;
  // The timeline is the only clock: stop the stage's own loop.
  cancelAnimationFrame(stage.raf);
  stage.tick = () => {};

  const resolved = resolveKeys(keys);
  let lastLid = null;
  let time = 0;

  const rig = {
    stage,
    screen: stage.screen(0),
    viewport: stage.viewport(model),
    get t() {
      return time;
    },
    set t(v) {
      time = v;
      const p = poseAt(resolved, v);
      Object.assign(stage.state.camera, { azimuth: p.az, elevation: p.el, distance: p.dist, fov: p.fov, roll: p.roll, targetX: p.tx, targetY: p.ty });
      Object.assign(stage.state.device, { rotX: p.rx, rotY: p.ry, rotZ: p.rz, x: p.x, y: p.y, z: p.z, float: 0 });
      if (p.lid !== lastLid && stage.slots[0].dev?.setLid) {
        stage.slots[0].dev.setLid(p.lid);
        stage.state.slots[0].lid = p.lid;
        lastLid = p.lid;
      }
      stage.layout();
      stage.apply(0);
      stage.render();
    },
  };
  rig.t = 0;
  return rig;
}
