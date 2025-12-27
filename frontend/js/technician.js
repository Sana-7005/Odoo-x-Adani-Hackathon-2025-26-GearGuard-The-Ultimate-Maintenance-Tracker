// (Optional — later this will come from login)
const TECH_NAME = "Tech-01";

async function loadJobs() {

  const res = await fetch("http://127.0.0.1:5001/tech/jobs");
  let data = await res.json();

  // ========= FILTERS + SEARCH =========
  const search = document.getElementById("searchBox")?.value.toLowerCase() || "";
  const filter = document.getElementById("statusFilter")?.value || "all";

  let list = data;

  // search
  list = list.filter(r =>
    r.description.toLowerCase().includes(search) ||
    r.equipment.toLowerCase().includes(search)
  );

  // status filter
  if (filter !== "all")
    list = list.filter(r => r.status === filter);

  // ========= TABLE RENDER =========
  const table = document.getElementById("techTable");
  table.innerHTML = "";

  list.forEach(r => {

    let badge = "";

    if (r.status === "New") badge = `<span class="badge new">New</span>`;
    if (r.status === "Accepted") badge = `<span class="badge accepted">Accepted</span>`;
    if (r.status === "In Progress") badge = `<span class="badge progress">In Progress</span>`;
    if (r.status === "Completed") badge = `<span class="badge done">Completed</span>`;
    if (r.status === "Rejected") badge = `<span class="badge reject">Rejected</span>`;

    table.innerHTML += `
      <tr>
        <td>${r.id}</td>
        <td>${r.equipment}</td>
        <td>${r.description}</td>
        <td>${badge}</td>

        <td>

          ${r.status === "New" ? `
            <button class="accept" onclick="claim(${r.id}, 'Accepted')">Accept</button>
            <button class="reject" onclick="claim(${r.id}, 'Rejected')">Reject</button>
          ` : ""}

          ${r.status === "Accepted" ? `
            <button class="start" onclick="updateJob(${r.id}, 'In Progress')">Start</button>
          ` : ""}

          ${r.status === "In Progress" ? `
            <button class="done" onclick="updateJob(${r.id}, 'Completed')">Complete</button>
          ` : ""}

        </td>
      </tr>
    `;
  });
}


// ACCEPT / REJECT
async function claim(id, status) {

  await fetch(`http://127.0.0.1:5001/tech/claim/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      status,
      tech: TECH_NAME
    })
  });

  loadJobs();
}


// START / COMPLETE
async function updateJob(id, status) {

  await fetch(`http://127.0.0.1:5001/tech/update/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      status,
      note: ""   // API still expects this field
    })
  });

  loadJobs();
}


// ========= EVENT LISTENERS (LIVE FILTERING) =========
document.getElementById("searchBox").addEventListener("input", loadJobs);
document.getElementById("statusFilter").addEventListener("change", loadJobs);

async function loadEmployeeDashboard() {

  const email = "rohan@example.com";

  const res = await fetch(`http://127.0.0.1:5000/requests/${email}`);
  let data = await res.json();


  // ================= COUNTS =================
  document.getElementById("empTotal").innerText =
    "Total: " + data.length;

  document.getElementById("empOpen").innerText =
    "Open: " + data.filter(r => r.status === "New").length;

  document.getElementById("empProgress").innerText =
    "In Progress: " + data.filter(r => r.status === "In Progress").length;

  document.getElementById("empDone").innerText =
    "Completed: " + data.filter(r => r.status === "Completed").length;



  // ================= RECENT REQUESTS (ONLY 5) =================

  // newest first (assuming id increases)
  data.sort((a, b) => b.id - a.id);

  const recent = data.slice(0, 5);

  const tbody = document.getElementById("empTable");
  tbody.innerHTML = "";

  recent.forEach(r => {

    const statusClass = r.status.toLowerCase().replace(" ", "-");

    tbody.innerHTML += `
      <tr>
        <td>${r.description}</td>
        <td>${r.equipment}</td>
        <td>${r.team}</td>

        <td>
          <span class="badge ${statusClass}">
            ${r.status}
          </span>
        </td>
      </tr>
    `;
  });
}



// ================= NOTIFICATIONS =================
function toggleNotifications(){
  const box = document.getElementById("notifyBox");
  box.style.display =
    box.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", e => {
  if(!e.target.closest(".notify-bell")){
    document.getElementById("notifyBox").style.display = "none";
  }
});

let hideCompleted = false;
// hide completed when enabled
if (hideCompleted)
  list = list.filter(r => r.status !== "Completed");
document.getElementById("clearCompletedBtn").addEventListener("click", () => {
  hideCompleted = true;
  loadJobs();
});


// FIRST LOAD
loadJobs();
