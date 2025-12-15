document.addEventListener("DOMContentLoaded", () => {
  const specialtySelect = document.getElementById("specialtySelect");
  const doctorSelect = document.getElementById("doctorSelect");
  const dayInput = document.getElementById("dayInput");
  const timeSelect = document.getElementById("timeSelect");

  if (!specialtySelect || !doctorSelect || !dayInput || !timeSelect) return;

  const doctorsEndpoint = specialtySelect.dataset.endpoint;
  const timesEndpoint = dayInput.dataset.timesEndpoint;

  function resetDoctors(msg = "Select Doctor") {
    doctorSelect.innerHTML = `<option value="">${msg}</option>`;
    doctorSelect.disabled = true;
  }

  function resetTimes(msg = "Select time") {
    timeSelect.innerHTML = `<option value="">${msg}</option>`;
    timeSelect.disabled = true;
  }

  async function loadTimes() {
    const doctorId = doctorSelect.value;
    const day = dayInput.value;

    resetTimes("Loading...");

    if (!doctorId || !day) {
      resetTimes("Select time");
      return;
    }

    try {
      const url = `${timesEndpoint}?doctor=${encodeURIComponent(doctorId)}&date=${encodeURIComponent(day)}`;
      const res = await fetch(url);
      const data = await res.json();

      if (!data.times || data.times.length === 0) {
        resetTimes("No available times");
        return;
      }

      timeSelect.innerHTML = `<option value="">Select time</option>`;
      data.times.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        timeSelect.appendChild(opt);
      });

      timeSelect.disabled = false;
    } catch (e) {
      console.error("Failed to load times:", e);
      resetTimes("Error loading times");
    }
  }

  specialtySelect.addEventListener("change", async () => {
    const specialty = specialtySelect.value;
    resetDoctors("Loading...");
    resetTimes("Select time");

    if (!specialty) {
      resetDoctors("Select Doctor");
      return;
    }

    try {
      const url = doctorsEndpoint + "?specialty=" + encodeURIComponent(specialty);
      const res = await fetch(url);
      const data = await res.json();

      if (!data.doctors || data.doctors.length === 0) {
        resetDoctors("No doctors for this specialty");
        return;
      }

      doctorSelect.innerHTML = `<option value="">Select Doctor</option>`;
      data.doctors.forEach(d => {
        const opt = document.createElement("option");
        opt.value = d.id;
        opt.textContent = d.name;
        doctorSelect.appendChild(opt);
      });

      doctorSelect.disabled = false;
    } catch (e) {
      console.error("Failed to load doctors:", e);
      resetDoctors("Error loading doctors");
    }
  });

  doctorSelect.addEventListener("change", loadTimes);
  dayInput.addEventListener("change", loadTimes);
});
