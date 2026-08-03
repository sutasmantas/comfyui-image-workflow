const form = document.querySelector("#recipe-form");
const errorBox = document.querySelector("#form-error");
const failureToggle = document.querySelector("#simulate-failure");
const adapter = document.querySelector("#adapter");
const submitButton = form.querySelector("button[type=submit]");
const retryButton = document.querySelector("#retry-button");
let activeJob = null;
let pollTimer = null;
let browserRun = 0;
const browserMode = window.location.hostname.endsWith("github.io")
  || new URLSearchParams(window.location.search).has("static");

adapter.addEventListener("change", () => {
  failureToggle.checked = false;
  failureToggle.disabled = adapter.value !== "mock";
  document.querySelector("#mode-label").textContent = adapter.value === "mock" ? "Prepared render" : "Live ComfyUI";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();
  const [width, height] = document.querySelector("#size").value.split("x").map(Number);
  const payload = {
    prompt: document.querySelector("#prompt").value,
    negative_prompt: document.querySelector("#negative").value,
    seed: Number(document.querySelector("#seed").value),
    width,
    height,
    steps: Number(document.querySelector("#steps").value),
    cfg: Number(document.querySelector("#cfg").value),
    adapter: adapter.value,
    simulate_failure: failureToggle.checked,
  };
  await queue("/api/jobs", payload);
});

retryButton.addEventListener("click", async () => {
  if (!activeJob) return;
  hideError();
  await queue(`/api/jobs/${activeJob.id}/retry`, {});
});

async function queue(url, payload) {
  submitButton.disabled = true;
  if (browserMode) {
    runInBrowser(url, payload);
    return;
  }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error?.message || "The run could not be queued.");
    activeJob = body;
    render(body);
    clearTimeout(pollTimer);
    pollTimer = setTimeout(poll, 120);
  } catch (error) {
    showFormError(error.message);
    submitButton.disabled = false;
  }
}

function runInBrowser(url, payload) {
  if (adapter.value === "comfyui") {
    showFormError("Live ComfyUI connects from the full local stack. Choose Prepared render to use this browser workspace.");
    submitButton.disabled = false;
    return;
  }
  browserRun += 1;
  const retryOf = url.includes("/retry") ? activeJob?.id : null;
  const recipe = retryOf ? activeJob.recipe : payload;
  const id = `browser-${String(browserRun).padStart(3, "0")}`;
  activeJob = {
    id,
    status: "running",
    stage: "Compiling workflow graph",
    progress: 40,
    recipe,
    workflow: { digest: "72ab91f02fd585b5f18ad3cf4875ce4d" },
    artifact: null,
    error: null,
    retry_of: retryOf,
  };
  render(activeJob);
  window.setTimeout(() => {
    const shouldFail = Boolean(recipe.simulate_failure) && !retryOf;
    activeJob = shouldFail
      ? {
          ...activeJob,
          status: "failed",
          stage: "Provider stopped safely",
          progress: 45,
          error: {
            message: "The render provider stopped before producing a frame.",
            handoff: "The recipe and graph are retained; retry starts a linked run.",
          },
        }
      : {
          ...activeJob,
          status: "succeeded",
          stage: "Artifact ready",
          progress: 100,
          error: null,
          artifact: {
            url: "./campaign-radio-showcase.png",
            mime_type: "image/png",
            size_bytes: 716844,
            sha256: "f1d39fdcf2483a108f208e4722943ddae6f34ddc8a3f14f8f9cc31824c37b9c3",
            provider_metadata: { renderer: "prepared-render" },
          },
        };
    render(activeJob);
    submitButton.disabled = false;
  }, 650);
}

async function poll() {
  if (!activeJob) return;
  try {
    const response = await fetch(`/api/jobs/${activeJob.id}`, { cache: "no-store" });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error?.message || "Run status is unavailable.");
    activeJob = body;
    render(body);
    if (["queued", "running"].includes(body.status)) pollTimer = setTimeout(poll, 180);
    else submitButton.disabled = false;
  } catch (error) {
    showFormError(error.message);
    submitButton.disabled = false;
  }
}

function render(job) {
  document.querySelector("#job-id").textContent = `RUN ${job.id}`;
  document.querySelector("#status").textContent = job.status;
  document.querySelector("#stage").textContent = job.stage;
  document.querySelector("#progress").textContent = `${job.progress}%`;
  const stages = [...document.querySelectorAll(".stage")];
  stages.forEach((stage) => {
    stage.classList.toggle("active", job.progress >= Number(stage.dataset.threshold));
    stage.classList.toggle("failed", job.status === "failed" && stage.classList.contains("active"));
  });
  document.querySelector("#pipeline-fill").style.width = `${job.progress}%`;

  const errorPanel = document.querySelector("#error-panel");
  errorPanel.hidden = !job.error;
  if (job.error) {
    document.querySelector("#error-message").textContent = job.error.message;
    document.querySelector("#error-handoff").textContent = job.error.handoff;
  }

  if (job.artifact) {
    document.querySelector("#artifact-state").textContent = `${job.artifact.mime_type} / ${job.artifact.size_bytes} bytes`;
    document.querySelector("#preview").innerHTML = `<img src="${job.artifact.url}" alt="Campaign radio key visual">`;
    const frame = document.querySelector("#filmstrip-frame");
    frame.querySelector(".frame-thumbnail").innerHTML = `<img src="${job.artifact.url}" alt="Frame 01 thumbnail">`;
    frame.querySelector("small").textContent = `Seed ${job.recipe.seed} · ${job.status}`;
    const values = [
      job.recipe.seed,
      job.workflow.digest.slice(0, 16),
      job.artifact.sha256.slice(0, 20),
      job.artifact.provider_metadata.renderer,
      job.retry_of ? `Retry of ${job.retry_of.slice(0, 12)}` : "Original run",
    ];
    document.querySelectorAll("#metadata dd").forEach((node, index) => node.textContent = values[index]);
  }
}

function showFormError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
}

function hideError() {
  errorBox.hidden = true;
}
