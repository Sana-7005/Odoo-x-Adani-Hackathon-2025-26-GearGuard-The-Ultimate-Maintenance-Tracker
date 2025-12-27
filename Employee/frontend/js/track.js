async function loadRequests(){

  const res = await fetch("http://127.0.0.1:5000/requests/rohan@example.com");
  const data = await res.json();

  const table = document.getElementById("reqTable");
  table.innerHTML = "";

  data.forEach(r => {

    let statusClass = "";

    if (r.status === "New") statusClass = "new";
    if (r.status === "Accepted") statusClass = "accepted";
    if (r.status === "In Progress") statusClass = "in-progress";
    if (r.status === "Completed") statusClass = "completed";
    if (r.status === "Rejected") statusClass = "rejected";

    table.innerHTML += `
      <tr>
        <td>${r.description}</td>
        <td>${r.equipment}</td>
        <td>${r.team}</td>
        <td>
          <span class="status ${statusClass}">
            ${r.status}
          </span>
        </td>
      </tr>
    `;
  });
}

loadRequests();
