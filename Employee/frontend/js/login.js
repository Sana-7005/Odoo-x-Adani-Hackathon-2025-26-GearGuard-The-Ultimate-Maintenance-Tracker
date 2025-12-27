// Fake users (you can add more)
const mockUsers = [
  { email: "rohan@example.com", password: "12345", name: "Rohan" },
  { email: "employee@test.com", password: "1111", name: "Test User" }
];

document.getElementById("loginBtn").addEventListener("click", () => {

  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPass").value.trim();
  const msg = document.getElementById("loginMsg");

  if(!email || !password){
    msg.innerText = "Enter email and password";
    return;
  }

  // check mock list
  const user = mockUsers.find(u => u.email === email && u.password === password);

  if(!user){
    msg.innerText = "Invalid email or password";
    return;
  }

  // save fake session
  localStorage.setItem("userEmail", user.email);
  localStorage.setItem("userName", user.name);

  // go to dashboard
  window.location.href = "index.html";
});
