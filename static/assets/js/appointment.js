console.log("appointment.js loaded");
document.addEventListener("DOMContentLoaded", () => {
  const specialtySelect = document.getElementById("specialtySelect");
  const doctorSelect = document.getElementById("doctorSelect");

  if (!specialtySelect || !doctorSelect) return;

  const endpoint = specialtySelect.dataset.endpoint;
  console.log("endpoint:", endpoint);

  function resetDoctors(msg = "Select Doctor") {
    doctorSelect.innerHTML = `<option value="">${msg}</option>`;
    doctorSelect.disabled = true;
  }

  specialtySelect.addEventListener("change", async () => {
    const specialty = specialtySelect.value;
    resetDoctors("Loading...");

    if (!specialty) {
      resetDoctors("Select Doctor");
      return;
    }

    try {
      const url = endpoint + "?specialty=" + encodeURIComponent(specialty);
      const res = await fetch(url);
      const data = await res.json();

      doctorSelect.innerHTML = '<option value="">Select Doctor</option>';

      if (!data.doctors || data.doctors.length === 0) {
        resetDoctors("No doctors for this specialty");
        return;
      }

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
});
