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



// INITIAL LOAD
loadEmployeeDashboard();
const email = localStorage.getItem("userEmail");

if(!email){
  window.location.href = "login.html";
}
