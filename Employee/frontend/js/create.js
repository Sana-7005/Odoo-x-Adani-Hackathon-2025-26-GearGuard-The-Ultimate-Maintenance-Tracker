const equip = document.getElementById("userEquipment");
const auto = document.getElementById("autoTeam");
const otherBox = document.getElementById("otherBox");
const otherInput = document.getElementById("otherInput");

const teams = {
  "Laptop 01": "IT Support",
  "Laptop 02": "IT Support",
  "Desktop PC": "IT Support",
  "Printer A": "IT Support",
  "Server Rack": "Network Team",

  "Generator A": "Maintenance Team",
  "Air Conditioner Unit": "Facilities",
  "CCTV Camera": "Security Team"
};


// ========= EQUIPMENT CHANGE =========
equip.addEventListener("change", () => {

  // If "Other" — show input + fallback team
  if (equip.value === "other") {
    otherBox.style.display = "block";
    auto.value = "Maintenance Team";
    return;
  }

  // Normal equipment
  otherBox.style.display = "none";
  auto.value = teams[equip.value] || "Maintenance Team";
});


// ========= POPUP =========
function openPopup(){ 
  document.getElementById("successPopup").style.display="flex"; 
}
function closePopup(){ 
  document.getElementById("successPopup").style.display="none"; 
}


// ========= SUBMIT REQUEST =========
document.querySelector(".primary-btn").addEventListener("click", async () => {

  // If "Other" is selected — use typed name
  const selectedEquipment =
    equip.value === "other" ? otherInput.value : equip.value;

  const payload = {
    name: "Rohan",
    email: "rohan@example.com",
    equipment: selectedEquipment,
    team: auto.value,
    description: document.querySelector("textarea").value
  };

  await fetch("http://127.0.0.1:5000/requests",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });

  openPopup();
});
